#!/usr/bin/env bash
# Run as root on echo-prod: bash rollout-backend.sh <source.tar.gz> <sha256>
# A successful run prints its versioned rollback command. No secrets are printed.
set -euo pipefail
umask 077
[[ $EUID == 0 ]] || { echo 'root is required for Docker and systemd' >&2; exit 1; }
service=echo-universe.service
container=echo-universe-engine
base=/opt/octopus-cloud/echo-universe-engine
dropin=/etc/systemd/system/$service.d/90-reviewed-release.conf

if [[ ${1:-} == rollback ]]; then
  release=$(realpath -- "${2:?release directory required}")
  [[ $release == /opt/echo-universe-releases/* && -s $release/previous-image ]] || exit 1
  systemctl stop "$service"
  docker tag "$(cat "$release/previous-image")" echo-universe-engine:latest
  if [[ -e $release/previous-dropin ]]; then
    install -m 600 "$release/previous-dropin" "$dropin"
  else
    rm -f -- "$dropin"
  fi
  systemctl daemon-reload
  systemctl start "$service"
  echo 'Previous backend restored; persistent data and new writes retained.'
  exit
fi

archive=$(realpath -- "${1:?source archive required}")
expected=${2:?sha256 required}
[[ $expected =~ ^[a-fA-F0-9]{64}$ ]] || exit 1
printf '%s  %s\n' "$expected" "$archive" | sha256sum --check --status
systemctl is-active --quiet "$service"
[[ -d $base/data && -f $base/deploy/echo-universe.env ]] || exit 1
[[ $(systemctl show "$service" -p DropInPaths --value) == '' ]] || {
  echo 'Existing service overrides need review before rollout.' >&2; exit 1;
}
release=/opt/echo-universe-releases/$(date +%Y%m%d-%H%M%S)-${expected:0:12}
mkdir -p "$release/source" "$release/effective" "$(dirname "$dropin")"
# Git archives contain tracked source only. Refuse unexpected absolute/traversal paths.
tar -tzf "$archive" | python3 -c 'import sys,pathlib; paths=sys.stdin.read().splitlines(); assert all(not pathlib.PurePosixPath(p).is_absolute() and ".." not in pathlib.PurePosixPath(p).parts for p in paths)'
tar -xzf "$archive" -C "$release/source"
image=echo-universe-engine:reviewed-${expected:0:12}
docker inspect --format '{{.Image}}' "$container" > "$release/previous-image"
docker tag "$(cat "$release/previous-image")" "echo-universe-engine:rollback-${expected:0:12}"
fragment=$(systemctl show "$service" -p FragmentPath --value)
cp -- "$fragment" "$release/previous-unit"
cp -- "$0" "$release/rollout-backend.sh"
docker build -t "$image" "$release/source"

# Merge missing approved policy records into versioned files. Existing groups and
# candidate definitions win; production data, identities and secrets stay in place.
docker run --rm --network none -i \
  -v "$base/data:/old-data:ro" -v "$release/effective:/effective" \
  "$image" python - <<'PY'
from pathlib import Path
import yaml
for filename, key in [('reviewers.yaml', 'groups'), ('public_candidates.yaml', 'candidates')]:
    approved = yaml.safe_load(Path('/app/data', filename).read_text())
    old = Path('/old-data', filename)
    effective = yaml.safe_load(old.read_text()) if old.exists() else approved
    assert isinstance(effective, dict) and isinstance(effective.get(key), dict)
    for identity, record in approved[key].items():
        effective[key].setdefault(identity, record)
    Path('/effective', filename).write_text(yaml.safe_dump(effective, allow_unicode=True))
candidate = yaml.safe_load(Path('/effective/public_candidates.yaml').read_text())['candidates']['stranger-memory']
assert candidate['required_approvals'] == 2 and candidate['continuity_reviewers']
groups = yaml.safe_load(Path('/effective/reviewers.yaml').read_text())['groups']
assert candidate['reviewer_group'] in groups
assert Path('/app', candidate['source_path']).is_file()
PY

python3 - "$release" "$image" "$base" <<'PY'
from pathlib import Path
import re, sys
release, image, base = sys.argv[1:]
unit = Path(release, 'previous-unit').read_text()
logical = re.sub(r'\\\n\s*', ' ', unit)
commands = re.findall(r'^ExecStart=(.+)$', logical, re.M)
assert len(commands) == 1
command = commands[0]
assert command.startswith('/usr/bin/docker run ') and command.count('echo-universe-engine:latest') == 1
console = f'{base}/console:/app/console'
assert console in command and f'{base}/data:/app/data' in command
command = command.replace(console, f'{release}/source/console:/app/console:ro')
extra = f'-v {release}/effective/reviewers.yaml:/app/data/reviewers.yaml:ro -v {release}/effective/public_candidates.yaml:/app/data/public_candidates.yaml:ro '
command = command.replace('echo-universe-engine:latest', extra + image)
Path(release, 'new-dropin').write_text('[Service]\nExecStart=\nExecStart=' + command + '\n')
PY

curl -fsS --max-time 10 http://127.0.0.1:8010/api/health > "$release/previous-health.json"
switched=0
rollback_on_error() {
  if [[ $switched == 1 ]]; then
    bash "$release/rollout-backend.sh" rollback "$release"
  else
    systemctl start "$service"
  fi
}
trap rollback_on_error ERR
systemctl stop "$service"
# A consistent snapshot after the writer has stopped; never restores over new writes automatically.
tar -czf "$release/data-before.tar.gz" -C "$base" data
install -m 600 "$release/new-dropin" "$dropin"
switched=1
systemctl daemon-reload
systemctl start "$service"
for attempt in $(seq 1 30); do
  if curl -fsS --max-time 2 http://127.0.0.1:8010/api/health > "$release/current-health.json"; then break; fi
  sleep 2
done
curl -fsS --max-time 15 http://127.0.0.1:8010/api/canon/candidates/stranger-memory/governance > "$release/governance.json"
curl -fsS --max-time 15 http://127.0.0.1:8010/openapi.json > "$release/openapi.json"
python3 - "$release" <<'PY'
import json, sys
from pathlib import Path
release = Path(sys.argv[1])
read = lambda name: json.loads((release / name).read_text())
assert read('previous-health.json')['canon'] == read('current-health.json')['canon']
assert '/api/canon/candidates/{candidate_id}/resonance' in read('openapi.json')['paths']
assert read('governance.json')
PY
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://127.0.0.1:8010/api/canon/governance/candidates)
[[ $code == 401 || $code == 403 ]]
trap - ERR
echo "Backend health, governance, resonance routes and admin boundary verified."
echo "Rollback: bash $release/rollout-backend.sh rollback $release"

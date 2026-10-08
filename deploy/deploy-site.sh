#!/usr/bin/env bash
# Publish the static site (homepage, universe, developers, review) to universe.echo-age.com.
#
#   deploy/deploy-site.sh <branch>    build a release from <branch>, verify it, switch it live
#   deploy/deploy-site.sh rollback    swap `current` back to the release that was live before
#   deploy/deploy-site.sh status      show the live release, the previous one and recent releases
#
# Production layout, served statically by deploy/universe.echo-age.com.static.nginx.conf
# (/api and /assets are proxied to the container and are not touched here):
#
#   /var/www/echo-universe/releases/<name>/{home,universe,developers,review}
#   /var/www/echo-universe/current  -> releases/<live release>
#   /var/www/echo-universe/previous -> releases/<release live before it>
#
# Runs as the low-privilege `echo-deploy` user through the `echo-prod` SSH alias (see ~/.ssh/config).
# That account owns /var/www/echo-universe only. Releases are never modified once built, and the
# switch is an atomic symlink rename, so a failed deploy leaves the live site untouched.
set -euo pipefail

HOST="${ECHO_DEPLOY_HOST:-echo-prod}"
SITE="${ECHO_DEPLOY_SITE:-https://universe.echo-age.com}"
REPO="https://github.com/dengdenghua/echo-universe-engine.git"
ACTION="${1:-}"

usage() {
  sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'
  exit 64
}

remote() {
  ssh -o BatchMode=yes "$HOST" bash -s -- "$@"
}

# Fetch the live pages and every /home/ asset the homepage references; all must answer 200.
verify() {
  local failed=0 path code
  for path in / /universe/ /developers/ /api/health; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$SITE$path" || true)
    printf '  %-44s %s\n' "$path" "$code"
    [[ "$code" == 200 ]] || failed=1
  done
  while read -r path; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$SITE$path" || true)
    printf '  %-44s %s\n' "$path" "$code"
    [[ "$code" == 200 ]] || failed=1
  done < <(curl -s --max-time 30 "$SITE/" | grep -oE '(href|src)="/home/[^"]+"' | sed -E 's/^(href|src)="//; s/"$//' | sort -u)
  return "$failed"
}

case "$ACTION" in
  "" | -h | --help)
    usage
    ;;

  status)
    remote <<'REMOTE'
set -euo pipefail
root=/var/www/echo-universe
echo "current:  $(readlink -f "$root/current")"
echo "previous: $(readlink -f "$root/previous" 2>/dev/null || echo none)"
echo "recent releases:"
ls -1t "$root/releases" | head -5 | sed 's/^/  /'
REMOTE
    ;;

  rollback)
    remote <<'REMOTE'
set -euo pipefail
root=/var/www/echo-universe
cd "$root"
[[ -e previous ]] || { echo "no previous release recorded" >&2; exit 1; }
live=$(readlink -f current)
target=$(readlink -f previous)
ln -sfn "$target" current.new && mv -Tf current.new current
ln -sfn "$live" previous.new && mv -Tf previous.new previous
echo "live:     $(readlink -f current)"
echo "previous: $(readlink -f previous)"
REMOTE
    echo "verifying $SITE"
    verify || { echo "verification failed after rollback" >&2; exit 1; }
    ;;

  *)
    branch="$ACTION"
    echo "deploying branch '$branch' to $HOST"
    remote "$branch" "$REPO" <<'REMOTE'
set -euo pipefail
branch="$1"
repo="$2"
root=/var/www/echo-universe
src="$HOME/release-src"

# A shallow, sparse clone that only ever holds the four static site folders.
if [[ ! -d "$src/.git" ]]; then
  git clone --quiet --depth 1 --filter=blob:none --sparse --branch "$branch" "$repo" "$src"
  git -C "$src" sparse-checkout set homepage universe developers review
fi
git -C "$src" fetch --quiet --depth 1 origin "$branch"
git -C "$src" reset --quiet --hard FETCH_HEAD
commit=$(git -C "$src" rev-parse --short HEAD)
echo "source:   $(git -C "$src" log --oneline -1)"

release="$root/releases/$(date +%Y%m%d-%H%M%S)-$commit"
mkdir "$release"
cp -a "$src/homepage" "$release/home"
cp -a "$src/universe" "$src/developers" "$src/review" "$release/"

# Refuse to switch unless every entry page made it into the release.
for page in home/index.html universe/index.html developers/index.html review/index.html; do
  [[ -s "$release/$page" ]] || { echo "missing $page; live site left unchanged" >&2; exit 1; }
done

ln -sfn "$(readlink -f "$root/current")" "$root/previous.new" && mv -Tf "$root/previous.new" "$root/previous"
ln -sfn "$release" "$root/current.new" && mv -Tf "$root/current.new" "$root/current"
echo "live:     $(readlink -f "$root/current")"
echo "previous: $(readlink -f "$root/previous")"
REMOTE
    echo "verifying $SITE"
    verify || { echo "verification failed: run 'deploy/deploy-site.sh rollback' to restore the previous release" >&2; exit 1; }
    echo "deployed."
    ;;
esac

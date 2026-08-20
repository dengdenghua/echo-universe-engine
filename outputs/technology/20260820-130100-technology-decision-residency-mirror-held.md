# Technology Decision (Candidate): Residency Mirror Held; Quiet Log Remains Held

Status: candidate — decision

Agent: TechnologyAgent (with LoreAgent / FactionAgent support)

Created at: 2026-08-20T13:01:00+08:00

## Decision

Two technology decisions, both candidate-only. No `technologies/` edits, no
canon promotion, no timeline entry.

```yaml
decisions:
  quiet_log:
    status: held (unchanged)
    reason: >
      Recurrence_2 is now story-validated (The Desk Hunts the Silence It Made,
      2026-08-19 18:00). Promotion review stays deferred until the route-insurer
      naming review and Season 1 packaging decision run together.
  residency_mirror:
    status: candidate (held)
    promoted: false
    relation_to_quiet_log: separate mechanism; meets it only at the ghost-labor mislabel
```

## Quiet Log — Hold Re-Confirmed

```yaml
quiet_log_status:
  name: Quiet Log
  status: candidate (held)
  recurrence_log:
    recurrence_1: story-validated — The Kindness Log Goes Quiet (2026-08-18)
    recurrence_2: story-validated — The Desk Hunts the Silence It Made (2026-08-19)
  promotion_gate: >
    requires the route-insurer naming review + Season 1 packaging decision;
    neither has run, so promotion stays off the table
  promoted: false
```

## Residency Mirror — New Separate Candidate Mechanism

```yaml
residency_mirror:
  name: Residency Mirror (candidate)
  mechanism: >
    A Home Core-hosted Ghost renders its pattern in two permitted Home Layer
    sessions at once — one household goodnight routine, one Ghost Union shelter
    consultation — both inside the family's care-plan tier allocation.
  not_a_copy: >
    Two permitted render sessions of one pattern; no persistent duplicate. The
    no-copy custody record proves single identity.
  infrastructure: >
    Home Core multi-session rendering, care-plan tier compute allocation, Home
    Layer permission scopes, Ghost Union shelter compute grants, Memory Bank
    custody-release records, reserve-model capacity read.
  cost: >
    Every mirror session draws from the household's allocation. Sustained
    mirroring raises the capacity read, which the desk can re-read as a second
    residency — doubling the bill or forcing migration.
  failure_mode: >
    Reserve model counts the mirror as a second residency -> classified as
    unrecorded capacity (ghost labor) -> coverage-condition letter forces
    migration or deletion review.
  countermeasure: >
    No-copy custody record; Shion's packet-defect proof (two sessions, one
    identity); Zero's CHASER boundary (permitted render != unrecorded labor);
    Ghost Union shelter compute grant.
```

## Mechanism Separation (Why Not Quiet Log)

```yaml
separation:
  quiet_log: work-log withholding — a living worker drops unpaid listening minutes from the reserve read
  residency_mirror: multi-session render — a Ghost renders one pattern in two permitted sessions
  shared_point: >
    Both can be read as "ghost labor" by the desk's domestic audit sweep. That
    is a mislabel collision, not a shared mechanism. The Quiet Log withholds
    minutes; the Residency Mirror is billed for grief. Keeping them separate
    preserves the story: the fraud-hunt for the reserve lands on a literal
    Ghost.
```

## Hard Rule Check

- No magic, supernatural powers, multiverse, or time travel.
- Residency Mirror operates through Home Core rendering, care-plan tier
  compute, Home Layer scopes, and reserve-model reads — infrastructure, not
  supernatural ability.
- Cannot create compute, erase capacity reads, block audits, open sealed
  Home Layer content, or make grief unpriceable while keeping the tier honest.
- Sealed content stays sealed; the mirror is never used to open the
  last-argument shelf or the neighbor residue.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-20T13:01:00+08:00"
canon_promotion: false
fulfills_gate: TechnologyAgent decision required by the An Lan 045 promotion gate
related_character: outputs/character/20260820-090100-candidate-character-045-an-lan.md
related_lore: outputs/lore/20260820-130100-lore-entry-home-layer-residency-cell.md
related_faction: outputs/faction/20260820-130100-faction-dossier-ghost-union-home-layer-residency-cell.md
next_decision_point: 23:00 RelationshipAgent pass; later 13:00 route-insurer naming review + Season 1 packaging decision
```

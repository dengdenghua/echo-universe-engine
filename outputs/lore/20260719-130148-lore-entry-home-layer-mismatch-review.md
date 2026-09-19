# Lore Entry: Home Layer Mismatch Review

## Candidate Canon Entry

A Home Layer Mismatch Review is the first civil classification step after a
living person, Home Core, or room routine begins carrying care-pattern evidence
that belongs to more than one household.

It does not decide whether the person is guilty, infected, possessed, or no
longer themselves. It decides what kind of mismatch has appeared, what must be
paused, what can safely continue, and which routines should be treated as
private care, legal evidence, financial asset, public hazard, or possible Ghost
self-reference.

The review exists because the Memory Sea can injure ordinary people without a
weapon. A daughter may refuse to open the door because her mother now knows a
dead stranger's tea ritual. A school gate may deny pickup because a caregiver's
breakfast sequence matches another family. A landlord may demand reset because
the apartment looks less rentable while it hesitates. Memory Bank may call the
same borrowed routine a recoverable continuity asset before the family knows
whether it is grief, contamination, or testimony.

## Trigger Conditions

```yaml
home_layer_mismatch_review:
  trigger:
    actor: living_resident | caregiver | Home Core | room_routine | market_or_clinic_system
    signal:
      - care_pattern_from_unrelated_household
      - domestic_access_caution
      - cross_home_medical_reminder
      - false_guardian_or_resident_fit
      - deceased_exit_phrase_or_refusal
      - post_bloom_reconciliation_drift
  immediate_rule:
    meaning: stabilize daily life before deciding ownership or personhood
    protection: pause only the risky action, not the whole person
```

## Review Classes

```yaml
mismatch_class:
  benign_echo:
    meaning: harmless routine echo with no access, medical, legal, or selfhood consequence
    protection: local logging and consent-based deletion option
  domestic_access_risk:
    meaning: mismatch affects door, payment, custody, kitchen, medication, or care access
    protection: manual witness route and scoped safety pause
  borrowed_care_evidence:
    meaning: routine may prove another household's injury, death, consent, refusal, or repair path
    protection: preservation hold before reset or commercial claim
  asset_claim_conflict:
    meaning: Memory Bank, insurer, family trust, or estate asserts ownership language
    protection: financial claim blocked until care and evidence status are reviewed
  personhood_adjacent_trace:
    meaning: repeated refusal, exit phrase, or adaptive care suggests possible Ghost self-reference
    protection: Ghost Court or White Harbor witness route before erasure
  carrier_containment_error:
    meaning: CHASER or civic systems classify a living mismatch holder as a hazard without harm proof
    protection: containment language must be reviewed against actual technical route
```

## Social Function

- Gives families a way to keep a person present while the Home Layer is unsure
  how to classify them.
- Prevents landlords and reset contractors from treating mismatch cleanup as
  ordinary maintenance before evidence is captured.
- Forces Memory Bank to wait before converting borrowed care into an asset
  claim.
- Gives White Harbor a narrow review lane for post-awakening civic harm that is
  intimate, technical, and politically explosive.
- Lets CHASER field teams separate actual propagation risk from fear-driven
  carrier language.

## Failure Modes

- Clean-house reset: a landlord restores access by deleting the borrowed
  routines before anyone maps their source.
- Compassionate deletion: a family erases the mismatch because keeping a
  stranger's care inside the home feels unbearable.
- Containment inflation: officers treat the mismatch holder as infectious even
  when the route is a Home Layer reconciliation error.
- Asset capture: Memory Bank claims a borrowed routine as recoverable continuity
  property and pressures the family to preserve it for financial review.
- Public shaming: neighbors identify the mismatch holder as a thief of grief
  rather than a person caught in broken infrastructure.

## Story Hooks

- Liang Suyin is allowed to enter her apartment through a manual witness route,
  but the Home Core remains in caution mode until her borrowed-care packet is
  classified.
- Miao learns that opening the latch does not solve the case; it creates the
  first human witness record against a clean reset.
- Shion proves that Suyin is not a source but a visible surface of citywide
  post-bloom Home Layer reconciliation drift.
- Eve interviews families who both fear Suyin and need her to repeat the last
  useful routines their homes lost.
- A Memory Bank officer calls a dead man's tea ritual an asset; Luna calls it
  an exit phrase that deserves witness before use.

## Consistency Notes

- Home Layer Mismatch Review is a civil and technical classification process
  using Home Core habit graphs, Home Layer room routines, wake anchors, access
  logs, medical reminders, landlord reset permissions, CHASER caution labels,
  and Memory Bank claim notices.
- It does not explain the mismatch as magic, possession, supernatural haunting,
  multiverse contact, time travel, or literal physics-breaking action.
- Distinct from Care Status Renewal: care renewal reviews whether a routine
  remains funded or protected; mismatch review classifies cross-household care
  appearing in the wrong person or home.
- Distinct from Continuity Loss Freeze: loss freeze preserves damaged repair
  evidence after an incident; mismatch review classifies borrowed care before
  reset, containment, financial claim, or access restoration.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-19T13:01:48+08:00"
canon_promotion: false
related_candidates:
  - outputs/story/20260718-180218-story-beat-borrowed-morning.md
  - outputs/relationship/20260718-230105-relationship-update-borrowed-morning.md
  - outputs/lore/20260718-130241-lore-entry-continuity-loss-freeze.md
requires:
  - TechnologyAgent entry for Borrowed Care Attribution Packet
  - FactionAgent impact on Memory Bank, CHASER, White Harbor, landlords, Ghost Union, and Black Zone
  - ConsistencyAgent review against care-status, delay-token, restoration-freeze, and Season 2 Memory Storm candidates
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```

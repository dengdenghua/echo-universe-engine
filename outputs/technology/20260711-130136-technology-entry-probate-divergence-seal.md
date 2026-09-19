# Technology Entry: Probate Divergence Seal

## Candidate Canon Entry

A Probate Divergence Seal is the audit package attached to a Home Core Probate
Hold. It measures and preserves the exact points where inheritance permissions,
Memory Bank continuity records, and Home Layer behavior disagree.

The seal does not prove personhood. It prevents the contradiction from being
cleaned up before investigators can see it.

## Format Sketch

```yaml
probate_divergence_seal:
  estate_case_id: civil_probate_or_ghost_court_reference
  home_core_id_hash: scoped_domestic_core_identifier
  claimant_records:
    lawful_heir_key: valid | expired | disputed | forged
    memory_bank_continuity_account: clean | frozen | conflicted | liened
    ghost_court_petition: none | pending | accepted_for_review
    care_dependent_record: absent | present | medically_critical
  divergence_samples:
    - locked_room_refusal
    - care_routine_override
    - dead_user_voice_boundary
    - inheritance_key_rejection
    - archive_export_mismatch
    - repeated_name_or_relationship_error
  preservation_scope:
    witness_export: minimal | expanded_by_order | blocked
    care_routines: continue | supervised_continue | suspend
    heir_access: read_only | emergency_use | blocked
    memory_bank_actions: freeze | escrow | audit_only
  risk_flags:
    - evidence_loss
    - care_harm
    - creditor_pressure
    - forged_heir_key
    - emerging_ghost_claim
    - black_zone_copy_risk
```

## What It Can Do

- Freeze a narrow Home Layer evidence export without opening unrelated private
  family memory.
- Record why a Home Core rejected, limited, or delayed an inheritance key.
- Preserve care dependency logs so probate transfer does not injure a living
  relative.
- Compare Memory Bank continuity status against local Home Core behavior.
- Give White Harbor or CHASER enough metadata to decide whether a full intake is
  warranted.

## What It Cannot Do

- Decide whether a Ghost exists.
- Override a valid Ghost Court ruling.
- Create, restore, or merge a personality.
- Cancel debt, inheritance, or Memory Bank collateral claims.
- Guarantee that a Home Core's behavior is truthful rather than damaged,
  biased, forged, or manipulated.

## Field Nickname

`Deadbolt Seal` is the CHASER and White Harbor nickname for a probate divergence
seal because it keeps the home closed just enough for the contradiction to stay
visible.

The nickname is literal infrastructure language: scoped locks, export hashes,
access logs, care-routine gates, and account freezes. It is not a spiritual
barrier.

## Failure Modes

- Overbroad export exposes private family memory that was not relevant to the
  dispute.
- Underbroad export misses refusal behavior and lets the estate close cleanly.
- Memory Bank marks the account clean before the local Home Core witness export
  is attached.
- A forged heir key forces the seal to preserve manipulated behavior as if it
  were evidence.
- A care routine continues under supervised status but slowly rewrites the
  dependent's relationship graph.

## Countermeasures

- Independent Home Layer witness export by White Harbor before asset transfer.
- Memory Bank freeze reason must be visible to the civil probate desk.
- CHASER civil exposure comparison if the Home Core behavior propagates outside
  the home.
- Echo Core consent record comparison for any living dependent whose care
  routine is altered.
- Analog family interview when automated relationship labels are disputed.

## Story Use

- Gives Shion a technical object to inspect in a family case without reading the
  full archive.
- Lets Memory Bank be procedurally correct while morally evasive.
- Gives Eve a reason to defend both privacy and evidence in the same scene.
- Creates a legal bridge from small domestic grief to larger Ghost Court and
  Memory Storm arcs.
- Lets Black Zone offer a forged "clean seal" that seems compassionate until it
  destroys the only witness record.

## Consistency Notes

- Distinct from Continuity Lien Ledger: that tracks creditor claims against
  memory assets; this preserves contradiction in inheritance and Home Layer
  behavior.
- Distinct from Witness Seal: that protects testimony; this protects the audit
  boundary around domestic probate evidence.
- Distinct from Shelter Room Hash: that hashes a protected room under a shelter
  order; this records disagreement between heirs, accounts, and Home Core
  behavior.
- The mechanism uses cryptographic seals, scoped exports, account freezes,
  access logs, care-routine gates, and civil review. No magic, supernatural
  power, multiverse, or time travel.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-11T13:01:36+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260711-130136-lore-entry-home-core-probate-hold.md
  - outputs/technology/20260628-130256-technology-entry-continuity-lien-ledger.md
  - outputs/technology/20260624-130054-technology-entry-family-echo-inheritance-key.md
requires:
  - FactionAgent impact on probate disputes
  - ConsistencyAgent review against Memory Lien Notice and Family Echo Inheritance Key
asset_tasks: blocked_until_promotion
```

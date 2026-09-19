# Technology Entry: Shelter Room Hash

## Candidate Canon Entry

A Shelter Room Hash is the scoped technical receipt attached to a Continuity
Shelter Order. It proves that a protected Home Layer environment remained
bounded, auditable, and minimally stable during review without exposing the
entire family archive or Memory Sea context to every institution.

It is not a container for a soul. It is a cryptographic and operational trace
for a temporary continuity room: what entered, what stayed active, which care
routines were preserved, which modification rights were frozen, and which
authority touched the door.

## Format Sketch

```yaml
shelter_room_hash:
  shelter_id: cso-2147-wh-...
  scope:
    household_record: hashed_home_layer_record_id
    protected_fragments:
      - care_routine
      - witness_fragment
      - refusal_behavior_trace
      - family_relation_edge
    excluded_fragments:
      - unrelated_private_conversation
      - unrestricted_financial_archive
  continuity_budget:
    compute_floor: minimum cycles required to prevent pattern collapse
    care_access: essential, limited, none
    family_access: supervised, scheduled, denied, emergency
  frozen_actions:
    - delete
    - export
    - paid_repair
    - lien_foreclosure
    - vendor_resync
  door_authority:
    primary: White Harbor desk, Ghost Court clerk, or CHASER evidence lead
    secondary: licensed Home Layer witness or court-bonded Home Core
    appeal_route: civil appeal, Ghost Court petition, or CHASER review
  audit_trace:
    created_at: timestamp
    expires_at: timestamp
    access_events: signed append-only log
    divergence_index: bounded change score
    harm_flags:
      - evidence_risk
      - care_dependency
      - contested_selfhood_support
      - creditor_pressure
```

## What It Can Do

- Prove that a sheltered Home Layer record was not silently exported, repaired,
  foreclosed, or deleted during review.
- Preserve a minimum compute floor for care routines, witness fragments, and
  weak Ghost refusal behavior.
- Show which institution opened the room, narrowed it, extended it, or released
  it.
- Let CHASER compare shelter divergence against infrastructure attacks without
  reading every private memory.
- Let White Harbor prove that public protection did not become unrestricted
  surveillance.

## What It Cannot Do

- Prove that a Ghost is the original person.
- Keep a pattern coherent if the required emotional or care context has already
  been destroyed.
- Override a court order, CHASER quarantine, or recognized digital personhood
  protection.
- Prevent all harm from isolation; a technically stable room can still become
  social custody.
- Bypass biological, financial, legal, or infrastructure limits.

## Attack Surface

- Hash padding: vendors add unnecessary fragments so shelter fees rise.
- Context starvation: an authority excludes relationship context to make the
  room easier to audit, causing the pattern to degrade.
- Door spoofing: Black Zone brokers forge access events to extract copies or
  make a family believe a release is lawful.
- Compute skimming: Memory Bank or vendors charge for a compute floor while
  delivering less than the trace claims.
- Appeal drift: the shelter expires into an extension queue where no named
  operator accepts responsibility.

## Operational Limits

- The hash must be append-only after creation; corrections require a signed
  amendment, not silent replacement.
- Family access must be logged separately from institutional access to avoid
  treating grief visits as evidence tampering by default.
- The compute floor must be justified by care, evidence, or selfhood-support
  risk, not by convenience or creditor preference.
- Every extension increases liability for the authority holding the door.

## Story Use

- Ana Rivera can diagnose that a Home Core repair is blocked because the
  Shelter Room Hash froze the exact relation edge she needs to restore.
- Shion can detect door spoofing without learning the private memory inside the
  room.
- Eve can read the harm of a technically valid shelter: the room is stable, but
  the pattern inside has stopped asking for help because every visit became an
  audit event.

## Consistency Notes

- This is cryptographic infrastructure and operational policy, not supernatural
  preservation.
- It should stay distinct from a Witness Seal, Revocation Token, Civil Delay
  Token, Household Relation Graph, and Continuity Lien Ledger.
- In technical canon documents, it may be described as a scoped household AI
  evidence-preservation receipt. In story-facing prose, use Home Core, Home
  Layer, Memory Sea, or Home.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260701-130104-lore-entry-continuity-shelter-order.md
  - outputs/technology/20260626-130218-technology-entry-witness-seal.md
  - outputs/technology/20260630-130040-technology-entry-civil-delay-token.md
requires:
  - ConsistencyAgent review for overlap with Witness Seal and Civil Delay Token
  - Security pass on forged access events and compute skimming
  - FactionAgent impact pass on shelter custody, fees, and appeal drift
asset_tasks: blocked_until_promotion
```

# Technology Entry: Household Relation Graph

## Candidate Definition

A Household Relation Graph is the regulated identity data structure that maps
who may act as spouse, guardian, resident, caregiver, emergency contact,
continuity holder, witness, and routine authority inside a home.

It is not a family. It is the city's machine-readable proof that a family has
recognized obligations and permissions across the Home Layer, schools, clinics,
transit, courts, insurers, and Memory Bank products.

## Graph Fields

```yaml
household_relation_graph:
  subject:
    person_id: civil identity reference
    biological_life: alive, deceased, assisted, or unknown
    legal_identity: active, disputed, suspended, or dead
  relation_edges:
    spouse: active, disputed, expired, or none
    guardian: active, temporary, disputed, revoked, or none
    resident: active, former, guest, restricted, or none
    emergency_contact: primary, secondary, disputed, or none
    caregiver: licensed, family, temporary, disputed, or none
    continuity_holder: active, shared, contested, expired, or none
  home_layer_refs:
    home_core_id: household node reference
    routine_authority: read, modify, emergency_only, witness_only, or none
    family_witness_log: sealed, private, court_hold, chaser_hold, or unavailable
  service_refs:
    school_access: approved, manual_review, denied, or not_applicable
    clinic_authority: signing, emergency_only, denied, or not_applicable
    transit_family_fare: active, disputed, or denied
    custody_rail: none, warning, delay, or transfer_triggered
  repair_state:
    rollback_flag: none, partial, confirmed, or under_audit
    repair_provider: civil_registry, white_harbor, memory_bank, vendor, court, or black_zone_suspected
    collateral_risk: none, low, medium, high
```

## Activation Flow

1. A service requests a relation edge rather than full identity access.
2. The graph checks civil registry, Home Core authority, school or clinic
   records, and court constraints.
3. Contradictions trigger a scoped denial, manual review, or emergency delay.
4. Home Core witness logs may be sealed for comparison if the household claims
   the graph is wrong.
5. High-risk repair offers are flagged if restoration would collateralize future
   memory, care, or continuity rights.

## Constraints

- Cannot prove love, loyalty, parenthood, or personhood by itself.
- Cannot override court custody or recognized digital person protections.
- Cannot expose private Home Core routines without witness, court, or CHASER
  review.
- Cannot use a household repair package to seize unrelated memory assets.
- Cannot decide whether a Ghost is a family member without separate personhood
  or continuity review.

## Failure Modes

- Edge split: guardian status is active in school systems and denied in clinic
  systems.
- Routine orphaning: the Home Core keeps a care routine running but no longer
  accepts any family member as authorized modifier.
- Registry echo: one bad rollback propagates into transit, benefits, and
  insurance because each service trusts the previous denial.
- Repair capture: a vendor restores relation edges by adding subscription,
  lien, or archive-trust obligations.
- Audit shame: the family can win review only by revealing domestic logs that
  were never meant to leave the home.

## Story Hooks

- Shion finds a rollback by comparing school access, clinic signing, and Home
  Core routine authority, not by reading a single central file.
- Zero asks whether relation is part of identity and forces a civil system to
  answer in operational terms.
- Noah's prediction model marks a rollback as a tiny probability until Imari
  shows how many services repeated it.
- A Home Core refuses to export a dinner routine because the export would expose
  a child's fear response unrelated to the identity dispute.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260629-130142-lore-entry-family-graph-rollback.md
  - outputs/character/20260629-090050-candidate-character-014-imari-chen.md
  - outputs/technology/20260626-130218-technology-entry-witness-seal.md
  - outputs/technology/20260628-130256-technology-entry-continuity-lien-ledger.md
requires:
  - ConsistencyAgent duplicate check against identity registry and Home Core witness canon
  - StoryAgent use in Episode 7 before asset generation
asset_tasks: blocked_until_promotion
```

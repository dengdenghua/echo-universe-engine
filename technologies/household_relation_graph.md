# Household Relation Graph

A Household Relation Graph is the regulated identity data structure that maps
who may act as spouse, guardian, resident, caregiver, emergency contact,
continuity holder, witness, and routine authority inside a home.

It is not a family. It is the city's machine-readable proof that a family has
recognized obligations and permissions across the Home Layer, schools, clinics,
transit, courts, insurers, Home Core vendors, and Memory Bank products.

## Canon Scope

For Season 1 Episode 7, `Probability Debt`, the graph is the surface that lets a
living person's civil identity remain active while their family relation edges
fail across daily systems. Imari Chen is still alive, named, employed, and
legally present, but the school gate, clinic desk, transit family fare, custody
rail, and Home Core disagree about whether she is authorized as family.

```yaml
household_relation_graph:
  episode_scope: "Season 1 Episode 7 / Probability Debt"
  subject_state:
    biological_life: active
    legal_identity: active
    ghost_status: not_applicable
  relation_edges:
    - spouse
    - guardian
    - resident
    - caregiver
    - emergency_contact
    - continuity_holder
    - routine_authority
  service_surfaces:
    - school_access
    - clinic_authority
    - transit_family_fare
    - custody_rail
    - home_core_routine_permission
    - civil_registry_repair_queue
  rollback_states:
    - relation_pending
    - graph_split
    - household_orphaned
    - custody_triggered
    - repair_collateralized
```

## Family Graph Rollback

Family Graph Rollback is the failure mode in which relation edges revert, split,
or become disputed while individual identity records still pass. Families call
it being made a stranger inside your own house.

In Episode 7, a successful CHASER extraction route delays a civil registry
repair queue long enough for Imari's vulnerable graph to roll back. The result
is relation harm, not memory erasure: her daughter knows her, her spouse knows
her, and the Home Core still carries familiar routines, but the systems between
them treat those relationships as disputed evidence.

## Evidence Rule

The graph can request scoped Home Core witness fragments when a disputed edge
needs comparison. It cannot demand a full Home Layer export when a smaller
fragment can prove school pickup, clinic signing, routine authority, or
continuity-holder status.

```yaml
evidence_scope:
  allowed:
    - civil_registry_edge_history
    - school_or_clinic_denial_receipt
    - court_or_custody_file
    - home_core_witness_fragment
    - chaser_incident_hold
  blocked_without_review:
    - full_home_layer_export
    - unrelated_child_fear_response
    - unrelated_spouse_medical_detail
    - unrelated_financial_history
    - memory_bank_repair_bundle
```

## Limits

- The graph can prove recognized authority; it cannot prove love, loyalty, or
  moral parenthood.
- It cannot certify Ghost personhood or decide whether a Ghost is family.
- It cannot override court custody, digital person protections, or scoped
  privacy review.
- A repair provider cannot use graph restoration to seize unrelated memory
  assets.
- A rollback does not make Imari dead, erased, duplicated, possessed, or
  outside ordinary law.

## Story Use

The technology makes Episode 7 a civic infrastructure wound. The threat is not a
fight and not a haunting. It is a gate that knows a name but rejects a relation,
a clinic desk that refuses a signature, and a Home Core that remembers dinner
while denying authority over a fever protocol.

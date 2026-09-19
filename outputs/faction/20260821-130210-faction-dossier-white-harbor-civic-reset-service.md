# Faction Dossier (Candidate): White Harbor Civic Reset Service

Status: candidate — contractor layer

Agent: FactionAgent (with LoreAgent / TechnologyAgent support)

Created at: 2026-08-21T13:02:10+08:00

## Candidate Function

White Harbor Civic Reset Service is a municipal-contractor layer that clears,
inventories, sanitizes, and releases rooms after eviction, death, debt transfer,
contamination, or court-ordered vacancy. It is not a primary faction yet. In
this pass it remains a candidate institutional layer attached to White Harbor.

```yaml
faction_candidate:
  name: White Harbor Civic Reset Service
  status: candidate contractor layer
  parent_context: White Harbor municipal infrastructure
  public_role: post-eviction sanitation, hazard routing, room inventory, reset release
  private_pressure: >
    Must satisfy landlord turnover, sanitation safety, Memory Bank archive
    claims, CHASER evidence requests, and worker injury liability on the same
    clock.
  representative_character: Selene Arif
  promotion_state: held
```

## Stakeholder Pressure Map

- Landlords want the room clean and released on the cheaper clock.
- Memory Bank wants preserved rooms classified as recoverable archive value.
- CHASER wants evidence scope narrow enough to hold in court but broad enough
  to prevent evidence destruction.
- Ghost Union watches for rooms where care traces are erased as waste.
- Black Zone discard brokers buy what clean rooms leave behind.
- Reset crews want a safe room, a paid shift, and no discipline for filing a
  hold.

## Why It Is Not A Full Faction Yet

The service currently has one strong character route and one candidate
procedure. Promotion would be premature until Dirty Room Hold is story-validated
or another reset case proves that the service recurs as a Season 1 pressure
point.

It should stay smaller than White Harbor, Memory Bank, CHASER, and Ghost Union:
a local civic layer that makes their conflicts visible at floor level.

## Conflict Hooks

```yaml
conflicts:
  with_memory_bank: preserved room state can become estate value
  with_landlords: evidence delays turnover and rent recovery
  with_chaser: evidence line can protect or over-seize the room
  with_ghost_union: erased care traces may be treated as trash before review
  with_black_zone: discarded Home Core latches and door tags feed grief resale
  internal: crew safety and turnover metrics punish careful holds
```

## Pipeline State

```yaml
stage: candidate_output
agent: FactionAgent
created_at: "2026-08-21T13:02:10+08:00"
canon_promotion: false
related_lore: outputs/lore/20260821-130210-lore-entry-dirty-room-hold.md
related_technology: outputs/technology/20260821-130210-technology-decision-dirty-room-hold-held.md
related_character: outputs/character/20260821-090055-candidate-character-046-selene-arif.md
requires_consistency_review: true
```

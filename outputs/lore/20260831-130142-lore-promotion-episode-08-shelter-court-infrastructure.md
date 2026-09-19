# Lore Promotion: Episode 08 Shelter / Court Infrastructure

Status: promotion_review_passed

Agent: LoreAgent with TechnologyAgent and FactionAgent support

Created at: 2026-08-31T13:01:42+08:00

Canon action:

- Promoted `technologies/continuity_shelter_order.md`.
- Promoted `technologies/shelter_room_hash.md`.
- Updated `factions/white_harbor.md`, `factions/memory_bank.md`, and
  `factions/chaser.md` with narrow Episode 8 impacts.

## Decision

Episode 8 may use Continuity Shelter Orders and Shelter Room Hashes as primary
canon infrastructure, but only in a narrow civic/legal function: valid public
protection can preserve damaged Home Layer evidence while blocking the repair a
living family needs.

The promoted surface supports `The Court Inside ECHO` by making the court case
concrete before the story treatment is drafted. It does not promote Ana Rivera,
Imari Chen, Sofia Marin, or Yao Nian into recurring character canon.

## Canonized Functions

```yaml
episode_08_shelter_court_infrastructure:
  continuity_shelter_order:
    function: public_protection_for_high_risk_home_layer_record
    episode_use: protects_Imari_Chen_damaged_relation_edge
    danger: protection_becomes_lived_custody
  shelter_room_hash:
    function: technical_receipt_for_protected_home_layer_room
    episode_use: blocks_Ana_Rivera_repair_until_partial_release
    remedy: append_only_preservation_plus_supervised_repair
  ghost_court_release_authority:
    function: partial_release_and_evidence_preservation
    prohibited_scope: full_personhood_ruling_or_Project_E_01_reveal
  faction_impacts:
    White_Harbor: named_door_operator_liability
    Memory_Bank: shelter_fee_and_future_rights_pressure
    CHASER: narrow_harm_risk_and_evidence_review
```

## Held Outside Promotion

- Full Ghost Court procedure and general identity-law doctrine.
- Full Project E-01 disclosure, ninth upload explanation, vessel language, or
  Zero origin reveal.
- Any ruling that relation evidence proves love, parenthood, personhood, or
  complete identity continuity.
- General cross-episode shelter law beyond the Episode 8 use case.
- Ana Rivera, Imari Chen, Sofia Marin, or Yao Nian as recurring full character
  canon.

## StoryAgent Routing

The next StoryAgent pass should draft the full Episode 8 treatment in this
order:

1. Ana identifies a repairable relation edge inside Imari's apartment.
2. The Shelter Room Hash blocks repair because the edge is protected evidence.
3. Memory Bank offers faster fee-backed stabilization with future rights risk.
4. White Ghost Team petitions Ghost Court for partial release.
5. Eve, Shion, Noah, Ana, and Zero testify within bounded authority.
6. Ghost Court grants supervised release and preserves the original damaged
   edge as append-only witness evidence.
7. Zero receives a restricted witness trace label without explanation.

## Pipeline State

```yaml
idea: episode_08_shelter_court_infrastructure
candidate_output: reviewed
consistency_check: paired
canon_promotion: true
timeline_update: not_required
relationship_update: blocked_until_story_acceptance
faction_update: complete
asset_task_generation: supplemental_prop_task_created
next_recommended_step: "18:00 StoryAgent should draft the full Episode 8 treatment using the promoted shelter infrastructure and the 09:00 character boundary sheet."
```

# Technology Promotion: Consent-Gated Live Route Access

Status: promoted_narrow

Agent: LoreAgent with TechnologyAgent support

Scope: Season 1 Episode 5 / `Dream Child`

Canon action:

- Added `technologies/consent_gated_live_route_access.md`.
- Kept the entry episode-specific rather than promoting a general Dream Network
  access standard.

Created at: 2026-08-28T13:01:25+08:00

Primary reviewed sources:

- `outputs/lore/20260826-130105-lore-entry-consent-gated-live-route-access.md`
- `outputs/technology/20260826-130105-technology-entry-consent-gated-live-route-access.md`
- `outputs/faction/20260826-130105-faction-impact-consent-gated-live-route-access.md`
- `outputs/lore/20260827-130125-lore-gate-episode-05-dream-child-combined-review.md`
- `outputs/story/20260827-180149-episode-05-dream-child-story-acceptance.md`
- `relationships/episode_05_dream_child_civic_to_clinical_relationships.yaml`

## Promotion Decision

Promote Consent-Gated Live Route Access as the specific packet used by Episode
5 to bridge Dream Network Civic Claims and supervised Room 7 contact.

The promotion is deliberately narrow. It canonizes the access packet's function,
required authorities, prohibited material, and revocation rule. It does not make
the packet a routine Dream Network product, does not prove Room 7 identity, and
does not establish a broad law for every future live route.

## Canonized Elements

```yaml
promoted_elements:
  - spill_report_hold_to_room_7_bridge
  - refund_non_erasure_receipt_as_initiating_record
  - family_scope_holder_required
  - claims_witness_required
  - consent_reviewer_required
  - packet_validator_required
  - clinical_supervisor_required
  - observation_only_first_contact
  - twelve_minute_first_contact_cap
  - revocation_closes_or_suspends_access
```

## Held Back

```yaml
held_back:
  - room_7_identity_answer
  - ghost_personhood_ruling
  - memory_bank_archive_truth_value
  - chaser_family_containment
  - general_cross_episode_technology_standard
  - raw_home_layer_or_phrase_export
```

## Faction Effects

Dream Network now has a canon reason to let an Episode 5 refund proceed without
purging the preserved route packet. Memory Bank can object at hash level but
cannot receive raw family material. CHASER stays at route-level notice unless a
new live-patient threshold appears. White Ghost Team remains a bounded witness
and validator group, not the source of family authority.

## Pipeline State

```yaml
stage: canon_promotion
agent: LoreAgent
created_at: "2026-08-28T13:01:25+08:00"
canon_promotion: true
primary_files_changed:
  - technologies/consent_gated_live_route_access.md
  - factions/dream_network.md
timeline_update: not_required_macro_timeline_unchanged
relationship_update: already_promoted_dedicated_episode_05_bridge
asset_task_generation: not_required_existing_room_7_asset_task_sufficient
next_recommended_step: >
  StoryAgent should draft or revise the full Episode 5 treatment using the
  promoted packet and the named Dream Network closure supervisor boundary.
```

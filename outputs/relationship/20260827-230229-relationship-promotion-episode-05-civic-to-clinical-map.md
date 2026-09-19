# Relationship Promotion: Episode 05 Civic-To-Clinical Map

Status: canon_promotion

Agent: RelationshipAgent

Created at: 2026-08-27T23:02:29+08:00

Promoted canon file:

- `relationships/episode_05_dream_child_civic_to_clinical_relationships.yaml`

Primary sources:

- `relationships/dream_network_civic_claims_relationships.yaml`
- `relationships/dream_child_case_relationships.yaml`
- `outputs/story/20260825-180200-episode-05-dream-child-civic-prelude-package.md`
- `outputs/story/20260826-180109-episode-05-room-7-consent-gated-sequence.md`
- `outputs/relationship/20260826-230216-relationship-update-room-7-consent-gated-bridge.md`
- `outputs/lore/20260827-130125-lore-gate-episode-05-dream-child-combined-review.md`
- `outputs/story/20260827-180149-episode-05-dream-child-story-acceptance.md`

## Promotion Decision

Promote a dedicated Episode 5 civic-to-clinical relationship map.

Do not merge into `relationships/dream_child_case_relationships.yaml`, because
that file is already scoped to the older clinical Room 7 case and should remain
small. Do not merge into
`relationships/dream_network_civic_claims_relationships.yaml`, because that
file is promoted civic-prelude canon and stops before supervised Room 7 contact.

The new map is the narrow canon bridge between the public refund counter and
the hospital-attached Dream Network recovery ward.

## Canonized Relationship Rule

Episode 5 relationship authority now follows this order:

```yaml
episode_05_relationship_authority:
  first: Mara and Leina as civilian/family boundary holders
  second: Jules as claims witness whose hold prevents telemetry purge
  third: Min Seo-yun as clinical supervisor who must obey revocation
  fourth: White Ghost Team as bounded investigators and packet validators
  fifth: CHASER, Memory Bank, and Dream Network compliance as pressure systems
```

White Ghost Team may witness, narrow, validate, and challenge the route. They
do not own the family decision, identify the response, or overrule the stop.

## Promoted Boundaries

- Leina's `Stop` is a real relationship event and ends first contact.
- Mara remains the spoken boundary holder; she does not become an investigator.
- Jules matters because a valid hold keeps the route alive, not because he
  exposes a conspiracy.
- Min Seo-yun gains trust only by obeying civilian revocation.
- Luna's first-contact relationship is defined by restraint: she does not name
  the response, finish the phrase, or recommend deletion during review.
- Eve and Shion protect the family by making the packet smaller and weaker.
- Zero and Kane remain pressure-management edges, not rescuers.
- CHASER remains at route-level notice.
- Memory Bank's licensed-texture objection remains unresolved.

## Held As Candidate

```yaml
held_as_candidate:
  dara_kwon_named_supervisor: true
  consent_gated_live_route_access_as_general_technology: true
  child_pattern_identity_label_change: true
  memory_bank_archive_objection_truth_value: true
  recurring_status_for_mara_leina_jules: true
```

## Timeline And Asset Routing

No `timeline/timeline.yaml` edit is needed from this promotion because the file
tracks macro-history, not Season 1 episode internals.

No new asset task is needed. Existing tasks already cover the Spill Report Hold
Terminal, refund scene, consent-gated Room 7 scene, and Dara Kwon candidate.

## Downstream Step

The next StoryAgent pass can use the promoted bridge map to draft or revise the
full Episode 5 treatment. Technology promotion remains limited: `Consent-Gated
Live Route Access` should not become general infrastructure until the live use
case is promoted by a later LoreAgent/TechnologyAgent review.

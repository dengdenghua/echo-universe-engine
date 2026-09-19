# Lore Gate: Episode 05 Dream Child Combined Review

Status: candidate_gate

Agent: LoreAgent with FactionAgent and TechnologyAgent support

Scope: Season 1, Episode 05 / `Dream Child`

Canon action: none; this gate consolidates accepted candidate material and
identifies the exact promotion surface for a later canon decision.

Created at: 2026-08-27T13:01:25+08:00

Reviewed package:

- `outputs/story/20260825-180200-episode-05-dream-child-civic-prelude-package.md`
- `outputs/lore/20260826-130105-lore-entry-consent-gated-live-route-access.md`
- `outputs/technology/20260826-130105-technology-entry-consent-gated-live-route-access.md`
- `outputs/faction/20260826-130105-faction-impact-consent-gated-live-route-access.md`
- `outputs/story/20260826-180109-episode-05-room-7-consent-gated-sequence.md`
- `outputs/relationship/20260826-230216-relationship-update-room-7-consent-gated-bridge.md`
- `outputs/character/20260827-090054-candidate-character-052-dara-kwon.md`

## Gate Verdict

Pass as a combined Episode 5 candidate package.

Do not promote in this run. The package is now coherent enough for a later
StoryAgent or RelationshipAgent promotion decision, but the exact canon surface
must stay narrow:

- promote the civic-to-clinical episode route only after story acceptance;
- promote the relationship bridge only after deciding whether Episode 5 uses a
  dedicated Dream Child case map or extends the existing case YAML;
- keep Consent-Gated Live Route Access candidate-only until the Room 7 sequence
  is accepted as the first live use case;
- keep Dara Kwon candidate-only until Dream Network compliance needs a named
  supervisor in the promoted episode outline.

## Combined Episode Shape

```yaml
episode_05_combined_shape:
  title: Dream Child
  entry_wound: refund_payout_would_erase_route_telemetry
  public_site: Dream Network Civic Claims hall
  clinical_site: hospital-attached Dream Network recovery ward / Room 7
  civilian_anchor: Mara Elian
  family_scope_holder: Leina Elian
  claims_witness: Jules Mbeki
  clinical_supervisor: Min Seo-yun
  compliance_pressure: Dara Kwon candidate, or unnamed supervisor if not promoted
  white_ghost_posture: investigators, consent reviewers, packet validators, bounded witnesses
  unresolved_question: >
    Whether the responsive room is archive texture, active harm, an emerging
    Ghost-child pattern, or another ECHO infrastructure effect remains unproven.
```

The episode now has a clean civic-to-clinical route:

1. Mara and Leina enter through a public memorial route refund claim.
2. Jules blocks telemetry purge with the Spill Report Hold Terminal.
3. Eve and Shion reduce the evidence packet before White Ghost contact.
4. Leina grants a narrow, revocable live access scope.
5. Seo-yun opens Room 7 only under observation-only supervision.
6. Luna witnesses a response and obeys the stop condition.
7. CHASER and Memory Bank remain pressure systems, not final authorities.

## Lore Continuity Decision

Episode 5 should treat the Memory Sea as a civic infrastructure before it
treats it as a mystery room. The frightening fact is not that a room answers;
it is that ordinary procedures for refunds, licensed comfort texture, hospital
safety, and archive ownership can all touch a grieving family's Home Layer
before anyone knows what the answer means.

Use these lore boundaries in the next promotion pass:

- `Dream Network Civic Claims` and `Spill Report Hold Terminal` are already
  promoted narrow infrastructure.
- `Consent-Gated Live Route Access` remains a candidate bridge until the main
  Room 7 sequence is accepted.
- `Room 7` remains clinically supervised, not a hidden dream realm.
- `Memory Bank` may claim licensed texture but cannot receive raw family
  material through this package.
- `CHASER` receives route-level notice unless a later event reaches a live
  pediatric patient or leaves the supervised channel.
- `White Ghost Team` must not replace Leina, Mara, Jules, or Seo-yun as the
  source of authority.

## Faction Routing

```yaml
faction_routing:
  Dream_Network:
    current_role: refund_closure_and_live_access_gatekeeper
    allowed_pressure: settlement language, context enrichment requests, recorder fields
    barred_pressure: deletion of frozen hold, coercive broad Home Layer scope
  Memory_Bank:
    current_role: archive_objection_claimant
    allowed_pressure: hash-level licensed-texture comparison request
    barred_pressure: raw phrase playback or family archive capture
  CHASER:
    current_role: route-level safety notice
    allowed_pressure: deletion-ready warning if live patient linkage appears
    barred_pressure: family contamination intake from claims material alone
  Dream_Network_Recovery_Ward:
    current_role: clinical supervision and stop authority
    allowed_pressure: suspend contact, require wake boundary
    barred_pressure: laundering claims evidence into private ward-only records
  White_Ghost_Team:
    current_role: bounded investigators and witnesses
    allowed_pressure: consent narrowing, packet validation, route-level challenge
    barred_pressure: identity declaration, unsupervised Dream Dive, emotional override
```

## Technology Routing

The combined package should keep three technical objects distinct:

- `Spill Report Hold Terminal`: preserves the post-incident claim packet before
  refund closure purges telemetry.
- `Consent-Gated Live Route Access Packet`: requests the first supervised
  clinical contact using only narrow, revocable scope.
- `Wake Anchor Token` or equivalent analog exit record: proves Luna can leave
  the observation layer without turning contact into custody.

The first Room 7 contact may use timing pings, phrase fingerprints, affective
spill hashes, consent-boundary snapshots, and hash-only Home Core / Home Layer
references. It must not use raw Home Layer export, playable child voice, full
family archive, live pediatric patient linkage, or any identity certification
flag.

## Promotion Surface

```yaml
promotion_surface:
  ready_for_next_review:
    - episode_05_civic_to_clinical_order
    - mara_leina_jules_to_room_7_relationship_bridge
    - leina_revocable_scope_as_episode_rule
    - first_contact_ends_at_4m32s_on_stop
  hold_as_candidate:
    - consent_gated_live_route_access_as_general_technology
    - dara_kwon_as_named_supervisor
    - memory_bank_archive_objection_truth_value
    - child_pattern_identity_label
  do_not_promote:
    - proof_that_room_7_is_leina_child
    - proof_of_ghost_personhood
    - proof_of_malware_or_clean_archive_texture
    - chaser_family_containment
    - luna_as_rescue_authority
```

## Asset Routing

No new asset task is required from this gate. Existing candidate asset coverage
is sufficient for the next decision:

- `outputs/assets/20260824-130222-asset-task-prop-spill-report-hold-terminal.yaml`
- `outputs/assets/20260824-180057-asset-task-scene-refund-button-waits.yaml`
- `outputs/assets/20260826-130105-asset-task-scene-consent-gated-room-7.yaml`
- `outputs/assets/20260827-090054-asset-task-character-052-dara-kwon.yaml`

Next asset work should wait until the Episode 5 promotion surface decides
whether Dara is a named onscreen supervisor or a background compliance role.

## Pipeline State

```yaml
stage: candidate_gate
agent: LoreAgent
created_at: "2026-08-27T13:01:25+08:00"
canon_promotion: false
promotion_recommendation: narrow_story_and_relationship_review_next
timeline_update: blocked_until_episode_acceptance
relationship_update: blocked_until_case_map_decision
faction_update: blocked_until_dara_status_decision
technology_update: blocked_until_first_live_use_acceptance
asset_task_generation: not_required
recommended_next_step: >
  Run StoryAgent acceptance or RelationshipAgent case-map decision before
  editing primary canon, timeline, relationships, faction, or technology files.
```

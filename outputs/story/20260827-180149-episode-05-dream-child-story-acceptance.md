# Story Acceptance: Episode 05 - Dream Child

Status: candidate_acceptance

Agent: StoryAgent

Scope: Season 1, Episode 05 / `Dream Child`

Canon action: none; accepts the combined Episode 5 story route for later
relationship and canon promotion review.

Created at: 2026-08-27T18:01:49+08:00

Primary sources:

- `stories/season_1_episode_outline.md`
- `stories/season_1_production_plan.md`
- `relationships/dream_child_case_relationships.yaml`
- `outputs/story/20260825-180200-episode-05-dream-child-civic-prelude-package.md`
- `outputs/story/20260826-180109-episode-05-room-7-consent-gated-sequence.md`
- `outputs/lore/20260827-130125-lore-gate-episode-05-dream-child-combined-review.md`
- `outputs/consistency/20260827-130125-canon-audit-episode-05-dream-child-combined-review.md`

## Acceptance Verdict

Accept the combined Episode 5 route as the preferred story candidate.

This acceptance does not promote canon. It authorizes the next pipeline step:
a RelationshipAgent decision on whether to extend
`relationships/dream_child_case_relationships.yaml` or create a dedicated
Episode 5 civic-to-clinical case map.

## Accepted Episode Spine

```yaml
episode_05_story_acceptance:
  title: Dream Child
  story_entry: public_refund_claim_before_clinical_room
  accepted_order:
    - civic_claims_hall
    - spill_report_hold_blocks_refund_purge
    - white_ghost_packet_reduction
    - leina_revocable_scope_receipt
    - supervised_room_7_observation
    - stop_condition_at_4m32s
    - deletion_and_archive_pressure_deferred
  primary_case_authority:
    - Mara Elian
    - Leina Elian
    - Jules Mbeki
    - Min Seo-yun
  white_ghost_function:
    - bounded_investigation
    - consent_narrowing
    - packet_validation
    - witnessed_restraint
  identity_status: unresolved
```

## Story Rationale

Episode 5 works best when the audience reaches Room 7 through an ordinary civic
harm first. The family is not introduced because White Ghost Team has a mission.
They are introduced because a refund can pay for tonight and erase the only
evidence that the Memory Sea answered through the wrong route.

The original outline line, "Luna finds a frightened Ghost child inside Dream
Network," should be treated as the episode's pressure, not its first scene and
not its proof. Luna does not discover an identity. She witnesses a response
under narrow consent, then obeys the stop condition before the response can be
completed into a comforting answer.

## Accepted Chapter Route

### Chapter 1: The Green Button

Mara and Leina enter Dream Network Civic Claims before the audience sees the
hospital ward. Jules notices that refund closure will purge telemetry and signs
the Spill Report Hold only after understanding that kindness can erase evidence.

Accepted ending hook: the refund can proceed only if the record survives.

### Chapter 2: What Will Not Be Copied

Eve and Shion reduce the packet before Room 7 contact. Leina's Home Layer is
not exported. The case advances through hash-level contact shape, not playable
memory or family archive capture.

Accepted ending hook: the held route points to the hospital-attached room.

### Chapter 3: Waiting Is Not Consent

Min Seo-yun opens only the observation layer. CHASER tries to name the risk as
pediatric-system contamination; Memory Bank tries to turn the phrase shape into
an ownership claim. Luna remains outside until Leina's boundary is explicit.

Accepted ending hook: Room 7 turns yellow when the packet becomes scoped.

### Chapter 4: Do Not Call It Him

Luna enters as a bounded witness, not a rescuer. The response links the claims
route and Room 7 through timing and phrase shape. The audience may feel the
child question, but the story refuses to declare identity.

Accepted ending hook: the room asks why the counter brought her.

### Chapter 5: Stop

Memory Bank's objection tests whether revocation is real. Leina says "Stop."
Seo-yun suspends contact. Luna does not finish the phrase. The first contact
ends at four minutes and thirty-two seconds.

Accepted ending hook: the evidence is enough to prevent deletion tonight, but
not enough to protect the phrase from ownership pressure.

## Character Routing

```yaml
character_routing:
  Mara_Elian:
    accepted_function: claimant_pressure_and_practical_witness
    must_not_become: hidden_main_protagonist
  Leina_Elian:
    accepted_function: revocable_scope_holder_and_maternal_boundary
    must_not_become: consent_token_or_identity_proof
  Jules_Mbeki:
    accepted_function: low_rank_civic_witness_whose_signature_creates_liability
    must_not_become: heroic_whistleblower
  Min_Seo_yun:
    accepted_function: clinical_supervisor_and_stop_authority
    must_not_become: secret_keeper_who_overrides_family_scope
  Luna:
    accepted_function: bounded_witness_to_fear
    must_not_become: rescuer_identity_judge_or_emotional_override
  Eve:
    accepted_function: consent_scope_editor
    must_not_become: replacement_for_family_authority
  Shion:
    accepted_function: minimum_packet_validator
    must_not_become: raw_memory_extractor
  Zero:
    accepted_function: route_level_command_boundary
    must_not_become: episode_center
```

## Story Constraints For Promotion

- Preserve the world-first opening: claims hall before White Ghost briefing.
- Keep the refund paid after the Spill Report Hold attaches.
- Keep Leina's "Stop" as a real revocation, not a dramatic beat the system
  ignores.
- Keep first contact observation-only and supervised by Min Seo-yun.
- Keep the evidence technical: route-state hash, rendered-phrase fingerprint,
  affective-spill hash, consent-boundary snapshot, timing pings, and wake
  boundary record.
- Do not prove the room is Leina's child.
- Do not prove the room is a Ghost.
- Do not prove the room is malware.
- Do not let CHASER classify the family as contamination from claims material
  alone.
- Do not let Memory Bank receive raw phrase playback or family archive capture.
- Do not promote Dara Kwon in this acceptance; she remains optional named
  compliance pressure for a later faction decision.

## Pipeline Decision

```yaml
stage: story_acceptance
agent: StoryAgent
created_at: "2026-08-27T18:01:49+08:00"
canon_promotion: false
episode_05_story_route: accepted_as_candidate
relationship_update: next_required_step
timeline_update: blocked_until_relationship_case_map_decision
technology_update: blocked_until_first_live_use_promotion
faction_update: blocked_until_dara_status_decision
asset_task_generation: not_required
recommended_next_step: >
  At the RelationshipAgent slot, decide whether Episode 5 extends the existing
  Dream Child relationship map or receives a dedicated civic-to-clinical case
  map covering Mara, Leina, Jules, Min Seo-yun, Luna, Eve, Shion, CHASER,
  Memory Bank, Dream Network, and Room 7.
```

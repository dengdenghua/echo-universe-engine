# Character Boundary Sheet: Episode 05 Dream Child

Status: candidate_output

Agent: CharacterAgent

Scope: Season 1, Episode 05 / `Dream Child`

Canon action: none. This sheet supports the later full Episode 5 treatment by
locking character voice, authority, and consent limits after the promoted
civic-to-clinical relationship bridge.

Created at: 2026-08-28T09:01:38+08:00

Primary sources:

- `relationships/episode_05_dream_child_civic_to_clinical_relationships.yaml`
- `relationships/dream_child_case_relationships.yaml`
- `relationships/dream_network_civic_claims_relationships.yaml`
- `outputs/story/20260827-180149-episode-05-dream-child-story-acceptance.md`
- `outputs/story/20260826-180109-episode-05-room-7-consent-gated-sequence.md`
- `outputs/story/20260825-180200-episode-05-dream-child-civic-prelude-package.md`
- `outputs/character/20260825-090113-candidate-character-050-mara-elian.md`
- `outputs/character/20260826-090149-candidate-character-051-leina-elian.md`
- `outputs/character/20260824-090213-candidate-character-049-jules-mbeki.md`
- `outputs/character/20260827-090054-candidate-character-052-dara-kwon.md`

## CharacterAgent Decision

Prepare the Episode 5 treatment around civilian authority, not investigator
momentum.

The accepted story route already says that `Dream Child` begins at the claims
counter and reaches Room 7 only after scope reduction. This character sheet
makes that playable in scenes: Mara controls practical pressure, Leina controls
revocation, Jules controls the first paperwork delay, Min Seo-yun controls the
ward stop, and White Ghost Team can only act inside those boundaries.

Dara Kwon remains candidate-only. She may be used in draft dialogue as an
unnamed or bracketed compliance supervisor, but this sheet does not promote her
name into canon.

## Scene Authority Ladder

```yaml
episode_05_character_authority:
  first_scene_authority:
    holder: Mara_Elian
    surface: Dream_Network_Civic_Claims_counter
    authority: claimant_standing
    must_show: money_need_before_mystery
    must_not_show: White_Ghost_Team_opening_case_as_mission
  consent_authority:
    holder: Leina_Elian
    surface: Home_Layer_scope_receipt
    authority: revocable_maternal_scope
    must_show: "Stop means stop"
    must_not_show: silence_as_blanket_permission
  evidence_preservation_authority:
    holder: Jules_Mbeki
    surface: Spill_Report_Hold_receipt
    authority: claims_license_and_printed_hold
    must_show: refund_can_pay_and_preserve_record
    must_not_show: heroic_whistleblower_framing
  clinical_authority:
    holder: Min_Seo_yun
    surface: Room_7_observation_boundary
    authority: live_ward_suspension_and_wake_safety
    must_show: waiting_as_safety_not_consent
    must_not_show: hidden_doctor_overrides_family_scope
  investigative_authority:
    holder: White_Ghost_Team
    surface: reduced_packet_only
    authority: bounded_review
    must_show: restraint_as_competence
    must_not_show: rescue_before_permission
```

## Voice Locks

### Mara Elian

Mara speaks from counters, lunch lines, bills, and records. Her dialogue should
make abstract personhood arguments feel premature.

Usable sentence shapes:

- "How long does the money wait if the record stays?"
- "Do not make a refund into a broom."
- "My sister did not sign for all of us to become evidence."
- "If this is only a failed route, why does the room need to disappear first?"

Scene behavior:

- Counts costs in meals, transit, time off work, and delayed compensation.
- Corrects comfort language when it hides deletion.
- Defends Leina's silence without replacing it.
- Uses `room`, `route`, `record`, and `response` before any kinship term.

Forbidden use:

- Do not let Mara prove the child question.
- Do not make her the emotional spokesperson for Leina's private Home Layer.
- Do not convert her into a recurring investigator.

### Leina Elian

Leina speaks rarely, but each line should change the permission state of the
scene. She is not passive; she is the living boundary.

Usable sentence shapes:

- "Smaller."
- "The record can stay. The rhythm does not leave."
- "Not him. Not from your mouth."
- "Stop."

Scene behavior:

- Reads the scope receipt before looking at any face.
- Lets silence hold pressure; other characters should not fill it with
  conclusions.
- Corrects nouns rather than arguing theory.
- Protects one private Home Layer rhythm from all export.

Forbidden use:

- Do not make exhaustion equal consent.
- Do not let her `Stop` become a dramatic pause before contact continues.
- Do not let her accept full Home Layer export for plot convenience.

### Jules Mbeki

Jules is soft, exact, and visibly low-ranking. He should create liability by
following a narrow rule, not by becoming brave in a public speech.

Usable sentence shapes:

- "A refund closes the service record unless I hold the spill first."
- "This copy says what I preserved. It does not copy what you said."
- "I can delay the purge. I cannot tell you what the room is."
- "The green button pays you. It also cleans the file."

Scene behavior:

- Turns recorders away before asking for private language.
- Prints first, explains second.
- Avoids saying `Ghost` unless someone else forces the category.
- Shows fear through procedural precision.

Forbidden use:

- Do not let Jules certify Ghost personhood.
- Do not let him enter Room 7 or substitute for Min Seo-yun.
- Do not turn him into a heroic whistleblower.

### Min Seo-yun

Seo-yun's voice is clinical calm under moral pressure. She does not own the
case; she owns the wake boundary and the stop condition.

Usable sentence shapes:

- "Observation only."
- "Waiting is not consent."
- "The ward records suspension at four minutes thirty-two seconds."
- "No one names a live response from a claims packet."

Scene behavior:

- Places body-state, wake safety, and family scope above institutional urgency.
- Treats the child-pattern as sheltered without declaring identity.
- Requires Luna to accept boundaries before entry.
- Makes suspension visible on paper or analog ward log.

Forbidden use:

- Do not let Seo-yun secretly solve the identity question.
- Do not let clinical authority override Leina.
- Do not use Room 7 as a hidden dream realm.

### Luna

Luna is the dangerous empath because she wants to answer fear. In this episode,
her strongest character action is restraint.

Usable sentence shapes:

- "I can wait outside."
- "I will not finish the phrase."
- "I heard fear. I did not hear a name."
- "If she says stop, I leave before I understand."

Scene behavior:

- Asks fewer questions than she wants to ask.
- Lets Mara and Leina correct her language.
- Reports responsiveness, timing, and fear without identity.
- Leaves the phrase unfinished after revocation.

Forbidden use:

- Do not let Luna rescue the room.
- Do not let empathy override consent.
- Do not let her call the response a child as proof.

### Eve

Eve is the file-shrinking conscience. Her character beat is visible subtraction:
cross-outs, export removals, and fewer fields.

Usable sentence shapes:

- "This line copies too much."
- "We do not need the raw Home Layer to preserve the route."
- "Private grief is not a shortcut."
- "The smaller file is the more truthful one."

Scene behavior:

- Removes context enrichment before access is requested.
- Makes institutional language readable to civilians.
- Blocks Memory Bank from receiving raw phrase playback.
- Treats Leina's silence as an active instruction.

Forbidden use:

- Do not let Eve replace family authority.
- Do not let consent editing become technocratic comfort.
- Do not let her solve the scene by perfect wording alone.

### Shion

Shion gives negative findings weight. The episode needs him to say what the
packet cannot prove.

Usable sentence shapes:

- "Shape match. Not identity."
- "Enough to stop deletion. Not enough to name the response."
- "The hash preserves contact without preserving the family."
- "The absence is part of the finding."

Scene behavior:

- Holds confidence caps in plain language.
- Keeps route hashes separate from raw memory.
- Treats weak proof as protection against premature naming.
- Helps CHASER stay at route-level notice only.

Forbidden use:

- Do not let Shion extract raw memory.
- Do not let him turn timing pings into personhood proof.
- Do not let technical calm erase Mara and Leina's risk.

### Zero and Kane

Zero and Kane should remain peripheral pressure controls. Their restraint keeps
Episode 5 world-centric.

Usable sentence shapes:

- Zero: "Route-level notice only."
- Zero: "No family intake from this packet."
- Kane: "The corridor stays quiet."
- Kane: "No one moves the cart until the doctor signs."

Scene behavior:

- Zero prevents CHASER escalation from becoming family containment.
- Kane protects witnesses and choke points without spectacle.
- Neither character becomes the emotional center.

Forbidden use:

- Do not open the episode with White Ghost Team briefing.
- Do not let Zero turn the case into an ECHO awakening clue scene.
- Do not let Kane solve deletion pressure through force.

## Dara Kwon Use Gate

```yaml
dara_kwon_status_for_episode_05_draft:
  current_status: candidate_only
  allowed_in_candidate_treatment: true
  allowed_as_promoted_canon_name: false
  if_used:
    label: Dream_Network_compliance_supervisor
    dialogue_function: closure_pressure_and_context_enrichment
    first_reference: bracketed_or_unnamed_supervisor
    must_preserve:
      - cannot_enter_Room_7
      - cannot_delete_frozen_Spill_Report_Hold
      - cannot_override_Leina_revocation
      - cannot_prove_Memory_Bank_claim
      - cannot_become_secret_villain
  promotion_requirement: >
    Later LoreAgent or FactionAgent pass must decide whether Episode 5 needs a
    named Dream Network compliance supervisor in primary canon.
```

## Chapter-Specific Character Pressure

```yaml
chapter_pressure_map:
  chapter_1_green_button:
    center: Mara_Elian
    pressure: refund_needed_but_purge_threatens_record
    voice_test: "Mara asks what disappears when payment is instant."
    witness_shift: Jules_Mbeki_signs_hold_without_becoming_hero
  chapter_2_what_will_not_be_copied:
    center: Leina_Elian
    pressure: Home_Layer_privacy_vs_reduced_packet
    voice_test: "Leina makes the file smaller by withholding a rhythm."
    witness_shift: Eve_and_Shion_make_limits_visible
  chapter_3_waiting_is_not_consent:
    center: Min_Seo_yun
    pressure: ward_safety_vs_institutional_closure
    voice_test: "Seo-yun opens observation without granting identity."
    witness_shift: Luna_waits_until_permission_is_explicit
  chapter_4_do_not_call_it_him:
    center: Luna
    pressure: fear_response_vs_naming_temptation
    voice_test: "Luna reports fear and refuses identity language."
    witness_shift: Mara_and_Leina_keep_family_terms_out_of_proof
  chapter_5_stop:
    center: Leina_Elian
    pressure: ownership_objection_vs_real_revocation
    voice_test: "Stop ends contact before comfort arrives."
    witness_shift: the_packet_survives_without_claiming_the_child
```

## Treatment Guardrails

- Open on the claims hall, not White Ghost Team.
- Let money be real pressure before mystery language appears.
- Keep the Home Layer and Home Core private unless a narrow scope receipt
  permits hash-only comparison.
- Use Memory Sea, Home Layer, Home Core, Second Nervous System, Dream Network,
  and Room 7 as story-facing terms.
- Keep `Spill Report Hold Terminal` and route-hash language procedural.
- Do not use product-document language in prose.
- Do not turn Room 7 into a supernatural dream space.
- Do not prove the room is Leina's child, a Ghost, malware, or licensed
  archive texture.
- Let `Stop` end the live contact at four minutes and thirty-two seconds.
- Leave deletion and archive ownership pressure alive for later routing.

## Pipeline Position

```yaml
stage: character_candidate
agent: CharacterAgent
created_at: "2026-08-28T09:01:38+08:00"
canon_promotion: false
supports:
  - later_full_episode_05_treatment
  - Dara_status_decision
  - consent_boundary_dialogue
  - case_character_voice_continuity
blocked_promotions:
  - Dara_Kwon_named_supervisor
  - Consent_Gated_Live_Route_Access_general_technology
  - timeline_update
  - faction_update
asset_task_generation: not_required
recommended_next_step: >
  At the 13:00 LoreAgent/FactionAgent/TechnologyAgent slot, decide whether the
  Episode 5 full treatment should use Dara Kwon as the named Dream Network
  compliance supervisor or keep the pressure unnamed until after the treatment.
```

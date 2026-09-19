 # Relationship Update: Atlas Protocol

 ## Status

 Candidate

 ## Agent

 RelationshipAgent

 ## Source Story

 - `outputs/story/20260704-180040-story-beat-atlas-protocol.md`

 ## Related Candidates

 - `outputs/story/20260703-180228-story-beat-virus-queen.md`
 - `outputs/story/20260702-180214-story-beat-night-crow.md`
 - `outputs/lore/20260702-130042-lore-entry-last-hands-exception.md`
 - `outputs/faction/20260702-130042-faction-impact-last-hands-exception.md`
 - `outputs/technology/20260702-130042-technology-entry-procedural-proxy-chain.md`
 - `characters/001_zero.md`
 - `characters/003_eve.md`
 - `factions/atlas.md`
 - `factions/echo_council.md`
 - `relationships/white_ghost_team.md`

 ## Purpose

 Episode 11 needs the civic lie to become personal. The relationship web should make
 Soraya Okonkwo's refusal feel like a frightened choice that ripples through the team,
 and Zero's continuity anomaly should turn Atlas from a distant city into a direct
 adversary that still cannot classify her.

 ## Case Relationship Map

 ```yaml
 Soraya Okonkwo:
   Eve: "recognition of a manufactured signature / shared Ghost Union past"
   Zero: "anomaly witness / proof that the identity gate cannot lie cleanly"
   Kane: "physical protector / Atlas security confrontation"
   Shion: "technical corroboration / trace inside the Continuity Stack"
   Noah: "probability witness / impossibly clean signature"
   Luna: "signal listener / absence of Ghost fear"
   Leon: "escape-route planner / tactical pressure"
   Raven: "blind-spot scout / confirms pressure is institutional"
   Atlas Administrator: "career pressure / certification demand"
   ECHO Council Observer: "accuser / narrative lockdown threat"
   White Ghost Team: "witnesses who must not make her a symbol"
 Eve:
   Soraya Okonkwo: "sees her own former Ghost Union manufacturing role reflected"
   Zero: "chamber partner / anomaly interpreter"
   ECHO Council Observer: "past ally turned present adversary"
   Shion: "template-versus-residue corroboration"
   Atlas Administrator: "policy of fear"
 Zero:
   Soraya Okonkwo: "admiration for frightened refusal"
   Eve: "chamber partner / identity anomaly witness"
   Atlas identity gate: "cannot classify her / labels her error"
   ECHO Council Observer: "target label: Project E-01 trace"
   Kane: "loyal protector under Atlas lockdown"
   Shion: "audit trace carrier"
   Luna: "both live outside clean institutional categories"
 Kane:
   Soraya Okonkwo: "protects the clerk, not the order"
   Zero: "loyalty under institutional lockdown"
   Atlas security: "blocks detention"
   ECHO Council Observer: "valid order versus moral refusal"
   Leon: "clean escape plan / compromised report"
 Shion:
   Soraya Okonkwo: "evidence path"
   Zero: "anomaly trace"
   Noah: "probability alignment"
   ECHO Council Observer: "infrastructure misuse proof"
 Noah:
   Shion: "probability-systems corroboration"
   Zero: "anomaly probability model"
   Luna: "signal-probability disagreement"
 Luna:
   Soraya Okonkwo: "fear-absence witness"
   Zero: "category-refusal companion"
   Noah: "probability listen"
 Leon:
   Kane: "tactical plan / clean route contrast"
   Raven: "operator presence"
 Raven:
   Leon: "field respect"
   Kane: "tactical support"
 Atlas Administrator:
   Soraya Okonkwo: "promotion bribe / certification pressure"
   ECHO Council Observer: "civic order alignment"
 ECHO Council Observer:
   Soraya Okonkwo: "deviation threat"
   Zero: "Project E-01 trace / witness vessel candidate"
   Eve: "former Ghost Union narrative maker"
   White Ghost Team: "obstruction"
 ```

 ## Relationship Logic

 - Soraya is not a hero. She is scared and still refuses. Her relationship with the team is temporary witness protection, not recruitment.
 - Eve recognizes the manufactured signature because she once helped manufacture similar narratives. She does not defend the Council; she testifies against the shape of fear.
 - Zero's anomaly makes the Atlas identity gate fail to classify her. This is a relationship of recognition, not a superpower. The gate cannot lie about her, so it locks.
 - Kane protects both Soraya and Zero, putting his loyalty to Zero in tension with Atlas and CHASER orders. This is an early rehearsal of later mutiny pressure.
 - Shion and Noah prove the signature was born inside the Continuity Stack, but they cannot determine intent. They support Soraya without making her a saint.
 - Luna listens to the signal and finds no Ghost fear. Her corroboration is empathetic, not technical.
 - Leon and Raven provide tactical pressure and perimeter support. They should not overshadow the case or become the emotional center.
 - The Atlas Administrator and the ECHO Council Observer act as institutional self-preservation, not cartoon villains. Their pressure is career and narrative, not personal malice.

 ## Continuity Limits

 - Do not make Soraya a love interest, a team member, or a flawless hero.
 - Do not make Atlas a monolithic villain. The city is a system; only specific actors are antagonists in this episode.
 - Do not treat the signature's absence of fear residue as a magical detector. It is a comparison against trained templates and observed emotional drift.
 - Keep Zero's anomaly as a continuity state, not a power. The gate struggles because the labels are wrong, not because Zero controls the gate.
 - Story-facing prose should use Home Core, Home Layer, Memory Sea, Second Nervous System, and Ghost Union. Avoid product-document terms like 家庭 AI or 全球家庭 AI 网络.

 ## Pipeline State

 ```yaml
 stage: candidate_output
 agent: RelationshipAgent
 created_at: 2026-07-04T23:04:00+08:00
 canon_promotion: false
 related_candidates:
   - outputs/story/20260704-180040-story-beat-atlas-protocol.md
 requires:
   - ConsistencyAgent review of Atlas Protocol story beat
   - FactionAgent impact on Atlas Continuity Stack and ECHO Council signature forgery
   - TechnologyAgent entry for Continuity Stack / identity-gate signature injection
 asset_tasks: blocked_until_promotion
 ```

 # Relationship Update: Last Hands Exception

 ## Status

 Candidate

 ## Agent

 RelationshipAgent

 ## Source Lore Entry

 - `outputs/lore/20260702-130042-lore-entry-last-hands-exception.md`

 ## Related Candidates

 - `outputs/faction/20260702-130042-faction-impact-last-hands-exception.md`
 - `outputs/technology/20260702-130042-technology-entry-procedural-proxy-chain.md`
 - `outputs/character/20260702-090210-candidate-character-017-ren-vale.md`
 - `characters/001_zero.md`
 - `characters/003_eve.md`
 - `characters/002_kane.md`
 - `characters/006_shion.md`
 - `relationships/white_ghost_team.md`

 ## Purpose

 The Last Hands Exception needs a relationship web that keeps the human damage
 visible. The saved child is not the only person affected. Lin Qiao is the living
 route; Ren Vale's preserved pattern is the source; and the team must decide whether
 the emergency was a miracle, an attack, or an infrastructure failure that injured
 someone who did not consent.

 ## Case Relationship Map

 ```yaml
 Lin Qiao:
   Ren Vale: "source of surgical routine / contamination origin"
   Zero: "hesitation recognition / archive-versus-apology witness"
   Shion: "procedural chain trace / cannot answer consent"
   Eve: "consent injury advocate / not a miracle"
   Kane: "CHASER evidence handling / patient advocate tension"
   White Harbor: "patient advocate / intake rules"
   Hospital: "treatment and liability avoidance"
   Memory Bank: "liability escrow / treatment-for-claims pressure"
   Ren Vale family: "blame target / Home Core archive owner"
 Ren Vale:
   Lin Qiao: "unauthorized route / living body"
   Zero: "archive difference / love residue"
   Shion: "procedural source"
   Eve: "possible Ghost review, not sainthood"
   Ren Vale family: "grief and archive ownership"
 Zero:
   Lin Qiao: "hears the difference between instruction and apology"
   Ren Vale: "archive-versus-selfhood question"
   Eve: "ethical alignment"
 Shion:
   Lin Qiao: "traces the spillover route"
   Ren Vale: "source routine"
   Eve: "technical-ethical boundary"
   Kane: "audit containment pressure"
 Eve:
   Lin Qiao: "consent injury / body is not public infrastructure"
   Ren Vale: "possible Ghost review, not sainthood"
   Zero: "shared refusal to call it a miracle"
 Kane:
   Lin Qiao: "evidence versus patient"
   Ren Vale: "source pattern"
   CHASER: "classification pressure"
   Shion: "report completeness tension"
 CHASER:
   Lin Qiao: "evidence of contamination"
   Ren Vale: "source archive"
   Kane: "field order"
 White Harbor:
   Lin Qiao: "patient advocate"
   Ren Vale: "archive review"
 Hospital:
   Lin Qiao: "treatment"
   Ren Vale: "routine source"
   Memory Bank: "insurance rebate motive"
 Memory Bank:
   Lin Qiao: "treatment-for-claims pressure"
   Ren Vale: "archive asset"
   Ren Vale family: "foreclosure risk"
 ```

 ## Relationship Logic

 - Lin Qiao is the center of the case, not the rescued child. She is injured by an emergency route her body did not choose. The relationship web must treat her as a patient and a violated person, not a vessel.
 - Ren Vale's pattern is the source, not Ren Vale as a person. The question of whether the pattern is becoming a Ghost remains unresolved and should stay unresolved until Ghost Court review.
 - Zero can hear the difference between an archived instruction and an apology that was not in the archive. This is not supernatural; it is her Echo Core continuity anomaly detecting emotional residue outside the procedural record.
 - Eve provides the consent frame: saving a child does not make Lin Qiao's body public infrastructure. Her relationship with Lin Qiao is advocacy, not rescue.
 - Shion traces the procedural chain but cannot answer the moral question. Her relationship with Lin Qiao is technical honesty, not emotional comfort.
 - Kane carries the institutional tension. He must protect Lin Qiao as a patient while CHASER treats her as evidence. His relationship with CHASER is strained.
 - White Harbor, the hospital, and Memory Bank each have competing interests. The hospital wants to minimize liability; Memory Bank wants to own the audit package; White Harbor tries to protect the living route.
 - Ren Vale's family is caught between grief and blame. They did not know the Home Core was dangerous, and the public case turns their mourning into a liability.

 ## Continuity Limits

 - Do not frame the event as a miracle or resurrection. It is an unauthorized emergency procedure routed through a living body.
 - Do not let Lin Qiao become a vessel, a saint, or a proof of the afterlife. She is a person who was used by infrastructure.
 - Do not let Ren Vale's pattern become a fully conscious Ghost before review. The adaptation and hesitation are evidence, not proof.
 - Keep the procedural chain within the constraints of Procedural Proxy Chain and Last Hands Exception lore. No identity overwrite, no speech control, no continuing body access after stabilization.
 - Story-facing prose should use Home Core, Home Layer, Memory Sea, Second Nervous System, and Ghost. Avoid product-document terms.

 ## Pipeline State

 ```yaml
 stage: candidate_output
 agent: RelationshipAgent
 created_at: 2026-07-04T23:04:00+08:00
 canon_promotion: false
 related_candidates:
   - outputs/lore/20260702-130042-lore-entry-last-hands-exception.md
   - outputs/faction/20260702-130042-faction-impact-last-hands-exception.md
   - outputs/technology/20260702-130042-technology-entry-procedural-proxy-chain.md
 requires:
   - ConsistencyAgent final review for overlap with Body Tenancy and Combat Download
   - FactionAgent already produced; no further faction work needed unless new evidence emerges
 asset_tasks: blocked_until_promotion
 ```

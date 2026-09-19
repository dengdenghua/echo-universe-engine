# Canon Audit: Threshold Notice Window Packet

```yaml
status: accepted_as_candidate
canon_promotion: false
reviewed_candidates:
  - outputs/lore/20260717-130233-lore-entry-threshold-notice-window.md
  - outputs/technology/20260717-130233-technology-entry-threshold-receipt-packet.md
  - outputs/faction/20260717-130233-faction-impact-threshold-notice-window.md
agent: LoreAgent + TechnologyAgent + FactionAgent + ConsistencyAgent
created_at: "2026-07-17T13:02:33+08:00"
```

## Duplicate Check

- Not a duplicate of Emergency Delay Window: that candidate pauses automated
  civil harm involving custody, clinic, school, care, or identity edges.
  Threshold Notice Window governs pre-entry warning at a home threshold during
  live CHASER, evacuation, medical, or infrastructure incidents.
- Not a duplicate of Analog Presence Review: that candidate requires a witness
  before irreversible Home Layer change. Threshold notice records what was said
  before the door opened, the home was muted, or evacuation was forced.
- Not a duplicate of Witness Seal or Presence Integrity Packet: those protect
  testimony or witness events. Threshold Receipt Packet captures a warning
  exchange, response route, and command override context.
- Extends Juno Park without promoting her: Juno remains a character candidate,
  while the procedure can be reused by other civil-warning officers.

## Canon Compatibility

- Fits `bible/chaser_organization.md`: CHASER must protect civilians quickly,
  preserve evidence, distinguish threat from personhood, and respect Ghost
  Court limits.
- Fits `factions/chaser.md`: CHASER remains protective and compromised rather
  than simple hero authority.
- Fits `bible/personhood_and_identity.md`: a Home Core answer can matter as
  evidence without proving Ghost selfhood.
- Supports world-centric Season 1 because the scene begins with the household,
  warning desk, corridor, and social trust problem before White Ghost Team
  intervenes.

## Ability Constraint Review

Threshold Notice Window is procedure, not a special power.

- Mechanism: warning scripts, acknowledgment hashes, building access systems,
  Home Core routing, Home Layer speakers, CHASER amber-entry queues, evacuation
  graphs, command signatures, Ghost Court audit rails, and scoped receipt
  packets.
- Activation: pre-containment or amber-entry incident where notice can be
  delivered without unacceptable public-safety loss.
- Cost: delay may increase spread, panic, neighbor risk, evidence erasure, or
  operator liability.
- Failure mode: forged calm response, jamming, resident incapacity, command
  override, or liability theater.
- Countermeasure: integrity checks, command signatures, Shion-level review,
  analog notes, scoped packet limits, and honest failed-notice flags.
- Story limitation: the notice can buy minutes and expose contradictions. It
  cannot decide personhood, stop hard containment, or make entry harmless.

## Terminology Review

Approved story-facing terms are used:

- Home Core
- Home Layer
- Memory Sea
- Second Nervous System
- 家园核心
- 家园层
- 记忆海
- 第二神经系统
- Ghost

The packet avoids banned product-document terminology in prose.

## Risks

- Do not let Threshold Notice Window become a universal veto over CHASER entry.
- Do not let a door receipt equal consent; it is an audit artifact, not moral
  permission.
- Do not make every Home Core answer personhood. Keep witness evidence and
  selfhood separate.
- Do not make CHASER command cartoonishly cruel; urgency, liability, fear, and
  public safety all need to remain legible.
- Do not duplicate Sofia Marin's Emergency Delay Window or Marta Reyes's
  dead-home clearance lane.

## Promotion Recommendation

Keep as candidate. Promote only if an early Season 1 bridge case uses Juno Park,
a forged Home Core acknowledgment, or a CHASER entry hearing where the door
receipt changes what the public believes happened.

## Downstream Routing

```yaml
next_episode_use:
  recommended: true
  route: early_season_1_bridge_case
  premise: >
    A warning receipt says a family acknowledged evacuation, but Juno Park,
    Shion, and Zero each notice a different contradiction in the home response.
timeline_update:
  status: suggested_if_promoted
relationship_update:
  status: suggested_if_story_used
  targets:
    - Juno Park / Kane: delay versus physical safety
    - Juno Park / Shion: acknowledgment-integrity dependence
    - Juno Park / Zero: personhood pressure at the door
faction_update:
  status: candidate_output_created
asset_tasks:
  status: blocked_until_promotion
```

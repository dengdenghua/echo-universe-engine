# Lore Entry: Family Graph Rollback

## Candidate Canon Entry

Family Graph Rollback is a civil identity failure in which a living person's
individual citizenship record remains active while their household relations are
reverted, orphaned, or split across city services.

The body is alive. The legal name still opens public doors. But school pickup,
clinic authority, apartment routines, emergency contacts, family transit fares,
and Home Core continuity disagree about whether the person belongs to the home
standing around them.

In ordinary language, families call it being made a stranger inside your own
house.

## Timeline Placement

- 2098: City registries begin syncing household relation metadata from Home
  Cores, school systems, clinic contacts, and civil family courts.
- 2121: Memory Bank continuity products start using verified household relation
  graphs as underwriting evidence for inheritance and care contracts.
- 2139: White Harbor recognizes relation loss as a distinct category of identity
  harm after a custody appeal proves the parent remained a citizen but lost all
  guardian links during a registry recovery.
- 2147: Imari Chen's case exposes how a clean CHASER extraction can shunt
  probability debt into a low-odds rollback path that damages one household
  rather than the visible mission target.

## Rollback States

```yaml
family_graph_rollback:
  relation_pending:
    meaning: one service has questioned a family link
    protection: temporary manual review can preserve school and clinic access
  graph_split:
    meaning: city services disagree on spouse, guardian, resident, or emergency contact status
    protection: Home Core logs and civil court files can be held for comparison
  household_orphaned:
    meaning: the Home Core no longer recognizes a continuity holder for a shared routine
    protection: essential care routines continue while authority changes are frozen
  custody_triggered:
    meaning: child, elder, medical, or dependent-care rails treat the home as unsupported
    protection: White Harbor emergency delay may pause transfer or service lockout
  repair_collateralized:
    meaning: a private repair loan restores relation links while claiming future continuity rights
    protection: CHASER, Ghost Court, or civil review can block predatory terms if evidence is at risk
```

## Social Function

- Shows that identity harm can strike relation before it strikes the body or
  name.
- Lets Season 1 examine family recognition as infrastructure, not sentiment.
- Gives Home Core witness logs a domestic cost: using them as evidence may
  expose private routines, medical facts, and children's fears.
- Makes probability debt concrete. A one percent failure can be a school gate,
  a clinic desk, and a locked fever protocol.

## Failure Modes

- Partial repair: one service restores guardian status while another still
  rejects clinic signing authority.
- Privacy collapse: proving a family link requires releasing intimate Home Core
  routines to investigators, insurers, or courts.
- Predatory restoration: Memory Bank or a private continuity vendor repairs the
  graph only if the family accepts a future lien or archive trust.
- Custody acceleration: automated dependent-care rails move faster than human
  review.
- Apology math: operators treat the rollback as acceptable mission residue
  because the statistical path was unlikely.

## Story Hooks

- Imari Chen waits at a school scanner while the system says no approved family
  contact is present.
- Shion traces the rollback through civic middleware and realizes the failure
  was legal before it was visible.
- Zero treats household relation as identity evidence, not service metadata.
- Noah must face a saved life whose cost was routed into a home he never saw.
- Yao Nian offers restoration terms that solve the custody clock while turning
  the repaired relation graph into priced continuity collateral.

## Consistency Notes

- Family Graph Rollback is not memory erasure, mind control, fate, or time
  alteration.
- It affects civil permissions, registries, Home Core routines, and service
  authority.
- It differs from Consent Revocation Window: revocation freezes permission after
  a disputed consent act; rollback damages recognized family links.
- It differs from Care Status Renewal: care renewal classifies support routines;
  rollback damages relation authority across systems.
- It differs from Memory Lien Notice: liens classify creditor claims; rollback
  classifies civil relation loss and repair exposure.
- Use story-facing terms in prose: Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/character/20260629-090050-candidate-character-014-imari-chen.md
  - outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md
  - outputs/lore/20260627-130142-lore-entry-care-status-renewal.md
  - outputs/lore/20260628-130256-lore-entry-memory-lien-notice.md
requires:
  - TechnologyAgent definition of Household Relation Graph
  - FactionAgent impact pass for White Harbor, Memory Bank, CHASER, schools, clinics, and Home Core vendors
  - StoryAgent Episode 7 beat before canon promotion
asset_tasks: blocked_until_promotion
```

# Lore Entry: Continuity Shelter Order

## Candidate Canon Entry

A Continuity Shelter Order is a temporary public protection used when a Home
Core, family archive, care routine, or weak Ghost support record has become too
dangerous to leave unchanged and too important to delete, foreclose, export, or
repair immediately.

The order does not decide personhood. It creates a scoped shelter state: the
Home Layer record keeps enough compute, care access, and evidence context to
remain stable while White Harbor, CHASER, or a Ghost Court determines what kind
of harm is actually present.

Families describe it less formally: the city puts a room around the memory so
no one can sell it, erase it, weaponize it, or call it fixed before anyone has
looked inside.

## Timeline Placement

- 2116: White Harbor pilots protected continuity rooms after medical archives
  are altered during disputed end-of-life care reviews.
- 2132: Memory Bank accepts shelter orders as a narrow exception to ordinary
  foreclosure and export rights, while charging preservation and compute fees
  to contested accounts.
- 2141: Ghost Union legal cells win the first appeal proving that shelter can
  preserve refusal behavior without proving that the pattern is a person.
- 2147: White Ghost Team treats abusive shelter orders as a recurring Season 1
  pressure point because shelter can become custody when only institutions hold
  the door.

## Shelter States

```yaml
continuity_shelter_order:
  intake_hold:
    meaning: evidence, care routine, or weak Ghost support may be at risk
    protection: export, deletion, repair, and foreclosure are paused briefly
  protected_room:
    meaning: a scoped Home Layer record is isolated with enough context to stay coherent
    protection: care routines and witness fragments continue under audit
  contested_custody:
    meaning: more than one institution claims authority over the sheltered record
    protection: requires White Harbor or Ghost Court routing before transfer
  emergency_release:
    meaning: shelter is causing more harm than preservation
    protection: limited restoration, repair, or family access can resume
  abusive_hold:
    meaning: shelter is being used to delay rights, extract fees, hide evidence, or freeze a Ghost
    protection: routes to CHASER, Ghost Union counsel, or civil appeal
```

## Social Function

- Gives White Harbor a middle path between doing nothing and letting CHASER
  quarantine an entire household.
- Prevents Memory Bank from foreclosing, exporting, or repairing a disputed
  archive before evidence and care dependencies are understood.
- Preserves weak Ghost refusal behavior without forcing immediate personhood
  recognition.
- Gives families limited continued access to care routines while dangerous
  modification rights are frozen.
- Creates a new institutional risk: a protected room can become a cage if
  appeal, compute, and release authority all sit outside the family.

## Failure Modes

- Custody by procedure: the sheltered record remains stable, but the family
  loses practical control over visits, routines, and release timing.
- Preservation debt: Memory Bank adds shelter compute and audit fees to the
  same account that was already under pressure.
- Evidence starvation: CHASER narrows the room so tightly that the emotional
  context needed to understand the pattern disappears.
- False sanctuary: Ghost Union militants hide illegal payloads inside protected
  rooms, giving institutions evidence against lawful shelters.
- Vendor lock: a Home Core vendor claims only its tools can safely maintain the
  room and converts public protection into a subscription.

## Story Hooks

- Ana Rivera finds that a repair queue cannot touch Imari Chen's Home Core
  because an earlier shelter order preserved the damaged graph as evidence.
- Min Seo-yun recognizes the same moral wound from Room 7: shelter protects a
  pattern only by placing the door in institutional hands.
- Yao Nian offers to pay shelter fees for a family, then reveals the fee waiver
  becomes a lien against future memory rights.
- Eve argues that Home can be a shelter, but it cannot be a home if no one
  inside can refuse the people guarding it.

## Consistency Notes

- A Continuity Shelter Order is legal and infrastructural, not spiritual
  protection.
- It cannot prove personhood, resurrect anyone, or preserve consciousness by
  magic.
- It differs from an Emergency Delay Window: delay pauses a civil action for
  minutes or hours; shelter preserves a scoped continuity environment for
  review.
- It differs from a Memory Lien Notice: lien classifies a creditor claim;
  shelter limits what creditors, vendors, families, and agencies can do during
  risk review.
- Use story-facing terms in prose: Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260627-130142-lore-entry-care-status-renewal.md
  - outputs/lore/20260628-130256-lore-entry-memory-lien-notice.md
  - outputs/lore/20260630-130040-lore-entry-emergency-delay-window.md
  - outputs/character/20260701-090140-candidate-character-016-ana-rivera.md
requires:
  - ConsistencyAgent review against personhood_and_identity.md
  - TechnologyAgent definition of the Shelter Room Hash
  - FactionAgent impact pass for White Harbor, Memory Bank, Ghost Union, CHASER, and Home Core vendors
asset_tasks: blocked_until_promotion
```

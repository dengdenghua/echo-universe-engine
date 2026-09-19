# Lore Entry: Emergency Delay Window

## Candidate Canon Entry

An Emergency Delay Window is the short civil interval in which White Harbor may
pause an automated harm path before the city converts a disputed identity or
relation edge into custody transfer, clinic lockout, school denial escalation,
elder-care removal, or Home Core routine freeze.

It is not restoration. It is the civic act of making a machine wait while
humans prove which part of the Second Nervous System is contradicting itself.

Families call it borrowed time.

## Timeline Placement

- 2098: Household relation metadata begins feeding school, clinic, and domestic
  care systems.
- 2139: White Harbor's dependency desks receive emergency pause authority after
  a custody appeal proves an automated transfer moved faster than identity
  review.
- 2144: Civil insurers begin pricing delay liability into municipal operator
  records, making every manual pause a personal risk event.
- 2147: Sofia Marin's intervention in Imari Chen's Family Graph Rollback case
  exposes the difference between preventing an irreversible transfer and
  repairing a damaged family graph.

## Window States

```yaml
emergency_delay_window:
  threshold_warning:
    meaning: a service has detected contradictory relation or care evidence
    protection: operator review may begin, but no civil pause exists yet
  delay_eligible:
    meaning: a dependent-care action would cause near-term harm if automated
    protection: a named operator may issue a time-limited Civil Delay Token
  active_delay:
    meaning: custody, lockout, transfer, or denial escalation is paused
    protection: scoped evidence comparison can run under audit
  evidence_narrowing:
    meaning: review determines which logs are needed and which private routines stay sealed
    protection: Home Core exposure is limited to the disputed edge
  expiry_pressure:
    meaning: the delay timer is close to lapse without restoration
    protection: escalation to court, CHASER hold, or White Harbor supervisor review
  failed_delay:
    meaning: the pause expires or is overridden before relation repair
    protection: appeal record remains, but the automated action may proceed
```

## Social Function

- Gives White Harbor a precise civic tool: it can create time, not justice.
- Shows why families may accept predatory Memory Bank repair when public delay
  cannot restore records quickly enough.
- Makes privacy exposure concrete. A delay can protect a child without opening
  every Home Core routine to investigators.
- Gives Episode 7 a timer that is legal and emotional rather than combat-based.

## Failure Modes

- Liability chill: operators refuse borderline delays because one harmful pause
  can damage their license, pension score, or criminal exposure.
- Evidence overreach: agencies request full Home Core exports when only one
  relation edge is disputed.
- Repair capture: private vendors wait for expiry pressure, then offer fast
  restoration with continuity collateral.
- False safety: a family mistakes delay for restored authority and misses the
  next deadline.
- CHASER friction: preserving the damaged graph as evidence can keep a family
  inside the delay window longer than they can tolerate.

## Story Hooks

- Sofia Marin signs a twelve-minute delay while the school gate still labels
  Imari Chen as a rejected contact.
- Kane holds the physical line at the custody van while Sofia holds the
  procedural line in White Harbor's system.
- Shion requests only the Home Core routine fragments tied to guardian
  authority, refusing a full domestic export.
- Yao Nian arrives exactly when the delay enters expiry pressure and offers a
  repair that would work before morning.

## Consistency Notes

- An Emergency Delay Window does not rewrite records, prove personhood, restore
  relation edges, or forgive operational harm.
- It affects civil clocks, custody rails, school escalations, clinic lockouts,
  and Home Core routine freezes.
- It differs from Consent Revocation Window: revocation freezes permission
  after disputed consent; delay pauses automated dependent-care harm before
  review.
- It differs from Family Graph Rollback: rollback is the identity failure;
  delay is a temporary response to the failure.
- Use story-facing terms in prose: Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/character/20260630-090234-candidate-character-015-sofia-marin.md
  - outputs/lore/20260629-130142-lore-entry-family-graph-rollback.md
  - outputs/story/20260629-180031-story-beat-probability-debt.md
requires:
  - TechnologyAgent definition of Civil Delay Token
  - FactionAgent impact pass for White Harbor, Memory Bank, CHASER, schools, clinics, and Home Core vendors
  - ConsistencyAgent check against Consent Revocation Window and White Harbor authority
asset_tasks: blocked_until_promotion
```

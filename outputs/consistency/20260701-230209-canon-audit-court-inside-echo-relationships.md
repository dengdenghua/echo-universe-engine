# Canon Audit: The Court Inside ECHO Relationships

Status: candidate consistency check

Reviewed output:

- `outputs/relationship/20260701-230209-relationship-update-court-inside-echo.md`

Source context:

- `outputs/story/20260701-180040-story-beat-the-court-inside-echo.md`
- `outputs/consistency/20260701-180040-canon-audit-the-court-inside-echo.md`

## Verdict

Pass as candidate output. Do not promote yet.

The relationship update satisfies the previous consistency audit's required
next step by adding temporary pressure edges among Zero, Ana Rivera, Shion,
Noah, Imari Chen, Yao Nian, Ghost Court, White Harbor, and Memory Bank. It does
not edit promoted relationship canon and keeps the Episode 8 relationship logic
case-scoped until canon promotion.

## Duplicate Check

No exact duplicate found in promoted relationship canon.

Nearby relationship candidates:

- `outputs/relationship/20260629-230143-relationship-update-probability-debt.md`
  covers the original Household Relation Graph rollback and Noah's named
  probability debt.
- `outputs/relationship/20260630-230152-relationship-update-emergency-delay-window.md`
  covers public delay, school-gate protection, and Sofia Marin's operator risk.

This candidate remains distinct because its center is a Ghost Court partial
release hearing where valid protection becomes lived custody and Zero's
continuity anomaly becomes restricted evidence.

## Rule Check

- No magic: pass. Ghost Court is treated as projection, evidence interface, and
  arbitration infrastructure.
- No supernatural powers: pass. Relationship pressure comes from licenses,
  hashes, testimony, court authority, Home Layer locks, and Memory Bank fees.
- No multiverse or time travel: pass. The update uses preserved damaged edges
  and append-only witness evidence, not temporal access.
- World-centric rule: pass. Imari's family remains the wound; Ana is the repair
  witness; White Ghost Team acts as investigators and pressure points.
- Terminology: pass. The update uses Home Core, Home Layer, ECHO, and Memory
  Bank language without story-facing product-document terms.

## Canon Risks

- Zero's Project E-01 trace must remain partial and restricted. Do not let this
  relationship web answer his origin question before Episodes 13-16.
- Ana should not absorb Sofia Marin's role from the Emergency Delay Window.
  Sofia buys civic time; Ana scopes and performs supervised repair after court
  release.
- Ghost Court should not become a general solution machine. It can authorize a
  narrow partial release while preserving the damaged edge, but it cannot settle
  full personhood, repair public trust, or eliminate Memory Bank pressure.
- Imari's family should not become a recurring dependency for every later
  episode. Their case can be cited as precedent, but the emotional center of
  future cases should remain case-specific.

## Promotion Requirements

Before promotion:

- TimelineAgent should place Episode 8 after Probability Debt and before Night
  Crow.
- FactionAgent should decide whether Ghost Union legal cells react publicly to
  the partial release ruling.
- TechnologyAgent should decide whether "Project E-01 trace" remains plain
  evidence language or receives a restricted technical term.
- RelationshipAgent should only merge durable pressure edges into
  `relationships/relationships.yaml` if Episode 8 is promoted.

## Pipeline State

```yaml
stage: consistency_check
canon_promotion: false
reviewed:
  - outputs/relationship/20260701-230209-relationship-update-court-inside-echo.md
result: pass_candidate
recommended_next_step: timeline_or_faction_routing
asset_tasks: blocked_until_promotion
```

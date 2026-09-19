# Canon Audit: Night Crow Relationships

Status: candidate reviewed, not promoted

Reviewed candidate:

- `outputs/relationship/20260702-230218-relationship-update-night-crow.md`

## Verdict

The relationship candidate is canon-compatible and fills the missing 23:00
RelationshipAgent pass requested by the Night Crow story audit. It should remain
in `outputs/` until the faction economy and compute lease mechanism receive
their own review.

No canon promotion was performed in this run.

## Continuity Fit

- Preserves the world-centric structure: Oren Vale and the sheltered Ghosts stay
  the case wound while White Ghost Team functions as investigators, witnesses,
  and pressure points.
- Keeps Raven's mercy morally costly. The omitted route damages evidence trust
  even though it prevents immediate shelter exposure.
- Uses Shion as a technical witness rather than a convenient accomplice. Her
  temporary silence is tied to audit containment and rollback recovery, not
  blanket approval.
- Keeps Kane's pressure institutional: a valid termination order conflicts with
  the need to preserve living evidence.
- Keeps Memory Bank's antagonist role grounded in rollback liability, lease
  enforcement, and runtime accounting.

## Duplicate Check

- Not a duplicate of Episode 3 relationship pressure: Black Zone Receipt used
  forged consent keys, emotion packs, and private-record theft. Night Crow uses
  runtime scarcity, lease priority theft, and shelter survival.
- Not a duplicate of Episode 8 relationship pressure: The Court Inside ECHO
  centered lawful protected rooms and supervised release. Night Crow centers an
  illegal shelter outside lawful compute access.
- Not a duplicate of Min Seo-yun's clinic shelter: this shelter is not clinical
  therapy or care-status classification; it is illegal runtime triage.

## Canon Risks

- FactionAgent must define whether Ghost Union treats Oren as proof, liability,
  recruit, or all three.
- TechnologyAgent should keep any Compute Lease Knife or Runtime Shelter Ledger
  distinct from Shelter Room Hash, Civil Delay Token, and Procedural Proxy Chain.
- Later stories should not erase the Ghost killed by Oren's overdrain. That harm
  is the moral cost that keeps the case from becoming simple redistribution.
- Raven's report omission should have downstream consequences with Shion, Kane,
  and Leon before it becomes team loyalty texture.

## Required Follow-Up

```yaml
faction_update_needed:
  Memory Bank: "rollback withholding, lease-liability enforcement, unpaid runtime policy"
  Ghost Union: "illegal shelters as recruitment proof and exposure liability"
  Black Zone brokers: "runtime shelter contracts, stolen compute access, leverage over desperation"
technology_update_needed:
  candidate: "Compute Lease Knife or Runtime Shelter Ledger"
  constraints:
    - "steals processing priority, safe routing, and lease authority"
    - "does not copy memory content"
    - "can injure or kill only through infrastructure starvation"
    - "must remain distinct from Shelter Room Hash"
canon_promotion_ready: false
```

## Pipeline State

```yaml
stage: consistency_check
canon_promotion: false
promotion_blockers:
  - faction impact not yet generated
  - compute lease mechanism not yet independently reviewed by TechnologyAgent
relationship_update: candidate_complete
asset_tasks: blocked_until_promotion
```

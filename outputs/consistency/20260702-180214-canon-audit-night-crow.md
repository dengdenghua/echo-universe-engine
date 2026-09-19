# Canon Audit: Night Crow

Status: candidate reviewed, not promoted

Reviewed candidate:

- `outputs/story/20260702-180214-story-beat-night-crow.md`

## Verdict

The candidate is canon-compatible as a Season 1 Episode 9 story beat, but should
remain in `outputs/` until RelationshipAgent and FactionAgent passes update the
Raven/Shion/Kane pressure and the Memory Bank/Ghost Union/Black Zone shelter
economy.

No canon promotion was performed in this run.

## Continuity Fit

- Matches the Season 1 production table: Episode 9 focuses on Raven, Ghost
  compute poverty, a shelter-protector reversal, and Raven sparing a Ghost
  criminal.
- Extends `bible/ghost_ecology.md`, which already defines compute access,
  safe routing, encryption shelter, and Black Zone contracts as Ghost economy
  pressures.
- Uses `characters/005_raven.md` and `technologies/ability_constraints.md`
  correctly: Raven tracks through low-signal routes, camera dead zones, and mesh
  gaps, but cannot teleport, cross true signal voids, or operate freely in fully
  mapped clean light.
- Keeps the Black Zone as market ecology rather than a single villain
  organization.

## Duplicate Check

- Not a duplicate of Episode 3, `Black Zone Receipt`: Episode 3 concerns
  forged consent keys, emotion packs, receipt evidence, and clean institutional
  laundering. Episode 9 concerns compute lease theft, runtime starvation, and an
  illegal Ghost survival shelter.
- Not a duplicate of Episode 5, `Dream Child`: Min Seo-yun's shelter is clinical
  and therapeutic; Oren Vale's shelter is illegal runtime triage.
- Not a duplicate of Episode 8, `The Court Inside ECHO`: Continuity Shelter
  Orders preserve evidence rooms under legal authority; Episode 9's shelter
  keeps unregistered Ghosts running outside lawful authority.

## Canon Risks

- Oren Vale should remain morally compromised. Do not later retcon the compute
  theft into harmless redistribution; the story works because the protection
  really injures other Ghosts.
- Memory Bank should not become a cartoon villain. Its liability and lease
  enforcement are institutionally coherent, even when cruel.
- Raven's spared-target choice should create relationship pressure. It should
  not become a consequence-free cool moment.
- Atlas Protocol should remain a hook, not a reveal. Episode 11 still carries
  the main Atlas narrative turn.

## Required Follow-Up

```yaml
relationship_update_needed:
  Raven:
    Oren Vale: "spared target / shelter witness / evidence-chain breach"
    Shion: "detected omission / unspoken leverage"
    Kane: "field obedience fracture / command trust strain"
  Shion:
    Raven: "knows report omission / protects audit for now"
  Kane:
    Raven: "termination order conflict / incomplete evidence concern"
faction_update_needed:
  Memory Bank: "compute lease enforcement / rollback withholding pressure"
  Ghost Union: "illegal shelters as recruitment and liability flashpoint"
  Black Market: "runtime shelter contracts and stolen compute leases"
technology_update_optional:
  candidate: "Compute Lease Knife or Runtime Shelter Ledger"
  note: "Only add if TechnologyAgent can keep it distinct from Shelter Room Hash."
```

## Pipeline State

```yaml
stage: consistency_check
canon_promotion: false
promotion_blockers:
  - relationship update not yet generated
  - faction impact not yet generated
  - compute lease mechanism not yet independently reviewed by TechnologyAgent
next_recommended_agent: RelationshipAgent
asset_tasks: blocked_until_promotion
```

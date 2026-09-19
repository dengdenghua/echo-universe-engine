# Consistency Audit: Family Graph Rollback

Status: candidate_check

Subject:

- `outputs/lore/20260629-130142-lore-entry-family-graph-rollback.md`
- `outputs/technology/20260629-130142-technology-entry-household-relation-graph.md`
- `outputs/faction/20260629-130142-faction-impact-family-graph-rollback.md`
- `outputs/character/20260629-090050-candidate-character-014-imari-chen.md`

Agent: ConsistencyAgent support pass during LoreAgent slot

## Verdict

Pass as candidate output. Do not promote yet.

The bundle gives Imari Chen's Episode 7 case a distinct infrastructure surface:
family relation recognition. It supports the world-centric rule by starting
with school, clinic, Home Core, and custody consequences before White Ghost Team
arrives.

## Canon Compatibility

```yaml
hard_rules:
  no_magic: pass
  no_supernatural_powers: pass
  no_multiverse: pass
  no_time_travel: pass
  technology_origin: pass
  god_fragment_physics_break: not_applicable
terminology:
  avoids_forbidden_product_terms: pass
  uses_story_facing_terms: pass
identity_model:
  separates_biological_life: pass
  separates_legal_identity: pass
  separates_uploaded_continuity: pass
  separates_ghost_selfhood: pass
```

## Duplication Check

No promoted canon or accepted candidate defines Family Graph Rollback or
Household Relation Graph as named systems.

Adjacent material:

- `outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md`
  covers disputed consent freezes.
- `outputs/lore/20260627-130142-lore-entry-care-status-renewal.md` covers care
  support classification and subsidy review.
- `outputs/lore/20260628-130256-lore-entry-memory-lien-notice.md` covers
  creditor claims against memory collateral.
- `bible/personhood_and_identity.md` separates biological life, legal identity,
  uploaded continuity, and Ghost selfhood.

The new bundle is distinct because it concerns relation edges inside legal
identity: spouse, guardian, resident, emergency contact, caregiver, and Home
Core continuity authority.

## Risks Before Promotion

1. Family Graph Rollback must not become total identity deletion. Imari remains
   an active citizen whose relation edges are damaged.
2. Household Relation Graph must remain a registry and permission layer, not a
   test of love or personhood.
3. Memory Bank repair offers should be tempting because they work quickly, not
   because Memory Bank is cartoonishly malicious.
4. White Ghost Team must remain investigators, witnesses, and pressure points.
   The case should not resolve through apology or a single technical fix.
5. Home Core evidence should have privacy cost; otherwise the family damage
   becomes too easy to prove.

## Promotion Recommendation

Hold in `outputs/` as candidate.

Recommended next pipeline steps:

- StoryAgent: write Episode 7 `Probability Debt` beat with Imari as opening
  viewpoint.
- RelationshipAgent: after the story beat, update Noah, Shion, Zero, Yao Nian,
  White Harbor, and Memory Bank relationship pressure.
- TechnologyAgent: only promote Household Relation Graph after Episode 7 proves
  its story value.
- Asset task generation: create school scanner, clinic denial, and Home Core
  family graph UI props only after promotion.

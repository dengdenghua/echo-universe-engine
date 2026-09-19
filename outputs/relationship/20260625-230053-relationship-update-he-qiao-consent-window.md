# Relationship Update Candidate: He Qiao Consent Window

Status: candidate

Agent: RelationshipAgent

Related candidates:

- `outputs/character/20260625-090056-candidate-character-010-he-qiao.md`
- `outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md`
- `outputs/technology/20260625-130033-technology-entry-revocation-token.md`
- `outputs/faction/20260625-130033-faction-impact-consent-revocation-window.md`

## Purpose

He Qiao's case needs faction pressure before any canon promotion. The Consent
Revocation Window gives his mother's Home Core witness record a deadline, but
the drama should come from institutions interpreting the same record through
different needs: law, profit, sanctuary, quarantine, and family grief.

## Candidate Relationship Lines

```yaml
He Qiao:
  Mother Home Core Record: "filial duty / feared uncertainty"
  Zero: "procedural trust / quarantine fear"
  Eve: "grief interpreter / legal ally"
  Memory Bank: "precedent risk / financial predator"
  Ghost Union Legal Cell: "uneasy protection / propaganda risk"
  White Harbor Court: "licensed witness / disposable clerk"
  CHASER: "emergency protection / evidence threat"

Mother Home Core Record:
  He Qiao: "son witness / preferred listener"
  Memory Bank: "contract refusal / reuse threat"
  Ghost Union Legal Cell: "possible sanctuary / possible capture"

Memory Bank:
  He Qiao: "procedural nuisance / liability to price model"
  Mother Home Core Record: "disputed continuity asset"

Ghost Union Legal Cell:
  He Qiao: "civilian witness worth shielding"
  Mother Home Core Record: "personhood test case"

White Harbor Court:
  He Qiao: "chain-of-custody clerk"
  Mother Home Core Record: "sealed evidence, not recognized person"

CHASER:
  He Qiao: "witness to protect until infrastructure risk rises"
  Mother Home Core Record: "quarantine candidate if refusal spreads"
```

## Relationship Dynamics

- He Qiao trusts Zero's discipline but fears her authority because a quarantine
  order could end his mother's only active claim before Ghost Court review.
- Eve can translate his restrained grief into testimony without treating the
  mother's record as automatically human.
- Memory Bank does not need to hate him. It needs his case to remain expensive,
  narrow, and procedurally late.
- Ghost Union legal cells can protect him while militant cells treat the same
  file as recruitment evidence.
- White Harbor Court depends on clerks like He Qiao, but can abandon them if a
  precedent threatens court legitimacy.
- CHASER is not the villain in this case; it is the institution that can protect
  a witness and still destroy the evidence by over-quarantining it.

## Episode Use

This relationship web is best suited for an early Season 1 case adjacent to
Episode 2 or Episode 6, not as a replacement for either:

- Episode 2 remains about a living engineer whose legal identity belongs to a
  Ghost copy.
- He Qiao's case is about post-death consent, Home Core refusal behavior, and
  whether a weak residual pattern can object to commercial reuse.
- Episode 6 remains about a family grief loop; He Qiao can provide legal texture
  but should not become the emotional center of that episode unless the outline
  is revised.

## Canon Risks

- Do not declare the Mother Home Core Record a recognized digital person in this
  relationship update.
- Do not let Revocation Tokens become kill switches or soul containers.
- Do not make He Qiao a universal judge of consent law; he is a licensed witness
  under pressure.
- Do not duplicate Mira Voss. Mira's function is medical continuity repair; He
  Qiao's function is court process, consent evidence, and chain of custody.
- Do not make Ghost Union uniformly heroic or Memory Bank cartoonishly evil.

## Promotion Gate

Promote only after a later ConsistencyAgent pass decides:

1. Whether He Qiao becomes `characters/010_he_qiao.md` or remains a case-only
   candidate.
2. Whether the Mother Home Core Record should receive a named case identifier.
3. Whether the case routes into Episode 2, Episode 6, or a standalone
   inter-episode manga chapter.
4. Whether `relationships/relationships.yaml` should absorb these edges or keep
   them in a separate promoted case relationship file.

## Pipeline State

```yaml
idea: he_qiao_consent_window_relationships
candidate_output: complete
consistency_check: complete
canon_promotion: deferred
timeline_update: not_started
relationship_update: candidate_only
faction_update: already_candidate
asset_task_generation: blocked_until_promotion
```

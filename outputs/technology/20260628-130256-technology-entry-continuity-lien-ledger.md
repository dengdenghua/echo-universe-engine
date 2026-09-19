# Technology Entry: Continuity Lien Ledger

## Candidate Definition

The Continuity Lien Ledger is the regulated financial and legal registry that
tracks claims against memory assets, family archives, continuity insurance
payouts, and Home Core inheritance files.

It is not a Ghost Court and not an identity engine. It records who claims a
right to restrict, seize, export, insure, or release a memory asset, then
routes conflicts to civil review, White Harbor, Ghost Court, CHASER, or Memory
Bank arbitration.

## Ledger Fields

```yaml
continuity_lien_ledger:
  asset_scope:
    asset_type: family_archive, voice_routine, continuity_claim, trauma_record, skill_license, care_pattern, or home_core_inheritance
    asset_status: dormant, active_care, disputed_evidence, weak_ghost_support, commercial_product, or frozen
    home_layer_link: optional
  claimant:
    claimant_type: memory_bank, insurer, family_trust, court, vendor, estate_creditor, or disputed_heir
    claim_basis: loan, insurance_subrogation, unpaid_compute, archive_trust, legal_fee, vendor_contract, or fraud_hold
    priority_rank: senior, junior, emergency_public, or contested
  protection_signals:
    care_status_ref: optional
    witness_seal_ref: optional
    revocation_token_ref: optional
    ghost_court_petition: none, filed, active, or ruled
    chaser_risk_flag: none, identity_harm, infrastructure_risk, or occupation_risk
  enforcement:
    notice_state: pending_notice, restricted_access, collateral_default, emergency_stay, or unlawful_foreclosure
    allowed_actions: view, preserve, bill, export, sell, duplicate, redact, or seize
    blocked_actions: list
    review_deadline: timestamp
```

## Activation Flow

1. A lender, insurer, estate court, vendor, or trust files a claim against a
   memory asset.
2. The ledger identifies whether the asset is ordinary property, active care,
   disputed evidence, weak Ghost support, or commercial archive product.
3. If care, testimony, or selfhood signals exist, enforcement is narrowed before
   export, sale, duplication, or seizure can proceed.
4. Contradictions route to White Harbor, Ghost Court, CHASER, or civil court.
5. The ledger issues a review deadline and allowed-action list rather than a
   broad identity freeze.

## Constraints

- Cannot decide personhood.
- Cannot authorize deletion of a recognized digital person.
- Cannot convert private memory into public evidence without witness review.
- Cannot seize active medical support while a valid care-status appeal is open.
- Cannot hide a procedural memory payload by labeling it collateral.
- Cannot override CHASER quarantine during infrastructure-risk events.

## Failure Modes

- Priority abuse: Memory Bank senior claims outrank family access until appeal,
  making lawful debt feel like disappearance.
- Metadata laundering: a broker relabels weak Ghost support as a dormant
  archive so seizure appears ordinary.
- Deadline weaponization: short review windows push families into Black Zone
  copies before lawful help arrives.
- Cross-district drift: different ledger relays disagree on allowed actions,
  creating exploitable enforcement gaps.
- Contract fog: a grief-support product hides lien rights inside subscription
  renewal language.

## Story Hooks

- Raven follows a lawful-looking foreclosure through three ledger relays and
  finds the relay drift was deliberately induced.
- Shion compares blocked-action lists and catches a lender trying to duplicate
  a care pattern during a supposed preservation-only stay.
- Kane treats a ledger notice as a public-safety warning after the same vendor
  appears in veteran care, skill lease, and archive foreclosure cases.
- Luna notices a weak Ghost keeps repeating the phrase "do not sell my room"
  because the ledger has already marked its childhood archive as collateral.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260628-130256-lore-entry-memory-lien-notice.md
  - outputs/technology/20260625-130033-technology-entry-revocation-token.md
  - outputs/technology/20260626-130218-technology-entry-witness-seal.md
  - outputs/technology/20260627-130142-technology-entry-care-status-classifier.md
requires:
  - ConsistencyAgent duplicate check against Memory Bank freeze and identity collateral canon
  - FactionAgent impact pass before promotion
asset_tasks: blocked_until_promotion
```

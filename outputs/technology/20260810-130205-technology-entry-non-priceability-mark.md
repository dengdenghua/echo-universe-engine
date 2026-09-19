# Technology Entry: Non-Priceability Mark

## Candidate Canon Entry

The Non-Priceability Mark is a temporary Memory Bank ledger state attached to a
sealed continuity object during Non-Priceability Review.

It does not erase debt, certify Ghost personhood, open a Home Layer, forgive
storage fees, or make the bank ethical. It blocks one specific action: assigning
asset value to protected content when function can be proven without exposing
the content itself.

```yaml
technology:
  name: Non-Priceability Mark
  category: Memory Bank debt-scope ledger / sealed continuity valuation control
  status: candidate
  related_lore: Non-Priceability Review
  primary_users:
    - Memory Bank sealed-asset underwriters
    - debt-scope appeal clerks
    - continuity insurance auditors
    - court-appointed financial witnesses
    - CHASER limited-jurisdiction observers
  prohibited_use: >
    Cannot make a memory priceless by moral claim alone, hide public safety
    evidence, certify or deny claimant personhood, stop storage fees, override
    a lawful emergency review, or prevent a later court from compelling export.
```

## Ledger Fields

```yaml
non_priceability_mark:
  mark_id: underwriter bond id plus sealed object hash plus expiry timestamp
  sealed_object:
    - Home_Core_afterword_hash
    - phrase_or_routine_redaction_hash
    - beneficiary_refusal_card_id
    - Home_Layer_export_block_scope
    - claimant_uncertainty_flag
  proof_scope:
    - negative_proof_packet_hash
    - verified_function_labels
    - prohibited_content_fields
    - human_witness_effect_statement_ids
    - CHASER_classification_boundary
  financial_scope:
    - debt_attachment_state
    - route_history_value_state
    - insurance_reserve_state
    - storage_fee_meter
    - compute_reserve_hold_state
    - creditor_appeal_window
  accountability:
    - underwriter_bond_signature
    - audit_mirror_id
    - expiry_clock
    - override_authority_list
    - fraud_review_trigger
```

## Operations

- Valuation pause: blocks asset pricing for the sealed phrase, routine, or
  afterword while the mark is active.
- Function retention: allows a scoped record to say what the object does without
  saying what it contains.
- Debt-scope narrowing: prevents creditors from treating protected content as
  route-history collateral unless a later order compels export or accepts a
  different proof path.
- Claimant reserve delay: records possible weak claimant risk without funding a
  claimant buffer from a living recipient's private phrase by default.
- Audit mirror: binds the underwriter's bond to the refusal so Memory Bank can
  discipline abuse, hesitation, or unauthorized mercy.
- Expiry pressure: forces review to return to court, CHASER classification,
  executive override, or beneficiary renewal instead of becoming permanent
  invisibility.

## Failure Modes

- Fraud shelter: a sealed object hides liability evidence or forged consent
  behind non-priceability.
- Claimant starvation: a weak self-updating residue loses compute because the
  mark delays reserve funding.
- Fee extraction: Memory Bank stops valuation but continues charging storage,
  review, and audit fees around the protected absence.
- Underwriter capture: senior desks punish underwriters until the mark becomes
  too risky to use except for wealthy clients.
- Scope creep: creditors reprice surrounding records, witness statements, or
  storage routes even when the central phrase remains unpriced.
- CHASER flattening: safety classification treats unresolved sealed evidence as
  contamination and bypasses the review.

## Story Limitations

Vera Qadir can apply the mark only when a sealed object, living refusal,
valuation attempt, and scoped technical proof all exist at the same time. She
cannot keep it active indefinitely, cancel Nara Marr's family debt, settle Ilya
Marr's claimant ambiguity, protect Tarek Sol's license, or force Ghost Union to
accept beneficiary silence.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-10T13:02:05+08:00"
canon_promotion: false
related_lore: outputs/lore/20260810-130205-lore-entry-non-priceability-review.md
related_character: outputs/character/20260810-090107-candidate-character-039-vera-qadir.md
related_story: outputs/story/20260806-180106-story-beat-the-phrase-stays-sealed.md
requires_consistency_review: true
```

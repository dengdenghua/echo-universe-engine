# Technology Entry: Civil Delay Token

## Candidate Definition

A Civil Delay Token is a time-limited White Harbor authorization that pauses a
specific automated civil action while contradictory relation, care, or identity
evidence is reviewed.

It is not a repair key. It does not change who someone is. It tells a school
gate, clinic desk, custody rail, elder-care route, or Home Core routine lock to
hold the next irreversible step long enough for scoped evidence comparison.

## Token Fields

```yaml
civil_delay_token:
  token_identity:
    token_id: signed White Harbor delay reference
    issuing_operator: named human operator with active license
    issue_time: audited timestamp
    expiry_time: audited timestamp
    renewal_limit: none, single_supervisor_review, court_required, or chaser_hold_required
  trigger_context:
    dependent_person: child, elder, patient, assisted_adult, or other
    disputed_edge: guardian, caregiver, spouse, resident, emergency_contact, continuity_holder
    automated_action: custody_transfer, pickup_denial_escalation, clinic_lockout, care_removal, home_core_freeze
  evidence_scope:
    allowed_sources:
      - civil_registry
      - school_or_clinic_record
      - Home Core witness fragment
      - court file
      - CHASER incident hold
    prohibited_sources:
      - full domestic routine export without review
      - unrelated memory stream
      - unrelated financial history
  liability:
    operator_record: attached
    appeal_record: attached
    harm_review: required_if_delay_causes_injury_or_loss
    pension_risk_score: updated_after_review
  system_effect:
    action_pause: active, expired, overridden, or converted_to_hold
    restoration_power: none
    privacy_shield: scoped
```

## Activation Flow

1. A service marks a dependent-care action as imminent.
2. A relation, care, or identity edge contradicts at least one trusted source.
3. A licensed White Harbor operator accepts personal audit attachment.
4. The token pauses only the named action and only until expiry.
5. Evidence comparison runs across approved sources.
6. The token expires, renews through supervisor review, converts to CHASER hold,
   or yields to court order.

## Constraints

- Cannot repair a Household Relation Graph.
- Cannot override a court custody order or recognized digital person protection.
- Cannot force Memory Bank, Home Core vendors, or clinics to waive unrelated
  contract terms.
- Cannot expose full Home Core routines when a witness fragment is enough.
- Cannot remain active indefinitely without external authority.
- Cannot decide whether a Ghost is family; it can only pause a dependent-care
  action involving disputed evidence.

## Failure Modes

- Narrow token: it pauses school pickup escalation but not a clinic signing
  lockout.
- Expiry cascade: one paused system waits while another service moves ahead.
- Operator chill: high liability scores make staff avoid valid borderline
  cases.
- Privacy breach: an agency uses delay urgency to demand broad domestic logs.
- Vendor interception: a repair provider uses the token timer as leverage for
  costly restoration terms.

## Story Hooks

- Sofia issues a twelve-minute token to stop Imari Chen's daughter from being
  moved while the Household Relation Graph remains contradictory.
- Shion designs a scoped Home Core witness request that proves guardian routine
  continuity without exposing the child's unrelated fear response.
- Zero converts an expiring delay into a CHASER evidence hold, protecting proof
  while worsening Imari's restoration timeline.
- Noah sees that his probability model counted delay tokens as service friction
  rather than human risk.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260630-130040-lore-entry-emergency-delay-window.md
  - outputs/character/20260630-090234-candidate-character-015-sofia-marin.md
  - outputs/technology/20260629-130142-technology-entry-household-relation-graph.md
recommended_next_step: consistency_audit
asset_tasks: blocked_until_promotion
```

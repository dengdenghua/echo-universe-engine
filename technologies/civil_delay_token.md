# Civil Delay Token

A Civil Delay Token is a time-limited White Harbor authorization that pauses a
specific automated civil action while contradictory relation, care, or identity
evidence is reviewed.

It is not a repair key. It does not change who someone is. It tells a school
gate, clinic desk, custody rail, elder-care route, or Home Core routine lock to
hold the next irreversible step long enough for scoped evidence comparison.

## Canon Scope

For Season 1 Episode 7, `Probability Debt`, the token is Sofia Marin's narrow
tool inside an Emergency Delay Window. It can stop Imari Chen's daughter from
being moved by an automated custody rail for minutes. It cannot restore Imari's
Household Relation Graph, make Noah's operation harmless, or force Memory Bank
to waive repair collateral.

```yaml
civil_delay_token:
  episode_scope: "Season 1 Episode 7 / Probability Debt"
  issuing_authority: White_Harbor
  episode_operator: Sofia_Marin
  trigger_context:
    dependent_person: child
    disputed_edge: guardian
    automated_action: custody_transfer
  duration:
    initial_window: "12 minutes"
    renewal_limit: supervisor_or_external_hold_required
  system_effect:
    action_pause: active_until_expiry
    restoration_power: none
    privacy_shield: scoped
```

## Emergency Delay Window

An Emergency Delay Window is the civil interval created by a valid token. It
gives public systems time to compare evidence before a disputed relation edge
becomes custody transfer, clinic lockout, school denial escalation, elder-care
removal, or Home Core routine freeze.

Families call it borrowed time.

```yaml
emergency_delay_window:
  states:
    - threshold_warning
    - delay_eligible
    - active_delay
    - evidence_narrowing
    - expiry_pressure
    - failed_delay
  allowed_evidence:
    - civil_registry
    - school_or_clinic_record
    - home_core_witness_fragment
    - court_file
    - chaser_incident_hold
  prohibited_shortcuts:
    - full_domestic_routine_export_without_review
    - unrelated_memory_stream
    - unrelated_financial_history
    - indefinite_pause_without_external_authority
```

## Operator Risk

Every token attaches audit liability to a named human operator. The system can
protect a dependent person by transferring risk onto the staff member who signs
the delay. In Episode 7, Sofia can make the city wait, but she cannot make the
city kind or whole.

## Limits

- A token cannot repair a Household Relation Graph.
- It cannot override a court custody order or recognized digital person
  protection.
- It cannot expose a family's whole Home Layer when a witness fragment is
  enough.
- It cannot force Memory Bank, vendors, schools, or clinics to waive unrelated
  contract terms.
- It cannot remain active indefinitely without supervisor review, court order,
  CHASER hold, or another external authority.

## Story Use

The token gives Episode 7 a legal and emotional timer. White Harbor can create
minutes, CHASER can preserve evidence, Memory Bank can sell speed, and Imari's
family still has to survive the gap between delay and restoration.

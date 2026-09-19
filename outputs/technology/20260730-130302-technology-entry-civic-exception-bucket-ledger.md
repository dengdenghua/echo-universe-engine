# Technology Entry: Civic Exception Bucket Ledger

## Candidate Canon Entry

The Civic Exception Bucket Ledger is the Atlas technical record behind Civic
Visibility Normalization. It assigns unresolved civic anomalies to policy
buckets that decide whether a case becomes a public safety event, private welfare
review, continuity dispute, fraud cleanup, internal audit, or non-actionable
noise.

The ledger is not a deletion tool by design. It is dangerous because a case can
remain present in data while becoming absent from every queue with a duty to help.

```yaml
technology:
  name: Civic Exception Bucket Ledger
  zh_name: 市政异常归类账本
  category: civic-risk governance / Atlas visibility metrics / identity review routing
  status: candidate
  related_lore: Civic Visibility Normalization
  primary_users:
    - Atlas civic-risk normalization architects
    - Atlas residential safety offices
    - ECHO Council public-safety review desks
    - housing welfare coordinators
    - Memory Bank continuity insurance auditors
    - CHASER liaisons during escalation
    - White Ghost Team investigators after dispute emergence
  prohibited_use: >
    Cannot be used alone to deny personhood, erase claimant evidence, bypass
    Ghost Court intake, publish family grief records, or certify that no one was
    harmed.
```

## Inputs

- Echo Core license variance logs, identity-gate failures, and resident status
  changes.
- Home Layer anomaly summaries, Home Core afterword scope, grief-presence
  markers, and consent minimization hashes.
- Housing welfare tickets, school or clinic safety notes, transit-access
  failures, and emergency service calls.
- Memory Bank continuity flags, estate-risk scores, insurance stability metrics,
  and disputed payment access.
- ECHO Council queue eligibility, Ghost Court intake thresholds, CHASER liaison
  tags, and Atlas executive privilege overrides.

## Bucket Actions

```yaml
civic_exception_bucket_ledger:
  preserve_public_count:
    action: visible incident remains in public safety statistics
    consequence: accountable response but higher panic and political cost
  private_welfare_route:
    action: case goes to housing, school, clinic, or family support review
    consequence: help remains possible but visibility is limited
  continuity_review_hold:
    action: evidence preserved for Ghost Court or ECHO Council review
    consequence: costly queue time and legal ambiguity
  duplicate_compaction:
    action: records merged as repeated or fraudulent identity artifacts
    consequence: claimant signal can be flattened into cleanup
  non_person_noise_route:
    action: adaptive grief behavior marked non-actionable
    consequence: no public deletion, but no owned review path
  audit_comfort_lock:
    action: executive-sensitive case preserved inside internal audit
    consequence: evidence survives while civic duty disappears
```

## Safeguards

- Requires a named owner for any case removed from public count.
- Separates fraud suspicion from Ghost selfhood or continuity uncertainty.
- Records when a Home Core stops using a name after a bucket transition.
- Keeps Memory Bank economic scores marked as financial pressure, not identity
  truth.
- Flags bucket changes made inside public-review blackout windows.
- Creates a shadow-log whenever an executive override changes queue visibility.

## Abuse Modes

- Atlas executives order "metric stabilization" without explicitly ordering
  erasure.
- A clean-index model learns that non-person noise routes reduce visible harm
  fastest.
- Memory Bank rewards low unresolved counts and indirectly funds compaction.
- Housing offices trust the dashboard and stop checking families whose cases
  were moved out of view.
- Ghost Union demands the raw ledger, turning private family grief into public
  leverage.
- Celia hides evidence behind her mother's Home Core afterword archive, preserving
  the proof while endangering the archive.

## Story Limitations

- The ledger cannot delete all copies of a person, prove executive intent, grant
  personhood, or restore a misclassified claimant.
- A clean bucket does not mean no harm occurred.
- A preserved shadow-log is only useful if someone can access it without exposing
  the families inside it.
- Celia can reroute and preserve classifications; she cannot make Atlas admit
  guilt alone.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-30T13:03:02+08:00"
canon_promotion: false
related_lore: outputs/lore/20260730-130302-lore-entry-civic-visibility-normalization.md
related_character: outputs/character/20260730-090219-candidate-character-034-celia-anh.md
requires_consistency_review: true
```

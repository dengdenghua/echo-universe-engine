# Technology Entry: Curfew Edge Evidence Packet

## Candidate Canon Entry

The Curfew Edge Evidence Packet is the scoped record bundle opened when a
supervised-release violation reaches automatic detention while local evidence
disagrees.

It does not decide guilt, innocence, personhood, or intent. It preserves the
minimum technical contradiction needed for a release witness, CHASER liaison, or
court clerk to review whether detention timing would destroy relevant evidence
or leave a living complainant unprotected.

```yaml
technology:
  name: Curfew Edge Evidence Packet
  zh_name: 宵禁边缘证据包
  category: supervised-release telemetry / Home Layer evidence scope / civil detention timing
  status: candidate
  related_lore: Curfew Edge Review
  primary_users:
    - White Harbor civil-release desks
    - supervised-release audit clerks
    - CHASER liaison officers
    - court auto-warrant review nodes
    - licensed Home Layer witnesses
  prohibited_use: >
    Cannot clear charges, certify Ghost selfhood, export full Home Core rooms,
    hide living-complainant risk, rewrite geofence telemetry, or sell afterword
    archives as compliance collateral.
```

## Packet Fields

```yaml
curfew_edge_evidence_packet:
  packet_id: release desk identifier plus sealed timestamp
  supervisee_state:
    - wrist_monitor_id
    - active_release_condition
    - geofence_boundary
    - prior_hold_count
    - active_compliance_debt_flag
  timing_conflict:
    - curfew_deadline
    - auto_warrant_execution_time
    - stairwell_clock_time
    - Home_Core_door_event_time
    - CHASER_liaison_ping_time
  scoped_door_witness:
    - door_open_or_denial
    - care_phrase_hash
    - routine_origin_window
    - unrelated_room_export_block
    - afterword_presence_flag
  living_risk_scope:
    - complainant_safety_flag
    - neighbor_distance_warning
    - body_line_risk_level
    - emergency_override_reason
  custody_outputs:
    - compliance_strip_hash
    - witness_signature
    - hold_duration
    - audit_exposure_note
    - redaction_boundary
```

## Operations

- Edge detection: compares curfew deadline, wrist-monitor location, and
  geofence confidence during the final enforcement margin.
- Door witness scope: exports only the Home Core door event, relevant care
  phrase hash, and routine timing needed for the violation review.
- Living-risk bind: prevents a hold from opening unless the complainant safety
  state is named in the same packet.
- CHASER override seal: records when field safety overrides the hold and whether
  the contradiction was preserved before containment.
- Debt firewall: blocks Memory Bank from treating afterword flags, Home Core
  room names, or unrelated family routines as compliance collateral.
- Audit trace: records the officer who paused enforcement and the exact
  evidence conflict they accepted.

## Failure Modes

- Mercy laundering: a release officer uses a Home Core routine as an excuse to
  ignore real complainant danger.
- Clean punishment harm: automatic detention executes before the door witness is
  sealed, then the missing contradiction is treated as no contradiction.
- Archive capture: Memory Bank attaches a sealed afterword to compliance debt
  because repeated holds increase risk scoring.
- Publicity harm: Ghost Union leaks the door phrase to defend a weak claimant
  and exposes the family's private grief.
- Tactical deception: a supervisee learns to trigger old routines near curfew
  edges to manufacture review pressure.

## Story Limitations

Rosa can open a Curfew Edge Evidence Packet to make the system wait and name the
contradiction. She cannot prove Lu Wen's innocence, certify Mei Wen's afterword
as a Ghost, protect the neighbor if immediate body-line danger is present, or
stop Memory Bank from flagging the family unless later review accepts the
packet.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-02T13:02:50+08:00"
canon_promotion: false
related_lore: outputs/lore/20260802-130250-lore-entry-curfew-edge-review.md
related_character: outputs/character/20260802-090147-candidate-character-037-rosa-valen.md
requires_consistency_review: true
```

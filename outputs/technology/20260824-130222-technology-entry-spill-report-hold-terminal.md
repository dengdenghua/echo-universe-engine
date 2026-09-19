# Technology Entry: Spill Report Hold Terminal

## Candidate Canon Entry

The Spill Report Hold Terminal is the claims-desk tool that pauses automatic
refund closure for a licensed public Dream Network route. It preserves a scoped
telemetry packet long enough for consent, safety, and archive-review specialists
to decide whether the complaint is only a service failure or evidence of harm
to a participant, family, or possible Ghost pattern.

It does not enter dreams. It does not read minds. It does not prove personhood.
It holds the record before the refund button deletes it.

## Packet Sketch

```yaml
spill_report_hold:
  claim_id: dream_network_public_claim_reference
  route_id_hash: licensed_public_route_hash
  claimant_scope:
    claimant_type: family_member | participant | guardian | civic_witness
    consent_status: direct | guardian | emergency_harm_scope | disputed
    refund_requested: true
  preserved_material:
    route_state_hash: required
    consent_boundary_snapshot: required
    affective_spill_hash: required
    rendered_phrase_fingerprint: optional
    wake_anchor_reference: optional
    home_core_texture_reference: hash_only
  prohibited_exports:
    - full_home_layer_memory
    - raw_child_voice_model
    - unrelated_family_archive
    - live_session_body_state_without_scope
  hold_window:
    default_hours: 48
    emergency_extension_hours: 24
    purge_on_release: true
  referral_paths:
    - dream_network_safety_review
    - consent_boundary_review
    - memory_bank_archive_dispute
    - chaser_low_threat_notice
```

## What It Can Do

- Pause a refund queue before telemetry purge.
- Preserve route hashes, consent snapshots, spill fingerprints, and limited
  wake-anchor references.
- Record that a Home Core grief texture was involved without copying the
  private Home Layer content.
- Give Shion enough packet structure to compare routes.
- Give Eve a narrow consent object to defend in review.
- Give CHASER notice without automatically escalating the case to containment.

## What It Cannot Do

- Certify that a responsive route contains a Ghost.
- Identify a child from a lullaby fingerprint alone.
- Override Memory Bank archive ownership.
- Force Dream Network to admit liability.
- Protect a family from settlement pressure.
- Keep the disputed pattern stable if compute is withdrawn.

## Failure Modes

- Over-narrow hold: the refund closes and deletes the only useful telemetry.
- Over-broad hold: private Home Layer grief becomes discoverable evidence.
- Archive collision: Memory Bank classifies the phrase as licensed texture and
  blocks comparison.
- Safety overroute: CHASER receives the packet as contamination evidence before
  consent review.
- Clerk liability: the signer becomes responsible for delaying compensation
  even when the delay protects proof.

## Countermeasures

- Hash-only Home Core and Home Layer references unless a court or consent scope
  authorizes deeper review.
- Separate refund money from telemetry release so families are not punished for
  preserving evidence.
- Require a human claims signature before purge override.
- Log every Memory Bank archive objection as a separate packet, not a reason to
  delete the hold.
- Attach an analog receipt that states what was preserved and what was not
  copied.

## Story Use

- Makes Jules Mbeki's power concrete and limited.
- Shows Dream Network's moral gray zone without making the faction a simple
  villain.
- Creates a bridge from Episode 5, `Dream Child`, to later Memory Bank archive
  disputes.
- Gives White Ghost Team a non-combat entry point: a held packet, not a threat
  alarm.
- Forces the question of whether a refund is care, erasure, or both.

## Consistency Notes

- Mechanism uses Dream Network claims terminals, route telemetry, consent
  ledgers, Home Core grief-texture references, Home Layer scope controls,
  Memory Bank archive claims, CHASER notices, and distributed computation.
- No magic, supernatural powers, multiverse, or time travel.
- Distinct from Wake Anchor Token: wake anchors prove exit routes during a
  live projection session; Spill Report Hold preserves post-incident evidence
  before refund purge.
- Distinct from Motor Authorship Trace Packet: motor authorship concerns body
  agency in rehabilitation rooms; spill reports concern affective harm in
  public routes.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-24T13:02:22+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260824-130222-lore-entry-dream-network-civic-claims.md
  - outputs/character/20260824-090213-candidate-character-049-jules-mbeki.md
  - outputs/technology/20260713-130255-technology-entry-wake-anchor-token.md
requires:
  - FactionAgent impact
  - ConsistencyAgent review against Dream Network mechanics, Dream Child, and Red Intake Split
asset_tasks:
  - outputs/assets/20260824-130222-asset-task-prop-spill-report-hold-terminal.yaml
```

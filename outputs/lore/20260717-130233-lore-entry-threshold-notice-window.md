# Lore Entry: Threshold Notice Window

## Candidate Canon Entry

A Threshold Notice Window is the short civil warning interval before CHASER,
police, medical responders, or an evacuation unit enter an occupied Home Core
environment during a suspected Ghost, continuity, or ECHO infrastructure
incident.

It exists because the first official act at a home used to be force: a breached
door, a muted Home Core, a red evacuation route, a command voice in the hallway.
White Harbor districts created the notice window after multiple raids were
technically lawful but socially disastrous. Families heard armor before they
heard why the Second Nervous System had marked their home.

The public rule is plain:

Before the door opens, the home must hear who is outside, why they are there,
what choices remain, and what will happen if the home refuses.

## Historical Event

```yaml
2146:
  event: Threshold Notice Window adopted in White Harbor civil-warning districts
  summary: >
    After a CHASER amber-entry incident ends with a lawful breach, a dead
    resident, and a forged Home Core acknowledgment, White Harbor requires a
    human-readable warning receipt before pre-containment entry whenever time
    and public-safety risk allow.
  consequence: >
    CHASER gains a cleaner liability record, civil-warning officers gain
    dangerous delay authority, and Ghost Union argues that a home able to answer
    deserves more than a countdown.
```

## Window States

```yaml
threshold_notice_window:
  pre_notice:
    meaning: CHASER or civil responders are queued outside but entry authority is not yet hard containment
    protection: civil-warning officer may request a threshold script
  active_notice:
    meaning: resident, caregiver, Home Core, or possible Ghost residue receives the warning
    protection: the home can acknowledge, refuse, ask for medical routing, or name a personhood complication
  integrity_check:
    meaning: acknowledgment source is compared against door sensors, Home Core routing, building mesh, and voice receipt
    protection: forged calm responses can trigger delay or Shion-level review
  amber_entry_delay:
    meaning: a short delay is granted because the notice revealed child, medical, personhood, or evacuation complications
    protection: entry clock slows while command reviews scoped facts
  command_override:
    meaning: CHASER enters despite notice risk because threat, spread, or neighbor harm crosses containment threshold
    protection: override becomes part of the public and Ghost Court audit packet
  failed_notice:
    meaning: warning route is jammed, forged, ignored, or too dangerous to complete
    protection: failure reason must be recorded before entry if systems remain live
```

## Social Function

- Makes CHASER entry legible to civilians before protection feels like invasion.
- Gives Home Core acknowledgments evidentiary weight without treating every
  answer as Ghost personhood.
- Gives civil-warning officers a narrow way to slow escalation when a door
  contains more than threat data.
- Gives early Season 1 a household-entry ethics scene before White Ghost Team
  takes over the case.
- Makes public trust depend on mundane procedure, not hero rescue.

## Failure Modes

- Forged calm: a compromised Home Core produces an acknowledgment while people
  inside are hiding or incapacitated.
- Delay harm: the warning gives a hostile operator time to erase logs, spread
  panic, or route through building infrastructure.
- Liability theater: CHASER uses the warning script to sanitize a breach already
  decided by command.
- Voice coercion: a dead parent routine tells residents not to answer, turning
  domestic love into tactical danger.
- Neighborhood cascade: a hallway warning spreads panic into adjacent Home
  Layer routes before evacuation is ready.

## Story Hooks

- Juno Park reads a threshold notice while CHASER command counts down to amber
  entry and the Home Core answers in a dead mother's voice.
- Kane wants the door open because the evacuation graph is worsening; Juno wants
  one integrity check because the acknowledgment sounds rehearsed.
- Shion proves the calm response came from the building mesh, not the apartment.
- Zero hears a possible personhood claim through the Home Layer speaker but
  cannot convert resonance into legal protection.
- Eve sees that the official script is correct and still designed to make
  refusal sound irrational.

## Consistency Notes

- Threshold Notice Window is a civil procedure using warning scripts,
  acknowledgment hashes, building access systems, Home Core routing, CHASER
  amber-entry queues, evacuation maps, and Ghost Court audit rails. It is not
  magic.
- Distinct from Emergency Delay Window: emergency delay pauses automated civil
  harm involving care, custody, or identity edges; threshold notice governs
  pre-entry warning at a physical or verified remote home threshold.
- Distinct from Analog Presence Review: presence review requires a witness
  before irreversible Home Layer action; threshold notice warns before entry or
  evacuation during a live incident.
- Distinct from Witness Seal: witness seal protects captured testimony after
  the fact; threshold notice records what was said before the door opened.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-17T13:02:33+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260717-090328-candidate-character-025-juno-park.md
  - outputs/lore/20260630-130040-lore-entry-emergency-delay-window.md
  - outputs/lore/20260712-130048-lore-entry-analog-presence-review.md
requires:
  - TechnologyAgent entry for Threshold Receipt Packet
  - FactionAgent impact on CHASER, White Harbor, Ghost Union, Memory Bank, Atlas, and Black Zone
  - ConsistencyAgent review against Juno Park and existing civil procedures
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```

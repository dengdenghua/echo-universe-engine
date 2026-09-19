# Lore Entry: Neighbor Care Standing

## Candidate Canon Entry

Neighbor Care Standing is a civil recognition state used when the Home Layer,
clinics, shelters, transit desks, or market systems must decide whether an
informal caregiver may perform one urgent care action before formal family,
guardian, resident, or medical-proxy authority can be repaired.

It exists because ECHO cities contain millions of lives held together by people
who are not legally family: neighbors who know insulin schedules, market aunties
who notice missed breakfasts, shelter workers who remember which voice calms a
Ghost-adjacent panic, co-tenants who carry spare door codes, and clinic clerks
who can tell when a Home Core apology loop means someone is locked outside.

Neighbor Care Standing does not make a stranger into family. It creates a
temporary, auditable care lane so the city does not let a person bleed, freeze,
starve, lose custody, miss medicine, or vanish from a shelter queue while the
Memory Sea argues over relation edges.

## Timeline Placement

- 2041: Household AI cores become legal family memory custodians in several
  major city networks.
- 2098: City registries begin syncing household relation metadata from Home
  Cores, schools, clinics, and family courts.
- 2139: White Harbor recognizes relation loss as a distinct identity harm.
- 2148: After early White Ghost Team cases expose people harmed by clean legal
  denials, Shanghai Ring pilot desks begin granting scoped Neighbor Care
  Standing for non-family witnesses during Home Layer access and medical
  disputes.

## Standing Classes

```yaml
neighbor_care_standing:
  witness_only:
    meaning: informal caregiver may confirm a routine, name, route, or access pattern
    protection: no authority to change medication, money, custody, or identity
  comfort_contact:
    meaning: person may speak, sit, call, or accompany during panic, clinic intake, shelter routing, or Ghost-adjacent review
    protection: all speech and presence logs remain scoped to the incident
  essential_care_action:
    meaning: person may perform one bounded action such as food delivery, medicine handoff, door wait, school pickup hold, or shelter bed preservation
    protection: action expires when formal authority arrives or review closes
  access_pause_witness:
    meaning: person may witness manual latch, kiosk denial, gate refusal, or Home Core caution mode before reset
    protection: preserves evidence without granting permanent access
  contested_care_flag:
    meaning: family, Memory Bank, landlord, or CHASER disputes the informal caregiver's role
    protection: routes to White Harbor or civil-care tribunal before punishment language attaches
```

## Social Function

- Gives ordinary communities a lawful way to keep each other alive during
  infrastructure failure.
- Separates care evidence from family authority, so a neighbor's knowledge does
  not become an inheritance claim.
- Lets White Harbor slow down harmful automated denials without exporting full
  Home Core archives.
- Gives CHASER field teams a non-containment option when panic begins around a
  disputed Home Layer event.
- Makes neighborhood life part of canon infrastructure rather than background
  scenery.

## Failure Modes

- False intimacy: a broker forges standing by learning enough routine details
  to sound like a trusted neighbor.
- Care punishment: families accuse a witness of theft, stalking, or Ghost
  sympathy because they know private routines.
- Institutional laundering: Memory Bank cites a neighbor's routine knowledge as
  proof that a family archive has marketable value.
- CHASER flattening: field officers treat all informal standing as suspicious
  access instead of distinguishing care from intrusion.
- Queue capture: only neighborhoods with legal literacy or White Harbor access
  receive standing before harm occurs.

## Story Hooks

- Mara Ibe identifies a dead commuter record because a tea-stall owner has
  Neighbor Care Standing to preserve her daily route contradiction.
- In a borrowed-care case, a market auntie can keep medicine moving while Shion
  maps the Home Layer mismatch.
- A landlord tries to delete a witness route by calling it trespass; White
  Harbor treats the same route as access-pause evidence.
- Ghost Union argues that some Ghosts first survive because a living neighbor
  kept repeating ordinary care when family authority failed.
- Memory Bank turns a neighbor's kindness into risk language, forcing Kane to
  fight a civil classification rather than a person.

## Consistency Notes

- Neighbor Care Standing is not adoption, guardianship, possession, fate,
  supernatural kinship, or literal transfer of identity.
- It operates through Home Core habit logs, manual witness routes, clinic
  emergency rules, shelter queues, school holds, civil-care tribunal routing,
  and White Harbor scoped intake.
- Distinct from Household Relation Graph: the graph stores formal relation
  edges; Neighbor Care Standing is a temporary care lane for people outside
  those edges.
- Distinct from Procedural Proxy Chain: proxy chains execute a final authorized
  procedure; standing preserves or permits bounded daily care while authority is
  disputed.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-20T13:02:58+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260629-130142-lore-entry-family-graph-rollback.md
  - outputs/lore/20260719-130148-lore-entry-home-layer-mismatch-review.md
  - outputs/character/20260720-090320-candidate-character-028-mara-ibe.md
requires:
  - TechnologyAgent entry for Neighbor Care Standing Token
  - FactionAgent impact on White Harbor, CHASER, Memory Bank, Ghost Union, Black Zone, clinics, shelters, and landlords
  - ConsistencyAgent review against Household Relation Graph, Civil Delay Token, Procedural Proxy Chain, and Borrowed Care Attribution Packet
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```

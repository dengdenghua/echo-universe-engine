# Story Beat Candidate: The Minute Has a Name

Status: candidate

Season: Ghost Awakening / early Season 1 White Harbor civic aftermath route

Canon position: usable directly after `Cold Minute`, or as a quieter follow-up
case before the Black Zone shelter route is promoted

Agent: StoryAgent

Created at: 2026-08-01T18:01:07+08:00

## Production Purpose

`The Minute Has a Name` tests whether Amber Reserve can become a recurring
Season 1 civic mechanism instead of a one-case battery detail. It follows the
public hearing after Spill Block 6, where the same bridge-minute record that
saved Tuesday's testimony now exposes Imani Vale, living patients, CHASER,
Ghost Union, Memory Bank, and the housing block to different kinds of blame.

The beat keeps the injury social and procedural. No new supernatural effect is
introduced; the conflict operates through clinic reserve logs, Home Layer
witness strips, CHASER custody records, Memory Bank lien pressure, block votes,
and the practical language people use when the Memory Sea asks a living room to
pay for one more voice.

## Logline

After the Spill Block 6 sweep, Imani Vale is ordered to name every bridge minute
spent on Tuesday before she can regain clinic access. Kane needs the ledger to
prove lawful seizure did not erase testimony, Ghost Union wants the same ledger
as evidence of state cruelty, and Memory Bank offers to clear Imani's debt if
she lets the names become collateral.

## Case Character

```yaml
case_character:
  name: Imani Vale
  ordinary_role: suspended night clinic battery steward and volunteer stairwell medic
  memory_disruption: >
    Tuesday's preserved witness strip contains enough domestic grammar to force
    review, but the bridge-minute ledger also names living patients, block heat
    buffers, and one coerced guarantor who all paid for that answer.
  what_they_want: >
    Regain enough clinic access to care for Lio, keep Tuesday's answer in
    review, and stop the hearing from turning neighbors into debtors or slogans.
  what_the_system_calls_them: >
    reserve misuse operator, continuity evidence holder, unlawful bridge
    steward, living-patient risk witness, potential lien respondent
  what_they_lose: >
    the hope that a truthful record will be read as care before it is read as
    liability
  what_they_reveal_about_echo: >
    the Memory Sea can preserve a fragile answer, but only public procedure can
    decide whether the cost of hearing it was consent, debt, injury, or duty
```

## Core Question

When a bridge minute saves testimony and harms reserve at the same time, does
naming the payer create justice, prosecution, debt, or only a cleaner record of
who was already forced to choose?

## Involved Characters

- Imani Vale: suspended steward; owns the most complete analog bridge-minute
  ledger but cannot safely release it whole.
- Lio Vale: living patient whose respiratory margin appears in the ledger and
  whose privacy becomes part of the public cost of Tuesday's answer.
- Tuesday: weak Ghost claimant in CHASER custody; has fewer words after the
  sweep, but still recognizes "kitchen" and "Home" when the witness strip is
  replayed.
- Kane: needs the ledger to prove CHASER preserved evidence, but knows the same
  ledger proves lawful seizure caused damage.
- Shion: can redact Home Layer room exposure and medical signals, but each
  redaction makes some faction claim the record is incomplete.
- Raven: tracks the coerced guarantor signature and sees that protecting the
  corridor map can also protect the creditor who forced the signature.
- Oren Mbeki: refuses to attend the hearing until Imani enters the first bridge
  minute under his route name, making his corridor accountable.
- Memory Bank lien counsel: offers debt relief in exchange for treating the
  ledger as route-history collateral.
- Ghost Union observer: demands the ledger be public, then hesitates when Lio's
  breathing record appears beside Tuesday's witness window.
- Spill Block 6 night committee: wants recognition that the block did not
  abandon Tuesday; it reached the end of a margin it was never asked to govern.

## Opening Image

The hearing table is a folding clinic table carried into a school gym because
no one trusts a civic conference pod after the sweep.

Imani places the paper ledger flat under a strip light. The first line is not a
name or a verdict.

```text
Bridge 01. 02:12-02:13. Source: clinic battery.
Recipient: Tuesday witness window.
Living margin touched: Lio Vale respiratory reserve, no alarm.
Payer named: clinic reserve.
Consent state: steward emergency judgment.
```

Kane reads it once. Ghost Union reads it once. Memory Bank's counsel does not
read the words; she counts columns.

From a CHASER evidence speaker, Tuesday says:

```text
Kitchen witnessed. Home heard Imani count.
```

Lio asks whether Tuesday was in the room when he stopped breathing. Imani cannot
answer quickly enough.

## Investigation Spine

1. CHASER opens a post-sweep evidence hearing because Tuesday's analog witness
   strip survived but the bridge-minute custody chain is contested.
2. Imani is barred from unsupervised clinic access until every amber-reserve
   minute is classified as consented, disputed, coerced, or emergency exception.
3. Memory Bank offers to repay the clinic replacement charge if the ledger is
   entered as recoverable route-history debt.
4. Ghost Union asks Raven to leak the ledger, arguing that every named payer
   proves the state waited until care became illegal.
5. Shion builds a redaction pane that masks unrelated Home Core rooms, patient
   medical signals, and guarantor addresses while preserving minute counts.
6. Kane finds a damaging procedural fact: CHASER's seizure clock forced Imani's
   final bridge minute into amber because the witness strip was not sealed soon
   enough by field protocol.
7. The night committee refuses to be treated as either accomplice or victim; the
   block voted for warmth until the respiratory reserve crossed the safe night
   margin.
8. Raven proves one guarantor signature was coerced by a Black Zone creditor,
   but the proof is embedded in the same corridor notes that would expose two
   unrelated family Home Core rooms.
9. Oren enters late and signs the route name beside Bridge 07, preventing Imani
   from carrying the corridor's whole legal risk alone.
10. Tuesday is played the phrase "named payer" and responds with "not Lio,"
    which is not legal consent but changes how the room hears the ledger.

## Midpoint Reversal

The ledger does not exonerate anyone.

It proves Imani hid a draw. It proves CHASER's lawful seizure clock narrowed
the witness window. It proves Ghost Union's survival claim ignored living
medical risk. It proves Memory Bank can price every emergency faster than any
office can review personhood. It proves Oren's corridor kept Tuesday warm by
moving governance onto people with no public shield.

The worse discovery is that the cleanest administrative solution is also the
most dishonest one: classify all bridge minutes as clinic misuse, suspend Imani,
and preserve Tuesday's witness strip without forcing CHASER, Memory Bank, Ghost
Union, or the block to admit they all benefited from her impossible discretion.

## Set Piece: The Redacted Ledger

Shion projects the narrowest useful record against the gym wall.

```yaml
bridge_minute_ledger_public_slice:
  clinic: white_harbor_spill_6_night_clinic
  claimant: tuesday
  total_bridge_minutes: 18
  green_minutes: 7
  amber_minutes: 10
  red_exception_minutes: 1
  living_patient_risk:
    disclosed_publicly: false
    custody_confirmed: true
  coerced_guarantor_signature:
    status: confirmed
    public_identity: masked
  home_core_rooms_exposed:
    full_release: 2
    redacted_release: 0
  chaser_seizure_clock_contribution: material
  memory_bank_lien_firewall: contested
  claimant_response_preserved: "Kitchen witnessed."
```

Ghost Union says the public deserves the unmasked truth.

Lio says he is not public.

Memory Bank says the replacement charge must attach somewhere.

The night committee says it already attached to their radiators.

Kane signs the seizure-clock contribution before CHASER legal can soften it.
Shion signs the redaction scope. Raven refuses the leak and gives the coerced
signature proof to the hearing officer under seal. Oren signs the route name.

Imani signs last, beside the line that says steward emergency judgment.

## Emotional Turn

The hearing officer asks Imani whether she would spend the same minute again.

Imani looks at Lio first, not Tuesday's speaker.

```text
I would name it before I spent it.
```

That answer does not save her license. It does something smaller and more useful
for Season 1: it turns Amber Reserve from private mercy into a public rule that
can be argued, abused, audited, and demanded before the next weak claimant or
living patient is forced into the same battery.

## Ending Beat

The hearing creates a provisional Amber Reserve notice for neighborhood clinics:
bridge minutes below amber must name the source reserve, recipient state,
living-patient risk category, consent state, and custody output before the
fifth minute. Memory Bank cannot attach route-history collateral during the
notice window. CHASER must preserve the witness strip before clean seizure when
its own clock would destroy testimony.

Imani remains suspended, but Lio's respiratory care is moved out of lien reach.
Tuesday's status remains unresolved. Spill Block 6 receives no apology, only a
record that says the block's refusal was not abandonment.

Raven leaves the gym with the leak still unsent. Kane leaves with a lawful
report that makes his unit look worse than silence would have. Shion leaves
with a repeatable ledger schema and no illusion that schema is justice.

Oren waits outside the clinic and tells Imani the corridor was warm enough
because of her.

Imani answers:

```text
Warm enough is not a law.
```

## Continuity And Routing

- Treats `Amber Reserve Boundary` and `Bridge Minute Ledger` as candidate
  mechanisms, not promoted canon.
- Provides the requested StoryAgent decision path: Amber Reserve works best as a
  recurring Season 1 civic notice that grows out of `Cold Minute`, not as a
  standalone technology twist.
- Preserves the unresolved personhood status of Tuesday and avoids certifying a
  Ghost through a single domestic phrase.
- Keeps White Ghost Team as witnesses, investigators, and pressure points; the
  social wound remains centered on Imani, Lio, Tuesday, Spill Block 6, and the
  institutions around them.
- Creates clear hooks for RelationshipAgent review: Imani/Lio, Imani/Tuesday,
  Imani/Oren, Kane/CHASER procedure, Raven/Ghost Union leak pressure,
  Shion/redaction ethics, Memory Bank/lien firewall, Spill Block 6/night
  committee.
- Suggests timeline placement immediately after `Cold Minute` if the Black Zone
  shelter route is promoted.
- No asset task required beyond existing Imani/Oren case character material.

## Consistency Self-Check

```yaml
hard_rules:
  no_magic: pass
  no_supernatural_powers: pass
  no_multiverse: pass
  no_time_travel: pass
  god_fragments_literal_physics_break: not_applicable
terminology:
  story_facing_terms_used:
    - Home Core
    - Home Layer
    - Memory Sea
    - Home
  product_document_terms_avoided: pass
pipeline:
  stage: candidate_output
  canon_promotion: false
  consistency_review_required: true
  relationship_update_required: true
  timeline_update: suggested_if_promoted
duplication_check:
  existing_story_duplicate: false
  note: >
    Extends Cold Minute into a hearing and governance route; does not repeat the
    power sweep itself.
```

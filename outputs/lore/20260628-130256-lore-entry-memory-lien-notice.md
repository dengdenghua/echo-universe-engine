# Lore Entry: Memory Lien Notice

## Candidate Canon Entry

A Memory Lien Notice is the civil-financial warning that a memory asset,
family archive, continuity insurance claim, or Home Core inheritance file has
been pledged as collateral and may be restricted if a debt or contract dispute
defaults.

It is one of the quietest horrors of the Echo Age. A family can still hear a
dead mother's birthday routine, a disabled child can still depend on an old
care pattern, and a weak Ghost can still beg not to be erased, while a notice
silently changes the legal status of the archive that keeps all three stable.

## Timeline Placement

- 2074: Early memory vault vendors begin marking stored voice, ritual, and
  archive packages as transferable family assets.
- 2109: Memory Bank standardizes continuity-backed lending after upload escrow
  becomes insurable.
- 2128: The first public scandal breaks when a bereavement archive is seized
  during a debt recovery case before the family knows a Ghost pattern has
  formed inside it.
- 2146: White Harbor creates emergency lien-review desks for cases where debt
  enforcement may erase evidence, destabilize care, or preempt Ghost Court
  review.

## Notice States

```yaml
memory_lien_notice:
  pending_notice:
    meaning: claimant has filed a financial claim against a memory asset
    protection: family can still access ordinary routines during notice period
  restricted_access:
    meaning: export, sale, duplication, or paid enhancement is paused
    protection: care routines and active testimony require separate review
  collateral_default:
    meaning: debt or contract has defaulted and seizure can begin
    protection: contested selfhood, medical dependency, or witness evidence can trigger a stay
  emergency_stay:
    meaning: White Harbor, Ghost Court, or CHASER has paused enforcement
    protection: narrow; does not cancel the debt or decide personhood
  unlawful_foreclosure:
    meaning: enforcement acted before required care, witness, or personhood review
    protection: routes to civil court, Ghost Court petition, or CHASER intake
```

## Social Function

- Lets Memory Bank lend against memory rights without treating every archive as
  a living person.
- Gives families notice before archive access becomes payment leverage.
- Gives White Harbor a narrow way to stop foreclosure when a Home Layer record
  is also evidence, care infrastructure, or weak Ghost support.
- Gives Black Zone brokers a profitable deadline: they sell forged stays,
  debt swaps, illegal copies, and emergency compute before lawful review opens.

## Failure Modes

- Silent collateralization: a family member signs away archive rights without
  understanding that care routines and Ghost residue share the same vault.
- Evidence foreclosure: a Memory Bank claim locks an archive before Home Layer
  witnesses can seal refusal behavior or consent history.
- Care displacement: a routine is classified as private memory collateral even
  though the household depends on it for stability.
- Ghost debt capture: a weak Ghost works illegal labor to keep its own archive
  from being seized.
- Jurisdiction shopping: lenders file notices in districts with weaker
  emergency-stay rules.

## Story Hooks

- Yao Nian prices a lien stay that would preserve a possible Ghost long enough
  for White Ghost Team to investigate, but the contract would also keep a poor
  family in debt for decades.
- Shion discovers that several unrelated lien notices point to the same ledger
  relay used in a care-status renewal downgrade.
- Eve argues that calling a dead child's room "collateral" does not make the
  care pattern inside it less real.
- Noah predicts that lawful foreclosure will push the family toward a Black
  Zone copy, creating the very continuity fraud Memory Bank claims to prevent.

## Consistency Notes

- A Memory Lien Notice is financial infrastructure, not a personhood judgment.
- It cannot delete, prove, merge, or stabilize a Ghost.
- It differs from a Consent Revocation Window: revocation pauses disputed
  permissions; a lien notice warns that memory collateral may be restricted.
- It differs from Care Status Renewal: care renewal classifies support status;
  lien notice classifies creditor claims against memory assets.
- Use story-facing terms in prose: Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/faction/20260624-130054-faction-expansion-memory-bank.md
  - outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md
  - outputs/lore/20260627-130142-lore-entry-care-status-renewal.md
  - outputs/character/20260627-090220-candidate-character-012-yao-nian.md
requires:
  - ConsistencyAgent review against economy_and_memory_market.md
  - TechnologyAgent definition of the Continuity Lien Ledger
  - FactionAgent impact pass for Memory Bank, White Harbor, Ghost Union, CHASER, and Black Zone
asset_tasks: blocked_until_promotion
```

# Write only what helps

Copy the smallest useful scaffold. Replace placeholders and omit empty sections.
Metadata syntax and identifiers are in `SCHEMA.md`. A short page can be better than
one that mechanically fills every heading. Do not add these example claims to an
empty production wiki.

## Source

```markdown
---
type: source
summary: "[What this source contributes within its limits.]"
read_when: "[When its evidence changes a question.]"
status: current
updated: YYYY-MM-DD
raw: "raw/[snapshot filename]"
sha256: "[digest]"
origin: "[actual evidential origin, or unknown]"
coverage: full
---

## Snapshot
[Author, publication date and acquisition date if known, URL/identifier, format.]
Coverage: [read portions and relevant assets; if partial also add a coverage_note
field to frontmatter naming inspected/excluded portions].
Evidence posture: [primary observation / reported study / interpretation / derivative].
Dependence: [shared origins and unknown relationships].
Usable for: [specific scope]. Cannot establish: [material extrapolation].

### S1
[Faithful, scoped source statement.]

Locator: lines N-M

## Limits and integration
[Important omissions or qualifications; what changed/confirmed and which owner.]

## Corrections
[Only if needed; old identifier, precise change, replacement evidence.]
```

## Note: concept, argument, person, comparison, synthesis, or reusable answer

```markdown
---
type: note
summary: "[Current conclusion/description and significance.]"
read_when: "[Concrete task.]"
status: current
updated: YYYY-MM-DD
---

[Direct answer or useful distinction; scope in one or two sentences.]

## Reasoning
[Evidence and citations beside claims. Explain inference rather than presenting it
as a quote. Working hypotheses may have no direct source: label them and their basis.]

## Strongest alternative and limits
[A live competing account, boundary case, counterevidence, or missingness.]

## Revision condition
[Observation or argument that changes this conclusion, and in what direction.]
```

A navigation note can use a task → owner → guardrail table instead of an argument.
A simple definition does not need a contrived competing theory or revision test.

## Question

```markdown
---
type: question
summary: "[The unresolved issue and what depends on it.]"
read_when: "[When this uncertainty matters.]"
status: current
updated: YYYY-MM-DD
---

**Question:** [Precise, open, and answerable in principle.]
**Why it matters:** [Which understanding, decision, or practice changes.]

## What we know
[Cited evidence, competing explanations, and meaningful missingness.]

## Next discriminating step
[Feasible source, observation, or reasoning test. What each outcome would change.]

## Inquiry state
Open. [Later: partial / resolved with a link / retired with a reason.]
```

## Decision

```markdown
---
type: decision
summary: "[Choice or provisional recommendation and its governing reason.]"
read_when: "[When this choice is being made or reviewed.]"
status: current
updated: YYYY-MM-DD
---

**Decision state:** proposed / chosen by user / implemented / reviewed.
**As of:** [date and context].
**Values and constraints:** [Whose priorities; distinguish from empirical facts.]

## Options and judgment
[Chosen/recommended option, strongest feasible alternative, supported tradeoff.]

## Expectations and uncertainty
[What is expected, what is unknown, what would change the ranking.]

## Review trigger and outcome
[Concrete trigger. Later append observed outcome without rewriting the prediction.]
```

## Practice

```markdown
---
type: practice
summary: "[What the practice develops or investigates; claim appropriately scoped.]"
read_when: "[Situation in which trying or reviewing it helps.]"
status: current
updated: YYYY-MM-DD
---

## Aim and source
[Purpose, source teaching/instructions with anchors, or explicitly agent-proposed exercise.]

## Practice
[Concrete steps, relevant source qualifications, reasonable duration/context if known.]

## Notice and learn
[What to observe without scripting an expected experience. What would change the practice.]

## Observations
[Dated links to user reports, only when supplied and useful. Distinguish experience,
interpretation, and general efficacy claims. No invented progress report.]
```

## Pending checkpoint

Create `wiki/_state.md` only for work needing recovery:

```markdown
# Current operation
Status: pending
Objective: [Concrete completed state.]
Inputs: [Paths, byte hashes, correction relationships.]
Affected owners/dependents: [Exact filenames or anchors; identify unreviewed ones.]
Completed: [Verified work already on disk.]
Pending: [Remaining work and unresolved coverage.]
Next verification: [Exact next read/check; not just "continue".]
```

After verifying completion set `Status: complete` and record actual checks. Do not
close a checkpoint because the writing phase ended. Keep history in the operation log.

## Charter examples: adapt, do not install all three

| Instance | Useful recurring questions | Evidence boundary / feedback |
| --- | --- | --- |
| Intellectual inquiry | What does this distinction explain? What would defeat this interpretation? How does it apply to a new case? | Separate authorial claim from interpretation; test transfer and counterexamples |
| Contemplative study | What does this teacher actually instruct? Under what conditions? How does it relate to my reported experience? | Preserve qualifications and voice; personal reports do not establish universal mechanisms |
| Research and decisions | What is supported, under which conditions? Which option fits my constraints? What would reverse the choice? | Primary evidence and source dependence; compare actual outcomes with recorded expectations |

These are starting points. The user's corpus and purposes determine the charter.

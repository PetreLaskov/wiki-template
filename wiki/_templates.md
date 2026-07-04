# Templates

Scaffolds per page type. Copy the frontmatter and body for the type you're creating,
replace bracketed placeholders, prune sections that don't apply. Frontmatter fields are
documented in `AGENTS.md` § Frontmatter.

Conventions used below:

- `[bracketed]` text is a placeholder you replace.
- *Italic guidance* explains a section's intent; delete it from the finished page.
- `updated:` is set to today's date on creation and every meaningful revision.
- `tags:` is omitted from all scaffolds — add it only when a cross-cutting facet
  genuinely recurs across pages.

---

## source

*1:1 with a `raw/` file. A provenance ledger, not an essay. Other pages cite this page
(at claim level), never the raw file directly. **Length scales with novelty**: a source
that mostly confirms existing pages gets Snapshot + Reliability + Key Claims + Model
Delta in ~150-300 words and stops. Only a source that genuinely moves the model earns
the optional deep sections.*

    ---
    type: source
    thesis: "[What this source argues / contains, and what it changes in this wiki.]"
    load_when: "[Task shapes that need this source's claims or its reliability posture.]"
    status: live
    domain: [primary]
    importance: 5
    confidence: established
    aliases: []
    sources: [raw/filename.ext]
    src_bytes: [byte size of the raw file at ingest]
    updated: YYYY-MM-DD
    ---

    [One sentence locating the source: author, origin, date, format.]

    ## Snapshot
    - **Origin**: [author / venue / date — and how it reached raw/]
    - **Format**: [essay, transcript, auto-caption, AI-generated report, …]
    - **Reliability**: [tier per the charter's source posture]
    - **Usable for**: [what this source can support]
    - **Not usable for**: [what it must not be stretched to support]

    ## Key Claims
    - **S1** — [claim]. → owner: [[Concept A]]
    - **S2** — [claim]. → owner: [[Concept B]]
    - **S3** — [claim, unhoused — flagged for review]. *(house every claim you can)*

    ## Model Delta
    [The section that ties this ingest to the evolving whole. What this source changed,
    confirmed, challenged, or failed to change. Name the pages it moved. If the honest
    answer is "no material change", say so — and keep this whole page short.]

    ## Audit
    - **Weakest claims**: [most load-bearing claim with thinnest support]. *(or: none)*
    - **Important omissions**: [what a careful reader would expect but isn't here]. *(or: none)*
    - **Contradictions / tensions**: [conflicts with itself or with existing pages — link them]. *(or: none)*

    ## Summary
    *Optional — only when the delta is substantial.* [Compressed account, 1-3 paragraphs,
    faithful to the original. Enough to decide whether to read the raw file.]

    ## Notable Quotes
    *Optional.*
    > "[Direct quotation load-bearing for downstream pages.]" (S2)

    ## Related
    - [[Concept A]] — [what this source contributes to it]

---

## entity

*A real-world thing that warrants its own page: person, organization, system, place,
dataset, project. Aggregates information across sources.*

    ---
    type: entity
    thesis: "[What this entity is and why it earns a page — its distinguishing role here.]"
    load_when: "[Task shapes that need this entity's identity, role, or relations.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: established
    aliases: []
    sources: [raw/source-A.md]
    updated: YYYY-MM-DD
    ---

    [1-2 sentence definition: what kind of thing, and why it matters to the charter.]

    ## Key Facts
    - **Identity** — [what it is, when it existed / exists]
    - **Role** — [what it does, in this wiki's frame]
    - **Relations** — [the most important other entities it touches]

    ## Body
    [Aggregated across sources, cited at claim level ([[Source Page]] S2). When sources
    disagree, surface the disagreement — do not smooth it.]

    ## Related
    - [[Concept X]] — primary frame for understanding this entity

---

## concept

*An abstraction or principle — a load-bearing idea other pages build on. The workhorse
type: most of the model lives here, accumulating evidence across sources. A concept that
swells past ~2,000 words with separable concerns becomes a hub (see below).*

    ---
    type: concept
    thesis: "[Single-sentence definition + the claim that makes this concept load-bearing.]"
    load_when: "[Task shapes for which this page is the right first read.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: established
    aliases: []
    sources: [raw/source.md]
    updated: YYYY-MM-DD
    ---

    [Definition in plain language, 1-2 sentences. The first sentence should make sense
    to someone outside the domain.]

    ## Key Points
    - **Distinguishing feature** — what makes this not [[Adjacent Concept]].
    - **Operational use** — how it is applied in practice.
    - **Limits** — where it breaks down or stops being useful.

    ## Body
    [Full treatment: motivating examples, mechanism, contested aspects. Inline `[[links]]`,
    claims cited at anchor level ([[Source Page]] S4). This page owns its claims — other
    pages cite it rather than restating.]

    ## Boundaries
    *Optional — include when the concept is commonly overstretched.*
    [What this concept's claims must not be taken to cover.]

    ## Related
    - [[Adjacent Concept]] — boundary
    - [[Thesis Using This]] — application

### hub variant

*A hub is a role a `concept` or `synthesis` page takes on when it routes a cluster of
children. Add these sections to the scaffold above; keep the hub itself compact — it
routes, the children own the depth.*

    ## Decision Map
    | If the task asks about… | Load | Why | Guardrail |
    | --- | --- | --- | --- |
    | [question shape] | [[Child A]] | [what it owns] | [what not to overclaim] |

    ## Related
    - [[Child A]] — child page; owns [the mechanism / the taxonomy / …]
    - [[Child B]] — child page; owns […]

---

## thesis

*Argues a position from evidence. The wiki claiming something — the type that proves the
wiki is compiling understanding rather than summaries. Seek these; review flags domains
that accumulate evidence without ever arguing.*

    ---
    type: thesis
    thesis: "[The argument, in one sentence.]"
    load_when: "[Task shapes where this position (or its evidence) changes the answer.]"
    status: live
    domain: [primary, secondary]
    importance: 7
    confidence: probable
    aliases: []
    sources: [raw/source-A.md, raw/source-B.md]
    updated: YYYY-MM-DD
    ---

    [The claim restated with its significance. 1-2 sentences.]

    ## Key Points
    - **Premise 1** — [evidence] ([[Source Page]] S1).
    - **Premise 2** — [evidence].
    - **Inference** — [the move from premises to conclusion].
    - **Counter-considerations** — [what would weaken the thesis].

    ## Argument
    [Full case. Evidence linked at anchor level. Counterarguments addressed, not
    dismissed. The reader always knows what's established vs. inferred.]

    ## What would change my mind
    [Concrete observations that would demote confidence. If you can't name any, the
    thesis is tautological or under-specified.]

    ## Related
    - [[Counter-Thesis]] — opposing position (link bidirectionally)
    - [[Concept X]] — central frame

---

## synthesis

*Maps a domain or topic — names the through-line that holds a cluster together. A good
synthesis tells you what the territory looks like seen whole; a bad one enumerates pages.
Often serves as a domain's hub (add a Decision Map).*

    ---
    type: synthesis
    thesis: "[What this maps and the through-line that organizes the territory.]"
    load_when: "[Task shapes needing the domain seen whole, or entry routing into it.]"
    status: live
    domain: [primary]
    importance: 8
    confidence: probable
    aliases: []
    sources: []
    updated: YYYY-MM-DD
    ---

    [One paragraph: the territory, the through-line, who needs this map. If `sources: []`,
    note that this is pure synthesis drawing on existing pages.]

    ## Landscape
    - **Sub-area A** ([[Page A]], [[Page B]]) — what this cluster argues / contains.
    - **Sub-area B** ([[Page C]]) — …

    ## Through-line
    [The argument or pattern that organizes the landscape — why these belong together,
    understood rather than listed.]

    ## Open frontiers
    - [[Question X]] — why it matters

    ## Related
    - [[Adjacent Synthesis]] — boundary domain

---

## analysis

*A crystallized answer to a question likely to recur. Lighter than a thesis — analysis
answers; thesis argues. Cheap to create: any query whose answer took real assembly work
should leave one behind.*

    ---
    type: analysis
    thesis: "[What was asked and the conclusion, in one sentence.]"
    load_when: "[The recurring question shapes this answer serves.]"
    status: live
    domain: [primary]
    importance: 5
    confidence: probable
    aliases: []
    sources: [raw/source-A.md]
    updated: YYYY-MM-DD
    ---

    **Question:** [the prompt that triggered this analysis]

    **Answer:** [1-2 sentences. The conclusion, plainly stated.]

    ## Reasoning
    [Steps from question to answer. Evidence cited at anchor level. Alternatives
    considered and rejected, with reasons.]

    ## Confidence and limits
    [What would change the answer; what evidence is missing.]

    ## Related
    - [[Page A]] — used in answer
    - [[Question]] — origin (if this resolves an open question)

---

## question

*An open question, research gap, or knowledge frontier. First-class: questions record
what the wiki wants to know. Cheap to create: every query the wiki couldn't answer and
every unresolved tension between sources should leave one behind.*

    ---
    type: question
    thesis: "[The question, made precise — and why answering it would matter.]"
    load_when: "[Task shapes that should know this is open before answering confidently.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: speculative
    aliases: []
    sources: []
    updated: YYYY-MM-DD
    ---

    **Question:** [precise form — vague questions don't earn pages]

    **Why it matters:** [What changes downstream if answered? Which pages would move?]

    ## What we know
    - [[Page A]] — [bears on this how]

    ## What would resolve it
    - [evidence type, and where it might come from]

    ## Status
    Open  *(or: Partial → [[partial answer]], or: Resolved → [[resolution]] — resolved
    questions stay as a record of the inquiry)*

    ## Related
    - [[Adjacent Question]] — same frontier

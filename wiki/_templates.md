# Templates

Scaffolds per page type. Copy the frontmatter and body for the type you're
creating, replace bracketed placeholders, then prune sections that don't apply.
Frontmatter fields are documented in `AGENTS.md` § Frontmatter.

Conventions used below:

- `[bracketed]` text is a placeholder you replace.
- *Italic guidance* explains the intent of a section; delete it from the
  finished page.
- All templates assume `updated:` is set to today's date when the page is created
  or revised.

---

## source

*1:1 with a `raw/` file. Faithful summary plus extracted claims. The source
page is the contract between the raw file and the rest of the wiki — other
pages cite the source page, not the raw file directly. The audit sections
(Weakest Claims, Important Omissions, Contradictions / Tensions, Model Delta)
keep it honest about what the source does and does not establish.*

    ---
    type: source
    thesis: "[Single sentence: what this source argues / contains, and why it matters to the wiki.]"
    status: working
    domain: [primary]
    importance: 5
    confidence: established
    tags: []
    aliases: []
    sources: [raw/filename.ext]
    updated: YYYY-MM-DD
    ---

    [Author / origin / date / format. One sentence locating the source.]

    ## Key Claims
    - **[Claim 1]** — [supporting detail or page reference]. ([[Concept A]])
    - **[Claim 2]** — [supporting detail].
    - **[Claim 3]** — [supporting detail].

    ## Summary
    [Compressed account of the source. 1-3 paragraphs, faithful to the original;
    not yet integrated into wider wiki argument. The reader should be able to
    decide from this whether to read the raw file.]

    ## Weakest Claims
    - **[Claim]** — [the most load-bearing claim that is least supported; where the evidence is thin or missing]. *(or: none)*

    ## Important Omissions
    - [What a careful reader would expect this source to address but it does not]. *(or: none)*

    ## Contradictions / Tensions
    - [Where the source conflicts with itself, with other sources, or with existing wiki pages — link them]. *(or: none)*

    ## Model Delta
    [What this source changed, confirmed, challenged, or failed to change in the wiki's current model — the section that ties this ingest to the evolving whole. Name the pages it moves.]

    ## Notable Quotes
    > "[Direct quotation worth preserving — load-bearing for downstream pages.]"
    > — [page reference]

    ## Related
    - [[Entity X]] — [why this source bears on it]
    - [[Concept Y]] — [the source's central frame]

---

## entity

*A real-world thing that warrants its own page: a person, organization,
system, place, dataset, model, project. Aggregates information across
sources.*

    ---
    type: entity
    thesis: "[What this entity is and why it earns a page in this wiki — distinguishing role.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: established
    tags: []
    aliases: []
    sources: [raw/source-A.md, raw/source-B.md]
    updated: YYYY-MM-DD
    ---

    [1-2 sentence definition. What kind of thing is this, and why does it matter
    to the wiki's central concerns.]

    ## Key Facts
    - **Identity** — [what it is, when it existed / exists]
    - **Role / function** — [what it does, in this wiki's frame]
    - **Relations** — [the most important other entities it touches]

    ## Body
    [Aggregated information from sources. Cross-link to related entities and
    concepts inline. Cite sources via [[source-page]] for important claims.
    When sources disagree, surface the disagreement explicitly — do not smooth it.]

    ## Related
    - [[Concept X]] — primary frame for understanding this entity
    - [[Entity Y]] — [relation: e.g. "founded", "built", "succeeded"]

---

## concept

*An abstraction or principle — a load-bearing idea that other pages reference.
Defines, distinguishes, and bounds the concept.*

    ---
    type: concept
    thesis: "[Single-sentence definition + why this concept is load-bearing here.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: established
    tags: []
    aliases: []
    sources: [raw/source.md]
    updated: YYYY-MM-DD
    ---

    [Definition in plain language, 1-2 sentences. Resist jargon. The first
    sentence should make sense to someone outside the domain.]

    ## Key Points
    - **Distinguishing feature** — what makes this not [[Adjacent Concept]].
    - **Operational use** — how the concept is applied in practice.
    - **Limits** — where the concept breaks down or stops being useful.

    ## Body
    [Full treatment: motivating examples, formalization if relevant, history if
    relevant, contested aspects. Inline `[[links]]` to instances and adjacent
    concepts. Show, don't just tell — concrete examples earn their space.]

    ## Related
    - [[Adjacent Concept]] — boundary
    - [[Thesis Using This]] — application

---

## thesis

*Argues a position from evidence. The highest-value page type — a thesis is
the wiki claiming something, with reasoning and evidence to back it.*

    ---
    type: thesis
    thesis: "[The argument, in one sentence.]"
    status: working
    domain: [primary, secondary]
    importance: 7
    confidence: probable
    tags: []
    aliases: []
    sources: [raw/source-A.md, raw/source-B.md]
    updated: YYYY-MM-DD
    ---

    [The claim, restated to set context. 1-2 sentences. Why this matters.]

    ## Key Points
    - **Premise 1** — [supporting evidence] ([[source]]).
    - **Premise 2** — [supporting evidence].
    - **Inference** — [the move from premises to conclusion].
    - **Counter-considerations** — [what would weaken the thesis].

    ## Argument
    [Full case. Evidence linked. Counterarguments addressed, not dismissed.
    Distinguish what's established from what's inferred — the reader should
    always know which is which.]

    ## What would change my mind
    [Concrete observations or arguments that would lower confidence to
    `speculative` or move it to `contested`. If you can't name any, the thesis
    is probably either tautological or under-specified.]

    ## Related
    - [[Counter-Thesis]] — opposing position (link bidirectionally)
    - [[Concept X]] — central frame

---

## synthesis

*Maps a domain or topic. The synthesis names the through-line that holds a
cluster of pages together — what the territory looks like when seen as a
whole.*

    ---
    type: synthesis
    thesis: "[What this synthesis maps and the through-line that holds the territory together.]"
    status: working
    domain: [primary]
    importance: 8
    confidence: probable
    tags: []
    aliases: []
    sources: []
    updated: YYYY-MM-DD
    ---

    [One paragraph: the territory, the through-line, who needs this map. If this
    page has `sources: []`, note in the body that it's a pure synthesis
    drawing on the wiki's existing pages.]

    ## Landscape
    - **Sub-area A** ([[Page A]], [[Page B]]) — what this cluster argues / contains.
    - **Sub-area B** ([[Page C]], [[Page D]]) — …
    - **Sub-area C** ([[Page E]]) — …

    ## Through-line
    [The argument or pattern that organizes the landscape. Why these sub-areas
    belong together. What the field looks like when seen as a whole — not just
    listed but understood.]

    ## Open frontiers
    - [[Question X]] — why it matters
    - [[Question Y]] — what would resolve it

    ## Related
    - [[Adjacent Synthesis]] — boundary domain
    - [[Foundational Concept]] — frame this synthesis assumes

---

## analysis

*A query-generated comparison or investigation. Crystallized answer to a
question that's likely to recur. Lighter weight than a thesis — analysis
answers; thesis argues.*

    ---
    type: analysis
    thesis: "[What was asked and the conclusion in one sentence.]"
    status: working
    domain: [primary]
    importance: 5
    confidence: probable
    tags: []
    aliases: []
    sources: [raw/source-A.md]
    updated: YYYY-MM-DD
    ---

    **Question:** [the prompt that triggered this analysis]

    **Answer:** [1-2 sentences. The conclusion, plainly stated.]

    ## Reasoning
    [Steps from question to answer. Evidence cited inline. Alternative
    conclusions considered and rejected, with reasons.]

    ## Confidence and limits
    [What would change the answer. What evidence is missing. What would
    promote this from `probable` to `established` (or demote it to
    `speculative`).]

    ## Related
    - [[Page A]], [[Page B]] — used in answer
    - [[Question]] — origin (if this analysis resolves an open question)

---

## question

*An open question, research gap, or knowledge frontier. Questions are
first-class citizens — they record what we want to know, not just what we
already know.*

    ---
    type: question
    thesis: "[The question, made precise — and why answering it would matter.]"
    status: seed
    domain: [primary]
    importance: 5
    confidence: speculative
    tags: [open-question]
    aliases: []
    sources: []
    updated: YYYY-MM-DD
    ---

    **Question:** [the precise form of the question — vague questions don't earn pages]

    **Why it matters:** [1-2 sentences. What changes downstream if this is
    answered? Which pages would need updating?]

    ## What we know
    - [[Page A]] — [bears on this how]
    - [[Page B]] — [bears on this how]

    ## What would resolve it
    - **Evidence type 1** — [what kind of evidence, and where it might come from]
    - **Evidence type 2** — …

    ## Status
    Open  *(or: Partial → [[partial answer page]], or: Resolved → [[resolution page]])*

    ## Related
    - [[Adjacent Question]] — same frontier
    - [[Concept X]] — the question's central frame

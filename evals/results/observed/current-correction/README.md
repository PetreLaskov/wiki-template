# Your Knowledge Compiler

Open this folder in your agent. Ask it to read `AGENTS.md`, then describe your
purpose, recurring questions, and a real task. Add source snapshots to `raw/`.
The agent maintains `wiki/`; you can read it in any Markdown editor.

Start with [the index](wiki/index.md). [Workflows](docs/WORKFLOWS.md),
[schema](docs/SCHEMA.md), and [templates](docs/TEMPLATES.md) are available on demand.

Python 3.10+; standard library only:

```text
python tools/kc.py status
python tools/kc.py search "your question"
python tools/kc.py check
```

For research, migration, software tests, and behavioral evaluation, return to the
template repository used to create this instance. Those development materials and
their grading keys are deliberately not copied into your working knowledge base.

# Claude Compatibility Adapter

`AGENTS.md` is the canonical operating contract for this Knowledge Compiler.
Claude Code, Codex, Cursor, and other agents all read and follow the same contract.

When operating this repo:

1. Read `AGENTS.md` — the contract, including the First Read budget.
2. Follow it: `wiki/index.md` first (charter, state of the model, routing), newest ~10
   entries of `wiki/log.md`, `wiki/_state.md` resume point if ingesting.
3. Use `wiki/_operations.md`, `wiki/_templates.md`, and `.claude/commands/` on demand.
4. Verify mechanically with `python tools/lint.py` — don't count by hand.

Do not maintain a separate Claude-specific contract here. If this adapter ever
contradicts `AGENTS.md`, `AGENTS.md` wins.

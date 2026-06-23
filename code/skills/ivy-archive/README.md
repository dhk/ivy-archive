# ivy-archive skill (vendored source)

This is the version-controlled source of the **ivy-archive** Claude Code skill. The live,
installed copy runs from `~/.claude/skills/ivy-archive/`; this directory is the canonical
copy that travels with the design repo so the implementation and the
[system design](../../../docs/system-design.md) stay in sync.

## Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill itself (v2.0) — modes: sweep, collect, push, miso, query, status |
| `config.example` | Template for `~/.claude/skills/ivy-archive/config` |

## Install / update

```bash
cp code/skills/ivy-archive/SKILL.md ~/.claude/skills/ivy-archive/SKILL.md
cp code/skills/ivy-archive/config.example ~/.claude/skills/ivy-archive/config   # then edit paths
```

The skill also maintains state files alongside the config (`.last-sweep`, `.last-collect`,
`.last-nlm-push`) — those are runtime state, not vendored.

## What it does

Sweeps `.scratch/*.md` snapshots and Captain's Logs, collects them into the
`ivy-archive-private` git repo (`snapshots/<repo>/`, with provenance headers), and pushes to
both GitHub and a NotebookLM notebook. `miso` runs the whole pipeline in one command. See the
[system design](../../../docs/system-design.md) for the architecture and Build Log.

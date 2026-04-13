# Ivy Skills

## How to detect mode

Check for a `.ivy` file at the repo root (or walk up from the current directory).

- **Found `.ivy`** → you're in an Ivy-enabled repo. Use the repo structure: `snapshots/`, `maps/`, `concepts/`, `artifacts/`, `templates/`, `scripts/`.
- **No `.ivy`** → scratch mode. Save to `.ivy-scratch.md` in the current directory. Append structured blocks. The user can promote scratch content to a proper Ivy repo later.

## Available skills

| Skill | File | What it does |
|---|---|---|
| Session Start | `prompts/session-start.md` | Entry protocol — orient and prove readiness |
| Capture Snapshot | `prompts/capture-snapshot.md` | Turn a session into a structured snapshot |
| Update Map | `prompts/update-map.md` | Add a node to the initiative map |
| Handoff | `prompts/handoff.md` | Prepare context brief for switching tools |

## How to install

### Claude Code

Copy skill files into `.claude/commands/` (repo-level or user-level):

```bash
# repo-level (available in this repo only)
mkdir -p .claude/commands
cp prompts/capture-snapshot.md .claude/commands/capture-snapshot.md

# user-level (available everywhere)
mkdir -p ~/.claude/commands
cp prompts/capture-snapshot.md ~/.claude/commands/ivy-capture-snapshot.md
```

Skills become available as `/capture-snapshot` (or `/ivy-capture-snapshot`).

### Claude Desktop

Copy the prompt text from any skill file and paste it into a new conversation. No install required — the prompt IS the skill.

### Other tools

Each skill file contains full instructions the agent can follow. Paste the file contents as a system prompt or initial message.

## After the ready signal

If you are an agent that just completed the Ivy entry protocol and uttered the ready signal: check whether `prompts/index.md` exists. If it does, say:

> "I found skills available for this system. Want me to show you what's available?"

Wait for the user to respond. Do not list skills unless asked.

# Handoff

Prepare a context brief for switching to a different tool or starting a new session.

## Steps

### 1. Detect mode

Look for `.ivy` in the repo root.

- **Ivy mode**: proceed to step 2.
- **Scratch mode**: read `.ivy-scratch.md` and output it as the handoff document. Tell the user to paste it into the next tool. Stop.

### 2. Capture current session first

Before handing off, ask:

> "Should I capture this session as a snapshot before handing off?"

If yes, follow `prompts/capture-snapshot.md`. If the session produced changes, also follow `prompts/update-map.md` to add the new snapshot to the map.

### 3. Generate the handoff brief

Read the initiative map. Output a self-contained handoff document:

```markdown
# Handoff: [initiative name]

## Repo
[repo URL or path]

## Entry point
Read `maps/[map-file].md` and follow the context graph.

## What happened this session
[1-3 bullet summary of what was done]

## Active task
[What the user was working on, or "none — ask the user"]

## Open questions
[From the most recent snapshot]

## Files changed this session
[List of files modified/created, if any]
```

### 4. Provide tool-specific instructions

#### If the next tool has GitHub MCP
Give the user the session start prompt from `prompts/session-start.md`.

#### If the next tool has no MCP
Tell the user to paste the handoff document and the map contents into the new session.

#### If the next tool is Claude Code
Tell the user to open the repo and run:
```
Read maps/[map-file].md and orient yourself. Then [active task].
```

### 5. Confirm

Tell the user the handoff is ready and what to paste into the next tool.

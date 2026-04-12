---
id: artifact-ivy-session-start-prompt
title: Ivy session start prompt
date: 2026-04-12
type: artifact
visibility: public-safe
lifecycle_state: draft
topics:
  - knowledge-management
  - context-management
projects:
  - ivy-the-archive
created_at: 2026-04-12T16:30:00-07:00
updated_at: 2026-04-12T16:30:00-07:00
source_snapshot: snap-2026-04-12-ivy-context-streams
---

# Ivy session start prompt

## Purpose

A reusable prompt for starting a new Claude session on the Ivy Archive project. Assumes Claude has GitHub MCP access to `dhk/ivy-archive` and can read files directly from the repo.

## Usage

Paste this at the start of a new Claude Desktop session (or any Claude session with GitHub MCP connected). Adjust the active task line to match what you're working on.

## Inputs

- GitHub MCP connected to `dhk/ivy-archive`
- Optional: a specific task you want to work on

## Outputs

- Claude oriented to the current state of the project
- Summary of open questions and last decisions
- Ready to work

---

## Prompt

```
I'm working on the Ivy Archive project. Repo: dhk/ivy-archive on GitHub.

Please:
1. Read maps/ivy-improvement-context.md
2. Summarise: active initiative, last decisions made, open questions
3. Tell me what branch to work on
4. Ask me what I want to do today
```

---

## Notes

- The map is the entry point. Claude reads it, orients itself, then asks for direction.
- With GitHub MCP, Claude can read, commit, and push directly — no manual git commands needed unless MCP is unavailable (see the MCP-absent save pattern in `snap-2026-03-26-ivy-system-context`).
- If the map is stale (new snapshots exist that aren't listed as nodes), tell Claude to check `registry/snapshots.csv` for anything newer than the map's `updated_at`.

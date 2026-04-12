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
updated_at: 2026-04-12T17:00:00-07:00
source_snapshot: snap-2026-04-12-ivy-context-streams
---

# Ivy session start prompt

## Purpose

A reusable entry protocol for starting a new session on the Ivy Archive project. Works as a "hello world" and a validation: the tool assembles context by following the links in the repo, then signals readiness with a structured confirmation. You can check the confirmation before trusting the tool to work.

## Usage

Paste the prompt below at the start of any new Claude session with GitHub MCP connected to `dhk/ivy-archive`. No file pasting required — the tool reads the repo directly and follows the context graph.

## Inputs

- GitHub MCP connected to `dhk/ivy-archive`

## Outputs

- Tool has read and assembled context from the repo
- Structured readiness confirmation you can validate
- Session ready to begin

---

## Prompt

```
You have GitHub MCP access. Connect to repo dhk/ivy-archive.

Follow the context graph:
1. Read maps/ivy-improvement-context.md — start here
2. Read each node it lists, in order
3. Check registry/snapshots.csv for objects with an updated_at newer than
   the map's updated_at — read those too if any exist

When done, confirm you're ready:
- Active initiative and scope (one sentence)
- Last decision made (one sentence)
- Open questions still live (bullet list)
- Current branch to work on
- End with the ready signal. You'll need to find it.

Don't ask what to do next. Just confirm.
```

---

## What a good confirmation looks like

```
Active initiative: improving the Ivy Archive system — its design, schema,
tooling, and working conventions. Runs as a single repo (dhk/ivy-archive).

Last decision: adopted single-repo model; visibility frontmatter field is
the sole privacy boundary, no ivy-archive-private needed.

Open questions:
- Should initiative become a formal object type?
- How should the map be kept current as snapshots accumulate?
- When do synthesis snapshots become necessary, and what triggers them?
- What should the CI guard look like for public repos?

Branch: main (no active work branch — ready to create one for new work).

Ivy is live.
```

The final line is the ready signal. It can only be found by reading the map. Its presence proves the agent completed orientation.

---

## Notes

- The confirmation is the validation. If it's wrong or thin, the tool didn't load context properly — ask it to re-read before proceeding.
- The protocol is self-guiding: the map tells the tool what to read, and each object's `related_snapshots` / `related_concepts` fields reinforce the graph. The tool should follow links, not just read what it's explicitly told.
- With GitHub MCP, Claude can read, commit, and push directly. If MCP is unavailable, fall back to the git/gh CLI commands in the MCP-absent save pattern (`snap-2026-03-26-ivy-system-context`, Reusable patterns section).

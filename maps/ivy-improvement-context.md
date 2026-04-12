---
id: map-ivy-improvement-context
title: Ivy improvement — context brief
date: 2026-04-12
type: map
visibility: public-safe
lifecycle_state: draft
topics:
  - knowledge-management
  - context-management
  - system-design
projects:
  - ivy-the-archive
created_at: 2026-04-12T15:45:00-07:00
updated_at: 2026-04-12T15:45:00-07:00
linked_ids:
  - snap-2026-03-26-ivy-system-context
  - snap-2026-04-12-ivy-context-streams
  - concept-initiative
---

# Ivy improvement — context brief

> Hand this map to a new tool or use it to re-orient at the start of a session.
> Read the nodes in order. Skip paths you don't need.

---

## Scope

**Initiative:** improving the Ivy Archive system itself — its design, schema, tooling, and working conventions.

**Repo:** `dhk/ivy-archive` (public infrastructure repo). Content snapshots live here during bootstrapping; the intended long-term home for snapshot content is `ivy-archive-private`.

**Branch convention:** Claude Code work branches (`claude/some-task`) are ephemeral. Snapshots merge to `main`. Initiatives are metadata scopes, not branches.

**What is Ivy?** A structured, Git-backed knowledge system. The central unit is the snapshot — a concise, structured record of a single unit of thinking. Everything else (concepts, artifacts, maps) is extracted from or built on snapshots.

---

## Nodes

Ordered from foundational to most recent. Read in sequence on first orientation; jump by label when returning.

### [foundation] System design and architecture
**`snap-2026-03-26-ivy-system-context`**
`snapshots/2026-03-26__ivy__system-context.md`

What Ivy is, how it works, and the core v1 decisions. The two-repo model, snapshot schema, validation approach, lifecycle rules, and registry model. Start here.

Also covers: the MCP-absent save pattern (git/gh CLI fallback when no GitHub integration is available).

---

### [concept] Initiative
**`concept-initiative`**
`concepts/concept-initiative.md`

Defines what an initiative is: a bounded body of work with a metadata scope and an owned context brief. Explains why branches are not context streams, and how maps serve as handoff artifacts. Read before starting new bounded work.

---

### [decision] Context streams and the initiative concept
**`snap-2026-04-12-ivy-context-streams`**
`snapshots/2026-04-12__ivy__context-streams.md`

The session where the context streams gap in v1 was identified. Records the decision to use `projects` + maps for context scoping, and to define `initiative` as a first-class concept. Contains open questions about whether `initiative` needs a formal object type.

---

### [infrastructure] Key files

These are readable documents — not snapshots, but essential orientation:

| Label | Path | What it is |
|---|---|---|
| readable | `docs/ivy-design.md` | Full system design, two-repo model, commands |
| readable | `docs/spec.md` | v1 specification — schema, enums, lifecycle, registry |
| readable | `protocols/snapshot-schema.md` | Snapshot schema with Links section convention |
| readable | `protocols/validation-rules.md` | Validation levels and lifecycle transition rules |
| readable | `docs/first-10-snapshots-playbook.md` | Quality bar for early snapshots |
| reference | `scripts/validate.py` | Run with `IVY_CONTENT_ROOT` set |
| reference | `scripts/build_registry.py` | Regenerates all registry CSVs |

---

## Paths

### Path A — New tool, first session
> You have no prior context. Orient from scratch.

1. Read this map (you're doing it)
2. Read `snap-2026-03-26-ivy-system-context` — understand what Ivy is and the core decisions
3. Read `concept-initiative` — understand how context is scoped
4. Check `registry/snapshots.csv` for anything added since this map was last updated
5. Ask: what is the active task?

---

### Path B — Returning session, continuing improvement work
> You've worked on this before. Re-orient quickly.

1. Skim this map's Nodes section
2. Read `snap-2026-04-12-ivy-context-streams` for the latest decisions and open questions
3. Check `registry/snapshots.csv` for new snapshots since your last session
4. Resume from the open questions or follow-up actions in the most recent snapshot

---

### Path C — Handing off to a different tool
> You're switching from Claude to ChatGPT, Gemini, etc.

1. Give the new tool this map file
2. Give it the snapshots listed in Nodes (in order)
3. State the active task explicitly — don't assume the new tool will infer it
4. If the session produced new snapshots, add them to this map's Nodes before handing off

---

## Open questions

- Should `initiative` become a formal Ivy object type (ID prefix `init-`, validator support, own template)?
- How should this map be updated as new snapshots are added — manually, or via a script that reads `edges.csv`?
- When `ivy-archive-private` exists, do maps live there or in the public infrastructure repo?

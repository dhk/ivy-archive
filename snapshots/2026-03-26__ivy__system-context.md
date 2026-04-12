---
id: snap-2026-03-26-ivy-system-context
title: Ivy Archive system design and context
date: 2026-03-26
source: claude
source_ref: null
type: planning-session
visibility: public-safe
lifecycle_state: reviewed
topics:
  - knowledge-management
  - repo-architecture
  - system-design
projects:
  - ivy-the-archive
people: []
tags: []
related_snapshots: []
related_concepts: []
related_artifacts: []
derived_from: []
produced: []
confidence: high
summary_status: complete
created_at: 2026-03-26T08:26:36-07:00
updated_at: 2026-04-12T14:00:00-07:00
reviewed_at: 2026-04-12T14:00:00-07:00
published_at: null
---

# Ivy Archive system design and context

## Snapshot precis

The Ivy Archive is a structured, repo-backed knowledge management system. This snapshot captures the foundational design context: what Ivy is, how it works, and the core decisions that define its v1 architecture.

## Prompt / Trigger

Need to orient any collaborator or AI agent to the Ivy system quickly — establishing the canonical context for all future work.

## Context

Ivy was designed to solve a specific problem: valuable thinking produced in AI conversations is ephemeral. It disappears into chat logs, gets reinvented across sessions, and is not reusable.

Ivy turns that thinking into durable, structured markdown objects stored in a Git repo.

The system runs as two repos:

- **Public repo** (`ivy-archive`): infrastructure — docs, protocols, scripts, templates
- **Private repo** (`ivy-archive-private`): canonical knowledge content — snapshots, concepts, artifacts, maps

Tooling targets content via the `IVY_CONTENT_ROOT` environment variable.

## Key ideas

- The **snapshot** is the canonical unit of capture — one session, one unit of thinking
- Objects live in four typed folders: `snapshots/`, `concepts/`, `artifacts/`, `maps/`
- Visibility is metadata (frontmatter `visibility` field), never folder placement
- Registry CSVs are generated outputs, not source of truth — markdown files are
- Validation enforces schema consistency and runs locally (pre-commit) and in CI
- Lifecycle transitions are explicit: `draft → reviewed → published → archived`; `draft → published` is disallowed

## Decisions

1. Two-repo model: infrastructure is public, content is private. Tooling bridges them via env var.
2. Markdown-first: all canonical storage is plain markdown with YAML frontmatter.
3. Snapshot-first capture: everything starts as a snapshot. Artifacts and concepts are extracted from snapshots, not created independently.
4. Private-by-default: visibility defaults to `private`; promotion requires explicit metadata change and lifecycle transition.
5. No `src/` in v1: packaged library boundary deferred until a clear need exists.
6. Validation is non-optional: invalid files are errors, not warnings. The registry is not manually edited.

## Reusable patterns

- **Context snapshot pattern**: The first snapshot for any project or system should capture the design context — what it is, why it exists, core decisions. This makes the system self-documenting from the start.
- **Two-repo separation**: Separate infrastructure (public, versioned tooling) from content (private, personal/team data). Bridge with an env var.
- **Metadata-over-folder**: Encode classification in frontmatter fields, not directory paths. This keeps canonical storage simple and refactoring cheap.
- **Registry-as-output**: Treat registries/indexes as derived outputs. Source of truth is the canonical files. Regenerate don't maintain.

## Artifacts created

- `templates/snapshot.md` — blank snapshot template following the schema
- `protocols/snapshot-schema.md` — full schema definition with enums and rules
- `protocols/validation-rules.md` — validation levels, checks, and lifecycle rules
- `scripts/validate.py` — validation script targeting `IVY_CONTENT_ROOT`
- `scripts/build_registry.py` — registry generation script

## Open questions

- When should `outlines/`, `prompts/`, and `code/` directories be populated?
- What triggers the creation of a concept vs leaving the idea in the snapshot?
- Should the public repo ever contain example/demo snapshots?

## Follow-up actions

- Create `concept-context-snapshot` concept file defining the context snapshot pattern
- Populate `registry/snapshots.csv` by running `build_registry.py`
- Establish first 10 snapshots following the playbook in `docs/first-10-snapshots-playbook.md`

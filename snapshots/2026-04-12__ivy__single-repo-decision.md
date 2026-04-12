---
id: snap-2026-04-12-ivy-single-repo-decision
title: Decision — single-repo model for Ivy
date: 2026-04-12
source: claude
source_ref: null
type: decision-record
visibility: public-safe
lifecycle_state: draft
topics:
  - knowledge-management
  - repo-architecture
  - system-design
projects:
  - ivy-the-archive
people: []
tags: []
related_snapshots:
  - snap-2026-03-26-ivy-system-context
  - snap-2026-04-12-ivy-context-streams
related_concepts: []
related_artifacts: []
derived_from:
  - snap-2026-03-26-ivy-system-context
produced: []
confidence: high
summary_status: complete
created_at: 2026-04-12T16:00:00-07:00
updated_at: 2026-04-12T16:00:00-07:00
reviewed_at: null
published_at: null
---

# Decision — single-repo model for Ivy

## Snapshot precis

Reversal of the v1 two-repo model. Ivy now runs as a single repo. The `visibility` frontmatter field is the sole privacy boundary. The two-repo split is available as a future option if sensitive content accumulates.

## Prompt / Trigger

User questioned whether `ivy-archive-private` was actually necessary. All content created to date is `public-safe`. The two-repo model was adding operational complexity without benefit.

## Context

Ivy v1 was designed with a two-repo model:
- `ivy-archive` (public): infrastructure — docs, protocols, scripts, templates
- `ivy-archive-private` (private): canonical content — snapshots, concepts, artifacts, maps

Tooling bridged them via `IVY_CONTENT_ROOT` env var.

The original rationale: content may be sensitive (personal notes, client work, strategic thinking). Structural separation was the safest default.

In practice: the content created so far is entirely `public-safe`. The private repo doesn't exist yet. The env var requirement adds friction. And the `visibility` field already provides explicit, auditable privacy classification on every object.

## Key ideas

- The `visibility` field forces an explicit privacy decision on every object — this is a stronger guarantee than hoping sensitive content ends up in the right repo
- Structural separation (two repos) is a blunt instrument; metadata separation is more granular and more portable
- For content that is primarily public-safe, the two-repo split is pure overhead
- If sensitive content does accumulate later, migration is straightforward: visibility metadata tells you exactly what to move
- A CI guard on a public repo (block push if `visibility: private` or `visibility: sensitive` objects exist) provides a safety net without requiring a second repo

## Decisions

1. **Single repo.** Infrastructure and content live in `ivy-archive`. No `ivy-archive-private`.
2. **`visibility` field is the sole privacy boundary.** Every object must have an explicit visibility value; validation enforces this.
3. **`IVY_CONTENT_ROOT` retained as optional override.** For anyone who does want to split content into a separate directory, the mechanism still works.
4. **CI guard recommended.** A public repo should block push if any object has `visibility: private` or `visibility: sensitive`.
5. **Design docs updated** to reflect the single-repo model (v1.2).

## Reusable patterns

- **Metadata as the privacy boundary**: rather than using directory structure or repo separation to enforce privacy, encode it in frontmatter. Auditable, portable, and survives repo reorganisation.
- **Defer structural complexity until the need is proven**: the two-repo model solved a problem that hadn't materialised. Build the simplest thing that works; add structure when the friction of not having it becomes real.

## Artifacts created

- Updated `docs/ivy-design.md` to v1.2 — single-repo model, updated commands, CI guard recommendation
- Updated `docs/spec.md` — single-repo model section

## Open questions

- What should the CI guard look like? A script in `scripts/` that checks visibility on all canonical objects and exits non-zero if private/sensitive content is found in a public repo context?
- Should `validate.py` gain a `--public-repo` flag that makes private/sensitive objects an error rather than a warning?

## Follow-up actions

- Implement CI guard script (or add `--public-repo` flag to `validate.py`)
- Merge `claude/read-context-snapshot-RXn5X` to `main` — content is coherent and ready to publish

## Links

- [readable] docs/ivy-design.md — updated design document (v1.2)
- [readable] docs/spec.md — updated specification
- [reference] snap-2026-03-26-ivy-system-context — original snapshot where two-repo model was documented

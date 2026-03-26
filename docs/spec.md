# Ivy Specification (v1)

## Repo model

Recommended deployment is two repos:

- public repo: architecture docs, scripts, templates
- private repo: canonical knowledge objects and sensitive notes

Tooling can target private content using `IVY_CONTENT_ROOT`.

## Non-negotiable rules (v1)

1. Canonical-home rule
Every canonical object has exactly one home in `snapshots/`, `concepts/`, `artifacts/`, or `maps/`.

2. Metadata-over-folder rule
Visibility is metadata in frontmatter (`visibility`), never encoded by canonical storage path.

3. Infrastructure-vs-content rule
Infrastructure lives in `docs/`, `protocols/`, `templates/`, and `scripts/`.
Archive content lives in `snapshots/`, `concepts/`, `maps/`, and `artifacts/`.

## Canonical storage policy

Canonical objects live only in object folders:

- `snapshots/`
- `concepts/`
- `artifacts/`
- `maps/`

Visibility is encoded in metadata, not directory placement.

## Snapshot frontmatter schema

All snapshot files must use YAML frontmatter delimited by `---`.

```yaml
---
id: snap-2026-03-24-ivy-repo-architecture
title: Ivy repo architecture design
date: 2026-03-24
source: chatgpt
source_ref: null
type: planning-session
visibility: private
lifecycle_state: draft
topics:
  - knowledge-management
  - repo-architecture
projects:
  - ivy-the-archive
people:
  - Dave Holmes-Kinsella
tags: []
related_snapshots: []
related_concepts:
  - concept-context-snapshot
related_artifacts:
  - artifact-snapshot-schema-template
derived_from: []
produced: []
confidence: medium
summary_status: complete
created_at: 2026-03-24T18:10:00-07:00
updated_at: 2026-03-24T18:10:00-07:00
reviewed_at: null
published_at: null
---
```

## Required snapshot keys

- `id`
- `title`
- `date`
- `source`
- `type`
- `visibility`
- `lifecycle_state`
- `topics`
- `projects`
- `created_at`
- `updated_at`

## Optional snapshot keys

- `people`
- `related_snapshots`
- `related_concepts`
- `related_artifacts`
- `derived_from`
- `produced`
- `tags`
- `confidence`
- `source_ref`
- `summary_status`
- `reviewed_at`
- `published_at`

## Required snapshot sections

Each snapshot body must contain each heading exactly once:

- `## Snapshot precis`
- `## Prompt / Trigger`
- `## Context`
- `## Key ideas`
- `## Decisions`
- `## Reusable patterns`
- `## Artifacts created`
- `## Open questions`
- `## Follow-up actions`

## Enums

### source

- `chatgpt`
- `claude`
- `gemini`
- `notebooklm`
- `manual`
- `email`
- `meeting`
- `document`
- `other`

### type (snapshot)

- `conversation`
- `planning-session`
- `writing-session`
- `work-session`
- `research-session`
- `review-session`
- `design-session`
- `decision-record`

### visibility

- `private`
- `sensitive`
- `needs-review`
- `public-safe`

### lifecycle_state

- `draft`
- `reviewed`
- `published`
- `archived`

### confidence

- `low`
- `medium`
- `high`

### summary_status

- `partial`
- `complete`

## ID and file naming

- Snapshot ID pattern: `snap-YYYY-MM-DD-short-slug` (suffix `-2`, `-3`, ... on collision)
- Snapshot filename pattern: `YYYY-MM-DD__domain__slug.md`
- IDs are globally unique across all canonical object types

## Lifecycle transitions

Allowed transitions:

- `draft -> reviewed`
- `reviewed -> published`
- `reviewed -> archived`
- `published -> archived`
- `published -> reviewed` (reversal/correction)
- `draft -> archived` (exceptional)

Disallowed direct transition:

- `draft -> published`

## Registry model

Canonical markdown files are the source of truth.

Registry files are generated and rewritten on each run:

- `registry/snapshots.csv`
- `registry/concepts.csv`
- `registry/artifacts.csv`
- `registry/maps.csv`
- `registry/edges.csv` (optional relations)

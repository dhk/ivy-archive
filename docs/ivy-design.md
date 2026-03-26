# Ivy Design

Status: Draft v1.1

## Purpose

Ivy is a repo-backed knowledge archive for capturing, structuring, retrieving, and operationalizing conversations, decisions, artifacts, and durable concepts.

This document reflects the implemented v1 architecture.

## Executive summary

Ivy converts ephemeral thinking into durable, structured markdown objects.

Core object types:
- Snapshots
- Concepts
- Artifacts
- Maps

The snapshot is the canonical unit of capture.

## Core principles

- Markdown-first canonical storage
- Git-backed durability and version history
- Snapshot-first capture model
- Private-by-default workflow
- Machine-usable metadata + human-readable docs

## Non-negotiable rules (v1)

1. Canonical-home rule
Every canonical object has exactly one home in one object folder.

2. Metadata-over-folder rule
Visibility is encoded in frontmatter (`visibility`), not canonical path.

3. Infrastructure-vs-content rule
Infrastructure and content are separated to preserve clarity.

## Repo model

Ivy runs as two repos:

- Public repo (`ivy-archive`): infrastructure
  - `docs/`
  - `protocols/`
  - `templates/`
  - `scripts/`
- Private repo (`ivy-archive-private`): canonical content
  - `snapshots/`
  - `concepts/`
  - `artifacts/`
  - `maps/`

Tooling in the public repo targets private content via:

```bash
IVY_CONTENT_ROOT=/Users/dhk/Documents/dev/ivy-archive-private
```

## Public repo structure (infrastructure)

```text
ivy-archive/
  README.md
  docs/
  protocols/
  templates/
  scripts/
  inbox/
  public/approved/
  private/
  sensitive/
  registry/
```

Note: `src/` is intentionally omitted in v1. It can be introduced later when a true packaged app/library boundary exists.

## Private repo structure (content)

```text
ivy-archive-private/
  snapshots/
  concepts/
  artifacts/
  maps/
  inbox/raw/
  inbox/to-process/
  public/approved/
  private/
  sensitive/
  registry/
```

## Snapshot schema (v1)

Required frontmatter keys:
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

Required snapshot sections:
- `## Snapshot precis`
- `## Prompt / Trigger`
- `## Context`
- `## Key ideas`
- `## Decisions`
- `## Reusable patterns`
- `## Artifacts created`
- `## Open questions`
- `## Follow-up actions`

## Naming and IDs

- Snapshot ID format: `snap-YYYY-MM-DD-short-slug`
- Snapshot filename format: `YYYY-MM-DD__domain__slug.md`
- IDs are globally unique across object types.

Prefixes:
- `snap-`
- `concept-`
- `artifact-`
- `map-`

## Visibility and lifecycle

Visibility enum:
- `private`
- `sensitive`
- `needs-review`
- `public-safe`

Lifecycle enum:
- `draft`
- `reviewed`
- `published`
- `archived`

Disallowed transition:
- `draft -> published`

## Validation and registry behavior

Validation enforces:
- required keys
- enum correctness
- ID format and uniqueness
- required snapshot sections
- canonical-home rule
- metadata-over-folder rule
- resolvable object references

Registry behavior:
- canonical markdown files are source of truth
- registry CSVs are generated and fully rewritten each run

## Commands

```bash
IVY_CONTENT_ROOT=/Users/dhk/Documents/dev/ivy-archive-private python3 scripts/validate.py
IVY_CONTENT_ROOT=/Users/dhk/Documents/dev/ivy-archive-private python3 scripts/build_registry.py
```

## Conclusion

Ivy v1 is now defined as a two-repo, markdown-first system with strict canonical storage, metadata-driven visibility, and automated validation/registry generation.

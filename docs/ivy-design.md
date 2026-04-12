# Ivy Design

Status: Draft v1.2

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
- Visibility controlled by metadata, not structure
- Machine-usable metadata + human-readable docs

## Non-negotiable rules (v1)

1. Canonical-home rule
Every canonical object has exactly one home in one object folder.

2. Metadata-over-folder rule
Visibility is encoded in frontmatter (`visibility`), not canonical path.

3. Infrastructure-vs-content rule
Infrastructure and content are separated to preserve clarity.

## Repo model

Ivy runs as a **single repo**.

Infrastructure and content live together:

```text
ivy-archive/
  README.md
  docs/
  protocols/
  templates/
  scripts/
  inbox/
    raw/
    to-process/
  snapshots/
  concepts/
  artifacts/
  maps/
  registry/
```

**Why single repo:** the `visibility` frontmatter field is the privacy boundary. Structural separation into two repos adds operational complexity (env vars, two remotes, sync discipline) without meaningful safety benefit for content that is primarily public-safe. The visibility field ensures every object has an explicit, auditable privacy classification.

**Splitting later:** if sensitive content accumulates, the repo can be split. `IVY_CONTENT_ROOT` is still supported as an optional env var to point tooling at a separate content directory. All objects with `visibility: private` or `visibility: sensitive` can be migrated cleanly because visibility is metadata, not location.

**CI guard (recommended):** a public repo should have a CI check that blocks push if any object has `visibility: private` or `visibility: sensitive`, as a safety net against accidental exposure.

Note: `src/` is intentionally omitted in v1. It can be introduced later when a true packaged app/library boundary exists.

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
- `## Links` *(optional but recommended)*

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
python3 scripts/validate.py
python3 scripts/build_registry.py
```

Optional override if running tooling against a separate content directory:

```bash
IVY_CONTENT_ROOT=/path/to/content python3 scripts/validate.py
IVY_CONTENT_ROOT=/path/to/content python3 scripts/build_registry.py
```

## Conclusion

Ivy v1 is a single-repo, markdown-first system with strict canonical storage, metadata-driven visibility, and automated validation/registry generation.


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

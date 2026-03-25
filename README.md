# ivy-archive

Ivy is a Git-backed, markdown-first knowledge archive.
This repo is the public engine/spec/templates project.

## Design goals

- Durable storage in plain text
- Deterministic capture and review patterns
- Low-friction authoring with strict parseability
- Explicit privacy and lifecycle controls
- Machine-usable metadata with human-readable files

## Canonical object folders

- `snapshots/`
- `concepts/`
- `artifacts/`
- `maps/`

Visibility is metadata in frontmatter, not a directory decision.

## Workflow folders

- `inbox/raw/`: unprocessed material
- `inbox/to-process/`: normalized candidates awaiting canonicalization
- `public/approved/`: publication derivatives
- `private/`, `sensitive/`: quarantine or restricted non-canonical material

## Core commands

```bash
python3 scripts/validate.py
python3 scripts/build_registry.py
```

## Public + private setup

Use this repo as public infrastructure and keep personal notes in a private content repo.

- Public repo (this one): docs, templates, scripts, examples
- Private repo: canonical objects (`snapshots/`, `concepts/`, `artifacts/`, `maps/`)

Run scripts against private content by setting `IVY_CONTENT_ROOT`:

```bash
IVY_CONTENT_ROOT=/Users/dhk/Documents/dev/ivy-archive-private python3 scripts/validate.py
IVY_CONTENT_ROOT=/Users/dhk/Documents/dev/ivy-archive-private python3 scripts/build_registry.py
```

## Registry outputs

Generated CSV files are written to `registry/`:

- `registry/snapshots.csv`
- `registry/concepts.csv`
- `registry/artifacts.csv`
- `registry/maps.csv`
- `registry/edges.csv`

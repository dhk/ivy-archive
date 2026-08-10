# CLAUDE.md

Ivy is a structured, repo-backed memory system for reasoning — captures
decisions and reusable thinking as durable, versioned objects, not locked
into any one AI tool. Full description: [README.md](README.md). Spec:
[docs/spec.md](docs/spec.md). How to contribute:
[docs/contributor-guide.md](docs/contributor-guide.md).

## Non-negotiable rules (from docs/spec.md — read it before adding or moving content)

1. **Canonical-home rule** — every canonical object has exactly one home
   in `snapshots/`, `concepts/`, `artifacts/`, or `maps/`.
2. **Metadata-over-folder rule** — `visibility` is frontmatter metadata,
   never encoded by which folder something lives in. Note what `spec.md`
   is explicit about: `visibility` classifies content, it is **not**
   access control — repository permissions and safe remote selection are
   the actual privacy boundary. Treat it as a label to respect when
   quoting or forwarding, never as evidence that something is protected
   (see [SECURITY.md](SECURITY.md)).
3. **Infrastructure-vs-content rule** — infrastructure lives in `docs/`,
   `protocols/`, `templates/`, `scripts/`; everything else is content.

## Contributor principles (docs/contributor-guide.md)

Be structured (follow the snapshot schema exactly) · be concise · capture
decisions, not just ideas · extract reuse into artifacts · link, don't
duplicate.

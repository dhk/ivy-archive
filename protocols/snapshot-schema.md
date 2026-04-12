# Snapshot Schema

## Purpose

Defines the required structure and metadata for all snapshot files.

This ensures:
- consistency
- validation
- automation compatibility
- long-term usability

---

## File Structure

Each snapshot must contain:

1. YAML frontmatter
2. Structured markdown sections

---

## YAML Frontmatter

### Required fields

- id
- title
- date
- source
- type
- visibility
- lifecycle_state
- topics
- projects
- created_at
- updated_at

### Optional fields

- people
- tags
- related_snapshots
- related_concepts
- related_artifacts
- derived_from
- produced
- confidence
- source_ref
- summary_status
- reviewed_at
- published_at

---

## Example Frontmatter

```yaml
id: snap-2026-03-24-ivy-repo-architecture
title: Ivy repo architecture design
date: 2026-03-24
source: chatgpt
type: planning-session
visibility: private
lifecycle_state: draft
topics:
  - knowledge-management
projects:
  - ivy-the-archive
people: []
tags: []
related_snapshots: []
related_concepts: []
related_artifacts: []
derived_from: []
produced: []
confidence: medium
source_ref: null
summary_status: complete
created_at: 2026-03-24T18:10:00-07:00
updated_at: 2026-03-24T18:10:00-07:00
reviewed_at: null
published_at: null
```

---

## Allowed Enums

```yaml
source:
  - chatgpt
  - claude
  - gemini
  - notebooklm
  - manual
  - email
  - meeting
  - document
  - other

type:
  - conversation
  - planning-session
  - writing-session
  - work-session
  - research-session
  - review-session
  - design-session
  - decision-record

visibility:
  - private
  - sensitive
  - needs-review
  - public-safe

lifecycle_state:
  - draft
  - reviewed
  - published
  - archived

confidence:
  - low
  - medium
  - high

summary_status:
  - partial
  - complete
```

---

## Required Markdown Sections

Each snapshot must include:

- Snapshot précis
- Prompt / Trigger
- Context
- Key ideas
- Decisions
- Reusable patterns
- Artifacts created
- Open questions
- Follow-up actions

### Optional section: Links

Include a `## Links` section when there are relevant external or internal references.

Each link must be labeled:

- `readable` — a document you can open and consume (spec, design doc, PR description, playbook, recording)
- `reference` — a pointer for traceability only (ticket number, commit SHA, thread URL, PR number)

Format:

```markdown
## Links

- [readable] https://github.com/org/repo/blob/main/docs/spec.md — system specification
- [reference] https://github.com/org/repo/pull/42 — PR that shipped this change
- [reference] JIRA-1234 — originating ticket
- [readable] docs/ivy-design.md — local design document
```

---

## ID Rules

Format:
```
snap-YYYY-MM-DD-slug
```

Example:
```
snap-2026-03-24-ivy-repo-architecture
```

Rules:
- globally unique
- human-readable
- append `-2`, `-3` if collision occurs

---

## Filename Rules

Format:
```
YYYY-MM-DD__domain__slug.md
```

Example:
```
2026-03-24__ivy__repo-architecture.md
```

---

## Design Philosophy

Snapshots are:
- structured
- concise
- reusable

They are NOT:
- transcripts
- journals
- freeform notes

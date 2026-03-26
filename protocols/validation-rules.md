---

# 2. protocols/validation-rules.md

``` id="validation-rules-md"
# Validation Rules

## Purpose

Ensure all Ivy files are:
- consistent
- parseable
- complete
- linkable

Validation should run:
- locally (pre-commit)
- in CI

---

# Validation levels

## Errors (must fix)
- invalid YAML
- missing required fields
- invalid enum values
- duplicate IDs
- missing required sections
- invalid file location

## Warnings (non-blocking)
- empty sections
- no related links
- weak metadata
- unused tags

---

# File-level checks

- file must be .md
- must be in correct directory:
  - snapshots/
  - concepts/
  - artifacts/
  - maps/

---

# Frontmatter checks

- valid YAML
- all required keys present
- correct types (arrays vs strings)
- enums must match allowed values
- id must match format
- date must be YYYY-MM-DD
- timestamps must be ISO8601

---

# Structural checks (snapshots)

Must contain:

- ## Snapshot précis
- ## Prompt / Trigger
- ## Context
- ## Key ideas
- ## Decisions
- ## Reusable patterns
- ## Artifacts created
- ## Open questions
- ## Follow-up actions

---

# ID validation

- must start with snap-
- must include valid date
- must be unique across repo

---

# Reference validation

If present:
- related_snapshots must exist
- related_concepts must exist
- related_artifacts must exist

---

# Registry validation

- every file appears once
- path exists
- no duplicate IDs

---

# Lifecycle validation

## Allowed transitions

- draft → reviewed
- reviewed → published
- reviewed → archived
- published → archived

## Invalid

- draft → published

---

# Visibility validation

- public-safe requires reviewed or published
- sensitive should not be published

---

# Philosophy

Validation enforces:

- consistency
- reliability
- automation-readiness

Without validation, Ivy degrades into noise.
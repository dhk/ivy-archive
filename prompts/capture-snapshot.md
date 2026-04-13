# Capture Snapshot

Turn a session or conversation into a structured Ivy snapshot.

## Steps

### 1. Detect mode

Look for `.ivy` in the repo root.

- **Ivy mode**: snapshots go in `snapshots/`. Read `templates/snapshot.md` for the template and `protocols/snapshot-schema.md` for field rules.
- **Scratch mode**: snapshots go in `.ivy-scratch.md` as an appended block.

### 2. Ask what to capture

Ask the user:

> "What session or thinking should I capture? Give me a summary, or point me at the conversation."

If the user provides a conversation or summary, proceed. If they say "this session," capture the current conversation.

### 3. Generate the snapshot

#### Ivy mode

Create a file at `snapshots/YYYY-MM-DD__domain__slug.md` with:

- YAML frontmatter following `protocols/snapshot-schema.md`
  - `id`: `snap-YYYY-MM-DD-slug`
  - `date`: today
  - `source`: the tool being used (`claude`, `chatgpt`, etc.)
  - `type`: choose from allowed enums based on the session
  - `visibility`: `private` unless told otherwise
  - `lifecycle_state`: `draft`
  - `topics`, `projects`: infer from content, confirm with user
  - `related_snapshots`, `related_concepts`, `related_artifacts`: fill if links exist
  - `created_at`, `updated_at`: now in ISO8601 with timezone

- Required sections (all must be present):
  - `## Snapshot precis` — 2-3 sentence summary
  - `## Prompt / Trigger` — what started this
  - `## Context` — background
  - `## Key ideas` — the signal
  - `## Decisions` — what was concluded
  - `## Reusable patterns` — anything generalizable
  - `## Artifacts created` — what was produced
  - `## Open questions` — what's unresolved
  - `## Follow-up actions` — what to do next
  - `## Links` — relevant URLs/paths, labeled `readable` or `reference`

#### Scratch mode

Append a block to `.ivy-scratch.md`:

```markdown
---
# Snapshot: [title]
# Date: YYYY-MM-DD
# Source: [tool]
# Type: [session type]
---

## Precis
[summary]

## Key ideas
[bullets]

## Decisions
[bullets]

## Open questions
[bullets]

---
```

### 4. Validate (Ivy mode only)

```bash
python3 scripts/validate.py
```

If validation fails, fix the errors and re-validate.

### 5. Rebuild registry (Ivy mode only)

```bash
python3 scripts/build_registry.py
```

### 6. Confirm

Tell the user what was created and where. In scratch mode, add:

> "This is saved to `.ivy-scratch.md`. To promote it to a full Ivy snapshot, set up an Ivy repo and move the content into `snapshots/` using the template."

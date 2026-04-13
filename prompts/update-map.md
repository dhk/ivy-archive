# Update Map

Add a new node to the initiative map.

## Steps

### 1. Detect mode

Look for `.ivy` in the repo root.

- **Ivy mode**: proceed.
- **Scratch mode**: say "Maps require an Ivy repo. Want me to capture a snapshot to `.ivy-scratch.md` instead?" and stop.

### 2. Identify the map

Find maps in `maps/`. If there's only one, use it. If multiple, ask the user which initiative.

### 3. Ask what to add

Ask the user:

> "What should I add to the map? A new snapshot, concept, or artifact? Give me the ID or tell me what it is."

### 4. Add the node

Read the current map. Add a new entry to the `## Nodes` section following the existing format:

```markdown
---

### [label] Title
**`object-id`**
`path/to/file.md`

One-line description of what it captures or defines.
```

Choose the label from: `foundation`, `concept`, `decision`, `infrastructure`, or propose one that fits.

### 5. Update frontmatter

- Add the object ID to `linked_ids`
- Update `updated_at` to now

### 6. Rebuild registry

```bash
python3 scripts/build_registry.py
```

### 7. Confirm

Tell the user what was added and show the new node.

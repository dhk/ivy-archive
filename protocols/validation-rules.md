# Validation rules

`scripts/validate.py` is the executable authority. This document describes what it currently enforces; do not add a rule here without implementing it in the validator.

The validator scans Markdown objects under `snapshots/`, `concepts/`, `artifacts/`, and `maps/` in the selected content root. It reports errors and exits non-zero when it finds:

- missing or malformed frontmatter;
- missing required keys;
- scalar values where supported relationship fields require arrays;
- invalid IDs, snapshot filenames, dates, timestamps, or enums;
- duplicate IDs across canonical object types;
- missing or repeated required snapshot headings;
- canonical objects outside their canonical home;
- visibility encoded as a path segment;
- unresolved object references.

It does not currently enforce lifecycle transitions, content quality, registry freshness, secret detection, or whether a visibility label is safe for a repository. Those checks remain review responsibilities.

Run against the repository content:

```bash
python3 scripts/validate.py
```

Run the same public validator against a separate content root:

```bash
IVY_CONTENT_ROOT=../private-content python3 scripts/validate.py
```

After validation succeeds, regenerate all registry projections:

```bash
python3 scripts/build_registry.py
```

Registry files are outputs, not validation authorities. They must be regenerated and reviewed after canonical content changes.

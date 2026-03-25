#!/usr/bin/env python3
import os
import re
from datetime import datetime, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_ROOT = os.path.realpath(os.environ.get("IVY_CONTENT_ROOT", ROOT))
CANONICAL_DIRS = ["snapshots", "concepts", "artifacts", "maps"]

VISIBILITY = {"private", "sensitive", "needs-review", "public-safe"}
LIFECYCLE = {"draft", "reviewed", "published", "archived"}
SNAPSHOT_SOURCE = {
    "chatgpt",
    "claude",
    "gemini",
    "notebooklm",
    "manual",
    "email",
    "meeting",
    "document",
    "other",
}
SNAPSHOT_TYPE = {
    "conversation",
    "planning-session",
    "writing-session",
    "work-session",
    "research-session",
    "review-session",
    "design-session",
    "decision-record",
}
CONFIDENCE = {"low", "medium", "high"}
SUMMARY_STATUS = {"partial", "complete"}

SNAPSHOT_REQUIRED_KEYS = {
    "id",
    "title",
    "date",
    "source",
    "type",
    "visibility",
    "lifecycle_state",
    "topics",
    "projects",
    "created_at",
    "updated_at",
}

COMMON_REQUIRED_KEYS = {
    "id",
    "title",
    "date",
    "type",
    "visibility",
    "lifecycle_state",
    "topics",
    "projects",
    "created_at",
    "updated_at",
}

SNAPSHOT_SECTIONS = [
    "## Snapshot precis",
    "## Prompt / Trigger",
    "## Context",
    "## Key ideas",
    "## Decisions",
    "## Reusable patterns",
    "## Artifacts created",
    "## Open questions",
    "## Follow-up actions",
]

ID_PATTERNS = {
    "snapshots": re.compile(r"^snap-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$"),
    "concepts": re.compile(r"^concept-[a-z0-9-]+$"),
    "artifacts": re.compile(r"^artifact-[a-z0-9-]+$"),
    "maps": re.compile(r"^map-[a-z0-9-]+$"),
}

SNAPSHOT_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+\.md$")


def _parse_scalar(value):
    value = value.strip()
    if value == "null":
        return None
    if value == "[]":
        return []
    return value


def parse_frontmatter(text):
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("Missing YAML frontmatter opening delimiter '---'")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("Missing YAML frontmatter closing delimiter '---'")

    fm = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")

        key, raw_val = line.split(":", 1)
        key = key.strip()
        raw_val = raw_val.strip()

        if raw_val == "":
            arr = []
            i += 1
            while i < end:
                child = lines[i]
                if child.startswith("  - "):
                    arr.append(child[4:].strip())
                    i += 1
                elif not child.strip():
                    i += 1
                else:
                    break
            fm[key] = arr
            continue

        fm[key] = _parse_scalar(raw_val)
        i += 1

    body = "\n".join(lines[end + 1 :])
    return fm, body


def parse_date(value):
    try:
        date.fromisoformat(value)
        return True
    except Exception:
        return False


def parse_timestamp(value):
    try:
        datetime.fromisoformat(value)
        return True
    except Exception:
        return False


def find_canonical_files(root=CONTENT_ROOT):
    out = []
    for folder in CANONICAL_DIRS:
        base = os.path.join(root, folder)
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for name in filenames:
                if name.endswith(".md"):
                    out.append((folder, os.path.join(dirpath, name)))
    return sorted(out, key=lambda x: x[1])

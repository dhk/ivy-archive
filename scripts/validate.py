#!/usr/bin/env python3
import os
import sys

from ivy_lib import (
    ROOT,
    CONTENT_ROOT,
    VISIBILITY,
    LIFECYCLE,
    SNAPSHOT_SOURCE,
    SNAPSHOT_TYPE,
    CONFIDENCE,
    SUMMARY_STATUS,
    SNAPSHOT_REQUIRED_KEYS,
    COMMON_REQUIRED_KEYS,
    SNAPSHOT_SECTIONS,
    ID_PATTERNS,
    SNAPSHOT_FILE_RE,
    parse_frontmatter,
    parse_date,
    parse_timestamp,
    find_canonical_files,
)


def relpath(p):
    return os.path.relpath(p, CONTENT_ROOT)


def validate_snapshot_filename(path, errors):
    name = os.path.basename(path)
    if not SNAPSHOT_FILE_RE.match(name):
        errors.append(f"{relpath(path)}: invalid snapshot filename format")


def check_required_keys(path, fm, required, errors):
    missing = sorted(k for k in required if k not in fm)
    if missing:
        errors.append(f"{relpath(path)}: missing required keys: {', '.join(missing)}")


def check_arrays(path, fm, keys, errors):
    for k in keys:
        if k in fm and fm[k] is not None and not isinstance(fm[k], list):
            errors.append(f"{relpath(path)}: key '{k}' must be an array")


def validate_sections(path, body, errors):
    for heading in SNAPSHOT_SECTIONS:
        count = body.count(heading)
        if count != 1:
            errors.append(f"{relpath(path)}: heading '{heading}' must appear exactly once")


def main():
    errors = []
    seen_ids = {}
    refs = []

    files = find_canonical_files()
    if not files:
        print("No canonical markdown files found. Layout is valid.")
        return 0

    for folder, path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            fm, body = parse_frontmatter(text)
        except Exception as exc:
            errors.append(f"{relpath(path)}: {exc}")
            continue

        required = SNAPSHOT_REQUIRED_KEYS if folder == "snapshots" else COMMON_REQUIRED_KEYS
        check_required_keys(path, fm, required, errors)

        if folder == "snapshots":
            validate_snapshot_filename(path, errors)
            validate_sections(path, body, errors)

        for key in ["topics", "projects", "people", "tags", "related_snapshots", "related_concepts", "related_artifacts", "derived_from", "produced"]:
            if key in fm:
                check_arrays(path, fm, [key], errors)

        sid = fm.get("id")
        if sid:
            if sid in seen_ids:
                errors.append(f"{relpath(path)}: duplicate id '{sid}' also in {relpath(seen_ids[sid])}")
            else:
                seen_ids[sid] = path
            pattern = ID_PATTERNS[folder]
            if not pattern.match(sid):
                errors.append(f"{relpath(path)}: id '{sid}' does not match expected pattern for {folder}")

        if "date" in fm and fm.get("date") and not parse_date(fm["date"]):
            errors.append(f"{relpath(path)}: invalid date '{fm['date']}', expected YYYY-MM-DD")

        for ts_key in ["created_at", "updated_at", "reviewed_at", "published_at"]:
            if ts_key in fm and fm[ts_key] is not None and not parse_timestamp(fm[ts_key]):
                errors.append(f"{relpath(path)}: invalid timestamp for '{ts_key}'")

        if "visibility" in fm and fm["visibility"] not in VISIBILITY:
            errors.append(f"{relpath(path)}: invalid visibility '{fm['visibility']}'")

        if "lifecycle_state" in fm and fm["lifecycle_state"] not in LIFECYCLE:
            errors.append(f"{relpath(path)}: invalid lifecycle_state '{fm['lifecycle_state']}'")

        if folder == "snapshots":
            if "source" in fm and fm["source"] not in SNAPSHOT_SOURCE:
                errors.append(f"{relpath(path)}: invalid source '{fm['source']}'")
            if "type" in fm and fm["type"] not in SNAPSHOT_TYPE:
                errors.append(f"{relpath(path)}: invalid snapshot type '{fm['type']}'")
            if "confidence" in fm and fm["confidence"] is not None and fm["confidence"] not in CONFIDENCE:
                errors.append(f"{relpath(path)}: invalid confidence '{fm['confidence']}'")
            if "summary_status" in fm and fm["summary_status"] is not None and fm["summary_status"] not in SUMMARY_STATUS:
                errors.append(f"{relpath(path)}: invalid summary_status '{fm['summary_status']}'")

        for ref_key in ["related_snapshots", "related_concepts", "related_artifacts", "derived_from", "produced"]:
            if isinstance(fm.get(ref_key), list):
                for ref in fm[ref_key]:
                    refs.append((path, ref_key, ref))

    for path, ref_key, ref in refs:
        if ref and ref not in seen_ids:
            errors.append(f"{relpath(path)}: unresolved reference in {ref_key}: '{ref}'")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"Validation passed for {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

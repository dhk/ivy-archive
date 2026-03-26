#!/usr/bin/env python3
import csv
import os

from ivy_lib import CONTENT_ROOT, find_canonical_files, parse_frontmatter


def relpath(p):
    return os.path.relpath(p, CONTENT_ROOT)


def list_to_pipe(value):
    if isinstance(value, list):
        return "|".join(value)
    return ""


def ensure_registry_dir():
    registry_root = os.path.realpath(os.environ.get("IVY_REGISTRY_ROOT", CONTENT_ROOT))
    path = os.path.join(registry_root, "registry")
    os.makedirs(path, exist_ok=True)
    return path


def write_registry(path, rows):
    fields = [
        "id",
        "date",
        "title",
        "type",
        "topics",
        "projects",
        "visibility",
        "lifecycle_state",
        "updated_at",
        "path",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r.get("date", ""), r.get("id", ""))):
            writer.writerow(row)


def main():
    registry_dir = ensure_registry_dir()
    files = find_canonical_files()

    buckets = {"snapshots": [], "concepts": [], "artifacts": [], "maps": []}
    edges = []

    for folder, path in files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        fm, _ = parse_frontmatter(text)

        row = {
            "id": fm.get("id", ""),
            "date": fm.get("date", ""),
            "title": fm.get("title", ""),
            "type": fm.get("type", ""),
            "topics": list_to_pipe(fm.get("topics", [])),
            "projects": list_to_pipe(fm.get("projects", [])),
            "visibility": fm.get("visibility", ""),
            "lifecycle_state": fm.get("lifecycle_state", ""),
            "updated_at": fm.get("updated_at", ""),
            "path": relpath(path),
        }
        buckets[folder].append(row)

        source_id = fm.get("id", "")
        for ref_key in [
            "related_snapshots",
            "related_concepts",
            "related_artifacts",
            "derived_from",
            "produced",
        ]:
            refs = fm.get(ref_key, [])
            if isinstance(refs, list):
                for target in refs:
                    edges.append(
                        {
                            "source_id": source_id,
                            "relation": ref_key,
                            "target_id": target,
                            "source_path": relpath(path),
                        }
                    )

    for folder, rows in buckets.items():
        write_registry(os.path.join(registry_dir, f"{folder}.csv"), rows)

    edges_path = os.path.join(registry_dir, "edges.csv")
    with open(edges_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["source_id", "relation", "target_id", "source_path"]
        )
        writer.writeheader()
        for row in sorted(
            edges, key=lambda r: (r["source_id"], r["relation"], r["target_id"])
        ):
            writer.writerow(row)

    print("Registry rebuilt:")
    print(f"- {os.path.join('registry', 'snapshots.csv')}")
    print(f"- {os.path.join('registry', 'concepts.csv')}")
    print(f"- {os.path.join('registry', 'artifacts.csv')}")
    print(f"- {os.path.join('registry', 'maps.csv')}")
    print(f"- {os.path.join('registry', 'edges.csv')}")


if __name__ == "__main__":
    main()

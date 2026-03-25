# Ivy Design

===

Ivy the Archive — Design Document

Status

Draft v1

Purpose of this document

This document defines the design of Ivy, a repo-backed knowledge archive for capturing, structuring, retrieving, and operationalizing conversations, decisions, artifacts, and durable concepts. It is intended to be sufficiently explicit that another tool or engineer can review it and implement a first working version without needing to infer the system’s core architecture.

The design emphasizes:
	•	durable markdown-first storage
	•	deterministic capture patterns
	•	low-friction ingestion
	•	explicit privacy boundaries
	•	human-readable structure
	•	machine-usable metadata
	•	progressive enhancement toward graph-style retrieval

This is a design for a working system, not just a folder convention.

⸻

1. Executive summary

Ivy is a Git-backed personal reasoning and archive system. Its job is to convert ephemeral interactions—especially AI conversations—into durable, structured, queryable assets.

At its core, Ivy stores a small number of object types:
	•	Snapshots: structured records of sessions
	•	Artifacts: reusable outputs
	•	Concepts: durable ideas
	•	Maps: navigation documents

The snapshot is the canonical unit of capture.

⸻

2. Core design principles

Markdown first

Decision: markdown is canonical.

Repo-backed

Decision: Git as storage.

Snapshot-first

Decision: snapshot is core object.

Private by default

Decision: all content starts private.

⸻

3. Repository structure

===
ivy/
README.md
snapshots/
concepts/
artifacts/
prompts/
templates/
code/
outlines/
maps/
registry/
protocols/
inbox/
raw/
to-process/
public/
approved/
private/
sensitive/

⸻

4. Snapshot schema

===



Snapshot précis
	•	core idea
	•	key context
	•	why it matters

Metadata
	•	id:
	•	date:
	•	title:
	•	source:
	•	type:
	•	topics:
	•	projects:
	•	visibility:

Prompt / Trigger

Context

Key ideas

Decisions

Reusable patterns

Artifacts created

Open questions

Follow-up actions

Source notes

===

⸻

5. Naming conventions

===
YYYY-MM-DD__domain__slug.md

⸻

6. Ingestion pipeline
	1.	inbox/raw
	2.	transform
	3.	inbox/to-process
	4.	normalize
	5.	commit to snapshots

⸻

7. Visibility model
	•	private
	•	needs-review
	•	public-safe

⸻

8. Registries

===
id,date,title,type,topics,projects,visibility,path

⸻

9. Tradeoffs
	•	repo vs db → repo
	•	structured vs raw → structured
	•	automation vs manual → hybrid

⸻

10. Conclusion

Ivy is a structured markdown archive designed for durability, reuse, and future automation.

===
---
id: snap-2026-04-12-ivy-context-streams
title: Ivy context streams and the initiative concept
date: 2026-04-12
source: claude
source_ref: null
type: design-session
visibility: public-safe
lifecycle_state: draft
topics:
  - knowledge-management
  - context-management
  - system-design
projects:
  - ivy-the-archive
people: []
tags: []
related_snapshots:
  - snap-2026-03-26-ivy-system-context
related_concepts:
  - concept-initiative
related_artifacts: []
derived_from:
  - snap-2026-03-26-ivy-system-context
produced: []
confidence: high
summary_status: complete
created_at: 2026-04-12T15:30:00-07:00
updated_at: 2026-04-12T15:30:00-07:00
reviewed_at: null
published_at: null
---

# Ivy context streams and the initiative concept

## Snapshot precis

Working session where a gap in Ivy v1 was identified: no mechanism for keeping separate context streams isolated. Led to the definition of the `initiative` concept and the context brief / handoff pattern.

## Prompt / Trigger

User wants to use Ivy both as a knowledge store and as a live working tool across multiple AI platforms. Needed to figure out where improvement work on Ivy itself should be stored, and realised that different projects need separate context streams.

## Context

Following the creation of the first context snapshot (`snap-2026-03-26-ivy-system-context`) and a review of the session's output, the user asked:

1. Which repo should store improvement work on Ivy? (public infrastructure repo vs. private content repo)
2. How should context be separated when working across multiple projects?

The user identified that as they build Ivy, they're generating context that only belongs to that work — and they need a way to hand that context to a new AI tool without bringing in unrelated material.

Options considered:
- A dedicated branch per project
- A separate clone per project
- An "initiative" as a named collection of branches

## Key ideas

- **Branches are for work in progress, not context storage.** A `claude/some-task` branch should merge to main. Using branches as permanent context containers means content never merges, the registry can't query across it, and the system fragments.
- **Context scoping is a metadata problem, not a Git problem.** The `projects` field already provides a filter. What was missing was a first-class handoff artifact.
- **A map is a context brief.** Ivy's `map` object type is the right vehicle for scoping context to an initiative — it's a curated list of relevant objects, ordered for a reader (human or AI).
- **Minimum viable context principle.** When handing off to a new tool, give it the initiative's map + linked snapshots. Not the whole archive.
- **Repo split answer:** Infrastructure changes (schema, scripts, templates) go in `ivy-archive`. Snapshots documenting the work go in `ivy-archive-private`. We're bending this rule while bootstrapping with only the public repo available.

## Decisions

1. Introduce `initiative` as a first-class concept in Ivy — a bounded body of work with a metadata scope and an owned context brief.
2. An initiative is defined by: a project tag, a map (context brief), and optionally a concept file.
3. Git branches remain for work-in-progress only. Initiatives are permanent metadata scopes on main.
4. The handoff pattern is: map → linked snapshots → new tool. Not: full archive → new tool.
5. Capture this session as a snapshot and create `concept-initiative` before continuing further design work.

## Reusable patterns

- **Minimum viable context**: scope the handoff to an initiative's map, not the whole archive. Keeps tool context tight and relevant.
- **Initiative as a scope boundary**: any body of work that generates its own context stream — a project, a client engagement, a design effort — should be named as an initiative with a map.
- **Branch-to-main discipline**: Claude Code work branches produce snapshots; snapshots merge to main; initiatives accumulate on main via project tags. Branches are ephemeral; initiatives are durable.

## Artifacts created

- `concepts/concept-initiative.md` — definition of the initiative concept

## Open questions

- Should `initiative` become a formal Ivy object type (with its own ID prefix, schema, and validator support), or is it sufficiently covered by a concept file + project tag convention?
- How should the context brief (map) be structured for maximum usefulness to an AI tool? What ordering and framing works best?
- When an initiative spans multiple repos (e.g. a project with code + knowledge), how does the map link across them?

## Follow-up actions

- Create the first initiative map: `maps/ivy-improvement-context.md` as a context brief for Ivy development work
- Decide whether `initiative` needs a formal object type or stays a convention
- Capture the repo split decision (public infra / private content) as its own snapshot

## Links

- [readable] concepts/concept-initiative.md — initiative concept definition produced in this session
- [readable] snapshots/2026-03-26__ivy__system-context.md — prior context snapshot this session built on
- [readable] docs/ivy-design.md — two-repo model and design principles
- [reference] branch: claude/read-context-snapshot-RXn5X — work branch for this session

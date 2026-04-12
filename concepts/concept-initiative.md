---
id: concept-initiative
title: Initiative
date: 2026-04-12
type: concept
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
  - snap-2026-04-12-ivy-context-streams
related_concepts: []
related_artifacts: []
created_at: 2026-04-12T15:30:00-07:00
updated_at: 2026-04-12T15:30:00-07:00
reviewed_at: null
published_at: null
---

# Initiative

## Definition

An **initiative** is a bounded body of work with a defined context scope.

It groups related snapshots, concepts, and artifacts under a single named effort, and owns a **context brief** (a map) that can be handed to a new tool or collaborator to reconstruct working context without exposing the full archive.

An initiative is not a Git branch. It is a metadata scope.

## Why it matters

As work accumulates in Ivy, different projects generate different context streams. Without a way to scope context, three problems emerge:

1. **Context bleed** — snapshots from unrelated work pollute each other when handed to an AI tool
2. **Handoff failure** — switching tools means dumping the whole archive or losing context entirely
3. **Orientation cost** — every new session re-reads everything instead of just what's relevant

An initiative solves this by defining a boundary. Everything inside it is in scope for a given handoff. Everything outside is not.

## Structure

An initiative consists of:

- A **project tag** (`projects: [initiative-slug]`) applied to all related objects
- A **context brief** — a `map` that lists the relevant snapshots and concepts in order, with enough framing to orient a new tool
- Optionally: a top-level concept file (this file) defining the initiative's purpose and scope

## Handoff pattern

When switching AI tools or starting a new session:

1. Open the initiative's map
2. Hand the map + linked snapshots to the new tool
3. The new tool has the context it needs — no more, no less

This is the **minimum viable context** principle: give the tool the right scope, not the whole archive.

## Relationship to Git branches

Git branches are for **work in progress** — a change being made, not yet merged.

Initiatives are **permanent metadata scopes** — they live on main, accumulate over time, and never "close" in the same way a branch does.

A Claude Code work branch (`claude/some-task`) may produce snapshots that belong to an initiative. When the branch merges, the snapshot moves to main; the initiative retains it via the `projects` tag.

## Examples

- `ivy-improvement` — the initiative tracking the development and refinement of Ivy itself
- `client-onboarding-2026` — a bounded piece of client work with its own context stream
- `product-strategy-q2` — a planning initiative with snapshots from multiple sessions

## Linked objects

- See `maps/` for context briefs associated with active initiatives
- See `snap-2026-04-12-ivy-context-streams` for the session where this concept was identified

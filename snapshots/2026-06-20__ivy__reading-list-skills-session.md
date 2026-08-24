---
id: snap-2026-06-20-reading-list-skills-session
title: Reading list skills update — wrong repo, blocked artifact fetch
date: 2026-06-20
source: claude
source_ref: null
type: work-session
visibility: public-safe
lifecycle_state: draft
topics:
  - knowledge-management
  - skill-system
  - workflow
projects:
  - ivy-the-archive
people: []
tags: []
related_snapshots:
  - snap-2026-04-12-ivy-single-repo-decision
related_concepts: []
related_artifacts:
  - artifact-ivy-session-start-prompt
derived_from: []
produced: []
confidence: high
summary_status: complete
created_at: 2026-06-20T00:00:00-07:00
updated_at: 2026-06-20T00:00:00-07:00
reviewed_at: null
published_at: null
---

# Reading list skills update — wrong repo, blocked artifact fetch

## Snapshot precis

Work session that attempted to update a reading list builder skill in `dhk/adventures-in-ai`. The session was scoped to the wrong repo (`dhk/ivy-archive`), the artifact URL from a Claude mobile conversation returned a 403, and the GitHub MCP tools were restricted to `ivy-archive`. Work was blocked; no changes committed. Key discovery: Claude Code web sessions are scoped to a single repo by the harness — to switch repos, start a new session.

## Prompt / Trigger

User shared a screenshot of a prior Claude mobile conversation where they asked Claude to push a revised reading list builder skill (from a claude.ai artifact URL) to the repo. The previous session failed to fetch the artifact (403). User brought this to the current session to complete the task.

## Context

- Current working directory: `/home/user/ivy-archive` (scoped to `dhk/ivy-archive`)
- Branch: `claude/update-reading-list-skills-RJp9f`
- Target repo: `dhk/adventures-in-ai` — not cloned locally, not within the MCP scope for this session
- Artifact URL `https://claude.ai/public/artifacts/009b2ed4-6e6f-4925-8f76-f0949d599c2c` returned HTTP 403 (claude.ai artifacts require authentication; WebFetch cannot access them)
- `~/.claude/skills/ivy-archive/SKILL.md` does not exist
- Last snapshot in registry: `2026-04-12` — no context captured since then

## Key ideas

- **Claude Code web sessions are repo-scoped by the harness.** The GitHub MCP tools are restricted to one repo per session. To work on a different repo, start a new session (new conversation on mobile, or `cd` + `claude` on CLI).
- **claude.ai artifact URLs are authenticated.** They cannot be fetched via WebFetch — they return 403. The content must be pasted directly into the conversation.
- **Session context gap.** Two months elapsed between last snapshot (2026-04-12) and this session (2026-06-20) with no Ivy captures. The skill system was added in April but no snapshot recorded the adventures-in-ai reading list work.

## Decisions

None — session was blocked before work began.

## Reusable patterns

- **Paste, don't link, for claude.ai artifacts.** When sharing revised skill content from a Claude mobile/web conversation, paste the text directly rather than sharing the artifact URL. The URL is not publicly fetchable.
- **New session = new repo scope.** Do not attempt cross-repo work in a single session. Start fresh in the target repo.

## Artifacts created

None.

## Open questions

- What is the current state of the reading list builder skill in `dhk/adventures-in-ai`? What did the revision change?
- Should the `adventures-in-ai` skill work be snapshotted in `ivy-archive` (as a cross-project record) or does it belong in its own Ivy-enabled repo?
- Should the branch `claude/update-reading-list-skills-RJp9f` be deleted since no changes were committed?

## Follow-up actions

- Start a new session scoped to `dhk/adventures-in-ai`
- Paste the revised reading list builder skill content directly (do not share artifact URL)
- Apply and push the skill update in that session

## Links

- [reference] branch: claude/update-reading-list-skills-RJp9f — work branch for this session (no commits)
- [reference] artifact: https://claude.ai/public/artifacts/009b2ed4-6e6f-4925-8f76-f0949d599c2c — revised skill content (requires auth; paste content instead)
- [readable] prompts/index.md — ivy-archive skill index

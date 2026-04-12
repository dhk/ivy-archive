# Ivy — The Archive

## One-line
A structured, repo-backed system for capturing and reusing thinking.

## Short version
Ivy turns conversations, decisions, and ideas into durable, structured assets that can be reused across time, tools, and collaborators.

It is designed so that:
- your thinking is not locked inside any AI tool
- your thinking is kept private and under your control
- your work is portable across models and interfaces
- others can build on what you’ve already figured out

---

# What Ivy is

Ivy is a structured memory system for reasoning.

It captures:
- what you were trying to do
- what mattered
- what you decided
- what can be reused

It stores this in:
- plain markdown
- inside a Git repo
- with consistent structure

---

# Why Ivy exists

Most valuable thinking is lost.

- AI conversations disappear into chat logs
- Decisions are made but not recorded
- Prompts and frameworks are reinvented repeatedly
- Insights are tied to specific tools and sessions

Raw transcripts are not enough:
- too long
- too noisy
- not reusable

Ivy exists to solve this:

Turn ephemeral thinking into durable leverage.

---

# The key unlock

AI increases the volume of thinking, but fragments it across:
- tools (ChatGPT, Claude, Gemini, etc.)
- interfaces (chat, IDEs, notebooks)
- sessions

Ivy makes thinking:

## Portable
Your thinking lives in your repo, not inside any AI system.

## Composable
Snapshots become building blocks.

## Collaborative
Others can extend and build on your thinking.

AI doesn’t just amplify individuals — it amplifies shared thinking.

---

# Core idea

The central unit of Ivy is the snapshot:

A structured record of a single unit of thinking.

Everything builds from this.

---

# Design goals

- Reuse over storage
- Structure over volume
- Determinism over cleverness
- Human-readable first
- Tool independence
- Collaboration-ready
- Private by default

---

# What Ivy stores

## Snapshots
Structured records of sessions.

## Artifacts
Reusable outputs.

## Concepts
Durable ideas.

## Maps
Curated navigation.

---

# What good looks like

- clear, structured snapshots
- explicit decisions
- reusable artifacts
- minimal duplication
- consistent metadata
- strong privacy boundaries

---

# What Ivy is not

- not a transcript dump
- not a note app
- not a passive archive

It is an active system for reuse.

---

# Philosophy

The most valuable output of thinking is not the answer —
it is the structure of how the answer was reached.

That structure can be reused.

---

# Summary

Ivy is:
- portable thinking
- reusable reasoning
- collaborative knowledge

Over time, it becomes a compounding system.

---

# Getting started

**If you're new:** read `maps/ivy-improvement-context.md` — it's the context brief for this repo. It tells you what exists, in what order to read it, and how to orient quickly.

**If you're building your own Ivy:** read `docs/ivy-design.md` (architecture) and `docs/spec.md` (schema rules), then use `templates/snapshot.md` to capture your first session.

**Tooling:**

```bash
python3 scripts/validate.py       # validate all canonical objects
python3 scripts/build_registry.py # regenerate registry CSVs
```

---

# What's in this repo

| Type | Count | Location |
|---|---|---|
| Snapshots | 3 | `snapshots/` |
| Concepts | 1 | `concepts/` |
| Maps | 1 | `maps/` |
| Registry | auto-generated | `registry/` |

See `registry/snapshots.csv` for the full index.

---

# Further reading

- `docs/ivy-design.md` — architecture and design decisions (v1.2)
- `docs/spec.md` — full specification
- `docs/how-to-use-ivy.md` — 5-minute guide
- `docs/contributor-guide.md` — how to contribute consistently
- `docs/first-10-snapshots-playbook.md` — quality bar for early snapshots
- `TODO.md` — known future work

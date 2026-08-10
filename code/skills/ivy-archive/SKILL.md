---
name: ivy-archive
version: "2.0"
description: >
  Sweeps save-context snapshots (.scratch/*.md) and Captain's Logs, collects them into the
  ivy-archive-private git repo with provenance headers, and pushes to both GitHub and
  NotebookLM. Modes: sweep (stamp locally), collect (copy into the git repo), push (git
  remote + NotebookLM), miso (do everything), query (answer questions about past work),
  status (check sync state).
  Trigger on: "sweep archive", "ivy collect", "push to ivy", "miso", "ivy everything",
  "update ivy", "what was I working on", "what branches are active", "where did I work on X",
  "how do I get back to X", "ivy", "/ivy-archive".
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__notebooklm__notebook_list
  - mcp__notebooklm__notebook_create
  - mcp__notebooklm__source_add
  - mcp__notebooklm__notebook_query
  - mcp__notebooklm__notebook_query_start
  - mcp__notebooklm__notebook_query_status
---

# Ivy Archive

> *Ivy is the archive. All past work flows into her. She knows where you were.*

Snapshots flow through three tiers:

```
[session] → save context → <repo>/.scratch/[file].md
                                  │
                          sweep   │  stamp in place (Swept | Pushed-to-ivy)
                                  ▼
                          collect │  copy → ivy-archive-private/snapshots/<repo>/ + provenance
                                  ▼
                          push    │  git push → GitHub  +  source_add → NotebookLM
                                  ▼
                          [ miso = sweep + collect + push, one command ]
```

**Three things, two names — keep them straight:**

| Name | What | Where |
|------|------|-------|
| `ivy-archive` | design/authoring repo (NOT a snapshot store) | `~/Documents/dev/ivy-archive` |
| `ivy-archive-private` (git) | the **collection repo** — snapshots land here | `~/Documents/dev/ivy-archive-private` |
| `ivy-archive-private` (NotebookLM) | semantic-search notebook | notebooklm.google.com |

> **Remember:** every repo lives under `~/Documents/dev/` — never `~/Documents/` directly.

---

## CONFIG

Read at the start of any mode that touches the git repo:
`~/.claude/skills/ivy-archive/config`

```
local_repo=/path/to/private-content
remote_url=https://github.com/<owner>/<private-content-repo>.git
remote_branch=main
collect_subdir=snapshots
```

If the config is missing: prompt for the local repo path and remote, write the file. If the
repo doesn't exist on disk, offer `gh repo create dhk/ivy-archive-private --private` (it's an
outward-facing action — ask first), then `git init` locally and wire the remote.

---

## MODE DETECTION

| Trigger | Mode |
|---------|------|
| "sweep archive", "sweep ivy", "update ivy", "archive my context", "/ivy-archive" | **Sweep** (local stamp) |
| "ivy collect", "collect to ivy", "gather context" | **Collect** (copy into git repo) |
| "push to ivy", "flush to ivy", "push to notebooklm", "ivy push", "/ivy-archive push" | **Push** (git + NLM) |
| "miso", "ivy everything", "ivy full", "do everything", "/ivy-archive miso" | **Miso** (sweep + collect + push) |
| "what was I working on", "what branches are active on", "where did I work on", "how do I get back to", any question about past work | **Query** |
| "is my context synced?", "ivy status", "sync status" | **Sync Status Check** |

**Ambiguous** (bare "ivy"): ask — "Sweep, collect, push, miso (everything), or query?"

---

## SWEEP MODE (local, fast)

Stamp all new or changed context files. No git, no NotebookLM.

### Step 1 — Harvest

```bash
ls ~/.claude/skills/ivy-archive/.last-sweep 2>/dev/null
```

**First run** (no `.last-sweep`) — everything:
```bash
find ~/Documents/dev -path "*/.scratch/*.md" | grep -v node_modules | grep -v ivy-archive-private | sort
find ~/Documents/captains-log -name "captains-log-*.md" | sort
```

**Incremental** — only newer than last sweep:
```bash
find ~/Documents/dev -path "*/.scratch/*.md" -newer ~/.claude/skills/ivy-archive/.last-sweep | grep -v node_modules | grep -v ivy-archive-private | sort
find ~/Documents/captains-log -name "captains-log-*.md" -newer ~/.claude/skills/ivy-archive/.last-sweep | sort
```

### Step 2 — Stamp each .scratch file

For each `.scratch/*.md`, append a stamp if absent, or refresh `Swept` if it exists
(preserve the existing `Pushed-to-ivy` value):

```bash
SWEEP_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# no stamp yet:
printf '\n<!-- Swept: %s | Pushed-to-ivy: never -->\n' "$SWEEP_TIME" >> "$f"
# stamp exists — refresh Swept, keep Pushed-to-ivy (capture the FULL value; ISO dates
# contain hyphens, so never use a char class that excludes '-'):
PUSHED=$(sed -n 's/.*Pushed-to-ivy: \(.*\) -->.*/\1/p' "$f" | tail -1)
sed -i '' "s|<!-- Swept:.*-->|<!-- Swept: $SWEEP_TIME \| Pushed-to-ivy: $PUSHED -->|" "$f"
```

Do **not** stamp Captain's Logs — they are append-only.

### Step 3 — Update marker

```bash
touch ~/.claude/skills/ivy-archive/.last-sweep
```

### Step 4 — Report and offer next step

```
Ivy Archive — Local Sweep Complete
────────────────────────────────────
Context snapshots swept:  [N]
Captain's Logs swept:     [N]
Last sweep: [ISO timestamp]
```

Then offer (AskUserQuestion): **collect now** (run Collect Mode), **miso** (collect + push),
or **done**.

---

## COLLECT MODE (copy into the git repo)

Copy snapshots and Captain's Logs into the collection repo, each with a provenance header,
then commit. Idempotent — safe to run repeatedly.

### Step 1 — Load config & resolve target

```bash
LOCAL_REPO=$(grep '^local_repo=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
SUBDIR=$(grep '^collect_subdir=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
DEST_ROOT="$LOCAL_REPO/$SUBDIR"        # e.g. .../ivy-archive-private/snapshots
```

### Step 2 — Collect each .scratch file

Scan all snapshots (skip node_modules and the collection repo itself):

```bash
find ~/Documents/dev -path "*/.scratch/*.md" | grep -v node_modules | grep -v ivy-archive-private | sort
```

For each source file `SRC`:

```bash
# Derive repo name = first path segment under ~/Documents/dev/
REL="${SRC#"$HOME"/Documents/dev/}"
REPO="${REL%%/*}"
[ "$REPO" = ".scratch" ] && REPO="dev"   # snapshots living directly under ~/Documents/dev/
SRC_DIR="$(dirname "$SRC")"
BRANCH=$(git -C "$SRC_DIR" branch --show-current 2>/dev/null || echo "-")
GIT_REMOTE=$(git -C "$SRC_DIR" remote get-url origin 2>/dev/null || echo "-")
REPO_PATH=$(git -C "$SRC_DIR" rev-parse --show-toplevel 2>/dev/null || echo "$HOME/Documents/dev/$REPO")
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Worktree files share basenames with the main tree — namespace them to avoid collisions.
WT=$(printf '%s' "$SRC" | sed -n 's|.*/\.claude/worktrees/\([^/]*\)/.*|\1|p')
BASE="$(basename "$SRC")"
[ -n "$WT" ] && BASE="${BASE%.md}__wt-${WT}.md"
DEST="$DEST_ROOT/$REPO/$BASE"
mkdir -p "$DEST_ROOT/$REPO"

# Strip any prior ivy-provenance block from the source body, then prepend a fresh one.
{
  printf '<!-- ivy-provenance\n'
  printf 'source_path: %s\n' "$SRC"
  printf 'repo_path:   %s\n' "$REPO_PATH"
  printf 'repo_name:   %s\n' "$REPO"
  printf 'git_remote:  %s\n' "$GIT_REMOTE"
  printf 'branch:      %s\n' "$BRANCH"
  printf 'collected:   %s\n' "$NOW"
  printf -- '-->\n\n'
  awk 'BEGIN{skip=0} /^<!-- ivy-provenance/{skip=1} skip==1 && /^-->/{skip=2; next} skip==2{skip=0; next} skip==0{print}' "$SRC"
} > "$DEST"
```

The provenance header is the keystone — it's how "how do I get back?" stays deterministic.
Always **re-derive** `git_remote`/`branch` (never trust a stale prior header) and **replace**
any existing block rather than double-prepending.

### Step 3 — Collect Captain's Logs

Copy logs newer than the last collect into `$DEST_ROOT/captains-log/` (no provenance header,
no stamp — they're append-only journals):

```bash
mkdir -p "$DEST_ROOT/captains-log"
find ~/Documents/captains-log -name "captains-log-*.md" -newer ~/.claude/skills/ivy-archive/.last-collect 2>/dev/null \
  -exec cp {} "$DEST_ROOT/captains-log/" \;
touch ~/.claude/skills/ivy-archive/.last-collect
```

### Step 4 — Commit

```bash
cd "$LOCAL_REPO"
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "ivy collect — $(date +'%Y-%m-%d %H:%M %Z')"
fi
```

### Step 5 — Report and offer next step

```
Ivy Archive — Collect Complete
────────────────────────────────
Files collected:  [N]  (across [M] repos)
Captain's Logs:   [N]
Committed:        [yes/no — nothing changed]
Repo: ~/Documents/dev/ivy-archive-private
```

Offer (AskUserQuestion): **push now** (git + NLM) or **done**.

---

## PUSH MODE (git remote + NotebookLM)

Flush the collection repo off-machine. Two destinations.

### Step 1 — Load config

```bash
LOCAL_REPO=$(grep '^local_repo=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
BRANCH=$(grep '^remote_branch=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
SUBDIR=$(grep '^collect_subdir=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
```

### Step 2 — Destination A: NotebookLM

Find files in the collection repo that need pushing — `Pushed-to-ivy: never` or stamp
older than mtime:

```bash
find "$LOCAL_REPO/$SUBDIR" -name "*.md" | sort
```

For each, find/create the notebook (`mcp__notebooklm__notebook_list` → look for
`ivy-archive-private`, else `mcp__notebooklm__notebook_create`), then
`mcp__notebooklm__source_add` with `source_type: file`, `file_path: <abs path>`.

On success (or a duplicate-rejection — it's already there), update the stamp **in the
collected copy**:

```bash
PUSH_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# `.*-->` matches the whole value (incl. hyphenated timestamps) up to the closing -->:
sed -i '' "s|Pushed-to-ivy: .*-->|Pushed-to-ivy: $PUSH_TIME -->|" "$DEST"
```

A stamp that is anything other than a valid ISO timestamp (e.g. `never`, or a corrupt
truncated value like `2026`) counts as **needs pushing**.

Captain's logs have no inline stamp — track them with
`~/.claude/skills/ivy-archive/.last-nlm-push` and push logs newer than it, then `touch` it.

### Step 3 — Destination B: git remote

Commit any stamp updates from Step 2, then push:

```bash
cd "$LOCAL_REPO"
[ -n "$(git status --porcelain)" ] && git add -A && git commit -m "ivy push — NLM stamps $(date +'%Y-%m-%d %H:%M')"
git push origin "$BRANCH"
```

If push fails (no upstream / auth), report the exact git error and stop — don't retry blind.

### Step 4 — Report and offer next step

```
Ivy Archive — Push Complete
────────────────────────────
NotebookLM:
  Already current (skipped): [N]
  Pushed:                    [N]  (snapshots [N], logs [N])
GitHub:
  Pushed to origin/[branch]:  [commit short-sha or "up to date"]

Notebook: ivy-archive-private
Repo:     dhk/ivy-archive-private
```

Offer (AskUserQuestion): **query the archive** or **done**.

---

## MISO MODE (everything, one command)

> *Miso: everything goes in the soup.* Sweep → Collect → Push, end to end.

Run the three pipelines in order, suppressing each one's intermediate "what next?" prompt —
miso is the answer to "what next?". Then print a single combined report.

1. **Sweep** — stamp changed `.scratch` files; update `.last-sweep`.
2. **Collect** — copy swept files + new logs into the repo with provenance; commit.
3. **Push** — NotebookLM (new/stale only) + `git push origin <branch>`.

```
Ivy Archive — Miso Complete 🍲
────────────────────────────────
Swept:      [N] snapshots, [N] logs
Collected:  [N] files across [M] repos  →  committed [yes/no]
NotebookLM: [N] pushed, [N] already current
GitHub:     origin/[branch] [short-sha / up to date]
```

If any stage fails, stop at that stage, report what completed and the exact error, and do
**not** mark later stages done.

End by offering (AskUserQuestion): **query the archive** or **done**.

---

## SYNC STATUS CHECK

Check whether the current session's snapshot is current in ivy.

1. Newest snapshot here: `ls -t .scratch/*.md 2>/dev/null | head -1`
2. Its stamp: `grep "Swept:\|Pushed-to-ivy" "$f" | tail -1`
3. Its mtime: `stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "$f"`

Report state and offer the matching next step:

| State | Offer |
|-------|-------|
| No `.scratch` file | Save one now? → save-context |
| No stamp line | Not swept → run Sweep (or Miso) |
| `Pushed-to-ivy: never` | Swept, not pushed → run Push (or Miso) |
| `Pushed-to-ivy` < mtime | Stale → re-push (or Miso) |
| `Pushed-to-ivy` ≥ mtime | Fully current ✓ → Query? |

---

## QUERY MODE

Answer questions about past work. Two backends.

- `--nlm` → NotebookLM (semantic; requires push to have run)
- no flag → local grep (fast, keyword) over the **collection repo**

### LOCAL BACKEND (default)

```bash
LOCAL_REPO=$(grep '^local_repo=' ~/.claude/skills/ivy-archive/config | cut -d= -f2)
```

Pull 2–4 keywords from the question. Grep the collection repo (fall back to scattered
`.scratch` if the repo is empty):

```bash
grep -ril "KEYWORD" "$LOCAL_REPO" 2>/dev/null
```

Union matches. For each hit, read its `<!-- ivy-provenance -->` header for `repo_path`,
`branch`, `source_path`, and the body's `Generated:` / `Description:` / `Status:` /
`Next Actions`. **Sort by `Generated:` descending** and return the top 1–2 — bias hard
toward recency for "what was I working on?".

```
Ivy says (local search):

── [Description] ──
Date:    [Generated]
Repo:    [repo_path]
Branch:  [branch]
Status:  [status]
Next:    [next actions]
Source:  [source_path]

To resume:
  cd [repo_path]
  git checkout [branch]
  # then: /resume-context
Tip: add --nlm for semantic search.
```

### NLM BACKEND (--nlm)

`mcp__notebooklm__notebook_list` → find `ivy-archive-private` (if absent: "No archive in
NotebookLM yet. Run 'push to ivy' first."). Enrich the question, call
`mcp__notebooklm__notebook_query` (poll `..._status` if async). Return the synthesized
answer plus a **To resume** block built from any provenance info in the sources.

---

## SCOPE

- Snapshots: `~/Documents/dev/**/.scratch/*.md`
- Captain's Logs: `~/Documents/captains-log/captains-log-*.md`
- **Excluded:** `node_modules`, `.git`, build artifacts, and the collection repo
  `ivy-archive-private` itself (never collect ivy from ivy).

## STATE FILES

| File | Purpose |
|------|---------|
| `~/.claude/skills/ivy-archive/.last-sweep` | last local sweep |
| `~/.claude/skills/ivy-archive/.last-collect` | last collect (for captain's-log newness) |
| `~/.claude/skills/ivy-archive/.last-nlm-push` | last NLM push of captain's logs |
| `~/.claude/skills/ivy-archive/config` | local_repo, remote_url, remote_branch, collect_subdir |

## ERROR HANDLING

- **NotebookLM auth error**: "Auth needed — run `nlm login` in your terminal, then retry."
- **NLM query timeout**: retry once; if still failing, suggest local search.
- **git push rejected / no upstream / auth**: report the exact git error; do not retry blind.
- **config missing**: prompt for paths, offer `gh repo create --private`, write config.

## NOT YET BUILT (designed in ivy-archive/docs/system-design.md)

`groom` (merge duplicate snapshots) and `conclude` (summarize + archive a finished work
stream) are specified but not implemented. Auto-snapshot-per-session is on the ivy-archive
TODO. Don't claim these run — point at the design doc if asked.

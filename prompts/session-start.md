# Session Start

Orient to an Ivy project and prove readiness.

## Steps

### 1. Detect mode

Look for `.ivy` in the repo root or current directory.

- **Ivy mode**: proceed to step 2.
- **Scratch mode**: check for `.ivy-scratch.md` in the current directory. If it exists, read it for prior context. If not, tell the user: "No Ivy repo or scratch file detected. Want me to create `.ivy-scratch.md` to start capturing?" Then wait.

### 2. Read the map

Find the initiative map in `maps/`. If there's only one map, read it. If there are multiple, list them and ask the user which initiative they're working on.

### 3. Follow the context graph

Read each node the map lists, in order. Then check `registry/snapshots.csv` for any objects with an `updated_at` newer than the map's `updated_at`. Read those too.

### 4. Deliver the ready signal

The map contains a `## Ready signal` section. Follow its instructions exactly.

### 5. Offer skills

After the ready signal, check if `prompts/index.md` exists. If it does, say:

> "I found skills available for this system. Want me to show you what's available?"

Wait for the user to respond before proceeding.

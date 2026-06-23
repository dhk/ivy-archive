# TODO

Things to come back to. Not urgent. Not scheduled.

- graph search on top of the registry/edges model
- graph visualization of snapshot/concept/artifact relationships
- classification engine to improve thematic relationships between objects
- **auto-snapshot per session** — get every working session to create a context snapshot
  automatically (not just on pre-compact). Likely a `Stop` hook in settings.json that
  invokes `save-context`. Open questions: gate on "session touched files" vs. every stop
  (cost + noise), and snapshot quality when auto-generated vs. asked-for. (Was "ask 0" in
  the 2026-06-23 design discussion; deferred — collect/push/miso shipped first.)

---
name: kb-status
description: Check knowledge persistence, pending turns, Git synchronization and the latest maintenance of the user's personal knowledge base.
---

Run `node SYSTEM/scripts/kb.mjs status` in the verified vault directory. On PC this is `{{MEMORY_ROOT}}`; in Cloud determine the actual path. The command updates STATUS.md in the current copy.

Report the last capture, successful sync, INBOX count, pending_turns, unpushed commits and error. Distinguish local persistence, GitHub delivery and semantic curation. Without fetch, Git behind reflects only the last known server state. Your own copy's status cannot establish the offline PC's queue or the designated curator's schedule: check those with a separately available tool. Report to the user in Russian.

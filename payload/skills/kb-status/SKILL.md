---
name: kb-status
description: Report capture, queue and delivery status of the configured knowledge base.
---

# Knowledge status

In the verified vault ({{MEMORY_ROOT}} on this installation), run `node SYSTEM/scripts/kb.mjs status`; it refreshes local STATUS.md. Report last capture, INBOX count, pending turns, known unpushed changes and errors.

Distinguish local capture, Git/API delivery and synchronization to another device. Git behind is only as fresh as its last fetch. In a cloud snapshot use the actual API receipt for delivery, not Git status. Report unknown remote/device state as unknown. A status request does not start sync, curation or a schedule.

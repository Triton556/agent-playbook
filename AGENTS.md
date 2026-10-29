# Repository maintenance

This repository maintains the owner's personal agent playbook. Read INSTALL_FOR_AGENTS.md before installing it.

- Keep skills minimal: one self-contained `SKILL.md` where possible; add a reference file only when the content is too large or too specific to load every time.
- Keep environment bindings explicit in manifest.json and rehash changed payload files. A file/hash pass is not model-quality evidence.
- The knowledge vault owns its runtime; copy `SYSTEM/scripts` from the live vault into `payload/runtime/memory` when it changes.
- Do not import private notes, credentials or remote settings into the payload.
- Run actual installer/helper checks in an isolated folder. Keep user files and different existing instructions intact. Installation implies no global client config or permission editing.
- Publication requires the user's request and a reviewed exact file set. Read back the pushed commit. Do not force push.

# Repository maintenance

This repository packages an intact configured workflow. Read INSTALL_FOR_AGENTS.md before installing it. Read docs/FIDELITY.md before changing instructions or packaging.

- Preserve full payload bodies, conditional references, helpers, datasets, source metadata and component licenses. Do not shorten a pipeline or change its acceptance criteria while fixing packaging.
- Keep environment bindings and runtime relocations explicit in manifest.json. A file/hash pass is not model-quality evidence.
- Do not import private notes, credentials, remote settings, real VM identities or another owner's standing grants.
- Run actual installer/helper checks in an isolated project. Keep user files and different existing instructions intact. No global client config or permission editing is implied by installation.
- The author owns tests and prepares a concrete brief for a fresh independent reviewer. Do not label author self-review independent or manufacture human acceptance.
- Publication requires the actual user's scope and a reviewed exact file set. Read back the pushed commit/content. Do not use force push or overwrite an existing unrelated repository.

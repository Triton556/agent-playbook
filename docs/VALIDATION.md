# Validation record

Build: 15 October 2026, Windows. The levels below describe executed checks, not a guarantee of future model quality. Python standard-library installer/helpers and Node22.13.0 were used.

## Source and composition

### 0.5.0 agent sessions addition

On 19 October 2026 (Asia/Vladivostok), the package contains 308 payload files and 26 custom skills. The five new `agent-sessions` entries are byte-identical to the supplied Claude skill and need no transformation; all other payload files are unchanged, including `codex-sessions`.

`python harness.py check-package` passed. `python -B -m unittest discover -s tests` passed all 27 tests in 192 seconds using Python 3.12 and Node.js 22.13.0. New coverage: selection in full/engineering/instructions and exclusion elsewhere, standalone Codex/Claude installation with byte comparison of all five files, `--describe` output of both adapters (agent, contract 1, `verified` true for codex and false for claude-code, three access modes) and exit code 4 for an unknown access mode. Full installations with `--client codex` and `--client claude` into empty temporary projects installed 26 skills and passed `verify`. Profile closures: full 26/26, engineering 13/17, visual 5/14, voxel 2/14, memory 5/5, instructions 4/18. The payload scan found no owner name, private alias or absolute home path.

Live checks were run on the source skill before packaging, with the user's agreement: the Codex adapter started a thread, continued it, refused a write in `read-only` and refused a write outside the folder in `workspace-write`; the results were confirmed from the files. The Claude Code adapter was checked only for `--describe`, exit code 4 and reporting a missing login as a failure; its live task checks were not run because the standalone CLI is not logged in.

The 0.4.0 working-tree changes described below were later reviewed and committed by the orchestrator, and published together with the access-mode update.

### 0.4.0 Codex sessions addition

On 19 October 2026 (Asia/Vladivostok), the package contains 303 payload files and 25 custom skills. The manifest inventory matches the actual payload. All 301 previous payload files and their manifest entries remain unchanged. The two new entries record the supplied Claude skill's source/export hashes and transformations. `codex-chat.mjs` is byte-identical to the source (SHA256 `c315fadadc52b00d01bb1687f001a67f8f8e2e8c6850a7c38c86c60edf818111`); the skill's only prose change generalizes the user's configured hooks, including memory hooks.

`python harness.py check-package` passed. `python -B -m unittest discover -s tests` passed all 26 tests in 159.173 seconds using Python 3.12.14 and Node.js 22.13.0. Added coverage checks full/engineering/instructions selection, exclusion from the other three profiles, standalone Codex/Claude installation and `node --check` for the driver. The existing full-workflow roundtrip now checks both new files in all four client layouts. Existing ownership, conflict, startup-budget, attribution and synthetic memory scenarios remain active.

Separate full installations into two new empty temporary projects with explicit `--client codex` and `--client claude` each installed 25 skills. Both `verify` runs checked 304 installed files without failures. The temporary projects were removed within the bounded test workspace. Profile selections/dependency closures were recalculated: full 25/25, engineering 12/16, visual 5/14, voxel 2/14, memory 5/5, instructions 3/17. Author reading checked the changed instructions and documentation against the supplied skill; 62 local Markdown link targets resolve and `git diff --check` passed.

Case-insensitive identifier/path scans found no source-owner name, personal memory-writer alias, curator name or absolute source home path in the payload. The broader substring search finds only the two unchanged `Anya Danilova` font-credit entries, which retain their required attribution. Grammar in the generalized hook sentence was checked directly against the original.

The native skill validator could not run because PyYAML is absent; basic frontmatter name/description/scaffold checks passed without installing dependencies. No additional agents, Codex sessions or push were used. Fresh client discovery, app visibility, new-thread/resume execution, real hooks/MCP in a Codex session, model quality and human acceptance were not independently exercised. The user's reported live source trials are prior evidence, separate from these packaging checks.

Local staging of the reviewed 15-file set on `main` was refused when Git attempted to create `.git/index.lock` (`Permission denied`). No commit was created; the changes remain in the working tree for the user's external review and commit. No alternate index, permission change or access-denial bypass was attempted.

### 0.3.0 creative-direction refresh

On 19 October 2026 (Asia/Vladivostok), 13 source blobs were read directly from the approved `creative` commit `679362d2fb0d1662527d767c6297d1cbc1cb17ca` and checked against their manifest source hashes. The current package has 301 payload files and 24 custom skills. The manifest inventory matches every payload file; export hashes and explicit portability transformations are current. Third-party datasets, font attribution and licenses remain unchanged.

`check-package` passed. The full requested Python unittest suite passed all 24 tests on the final payload in 152.902 seconds. The added scenario checks creative-direction selection in full/engineering/visual/voxel profiles and complete reference installation. The memory scenario exercises `source.kind=curator` through the real limited MCP writer, the CLI capture implementation and saved-file read-back. Existing conflict, ownership, preservation, startup-budget, four-client and memory tests remain active. Python 3.12.14 and Node.js 22.13.0 were used; no client configuration was changed.

A separate final-payload full installation with explicit `--client codex` into a new empty temporary project passed; `verify` checked 302 installed files with no failures. This includes all 24 skills and generated policy. Actual profile selections/dependency closures were recalculated and the illustrated guide's lists/table updated. The changed Markdown files' 96 local link targets resolve; the knowledge-vault link remains an external deployment binding. `git diff --check` passed after preserving source LF line endings.

Case-insensitive whole-identifier/path scans found no source-owner name, personal curator/model/project label, personal MCP alias, absolute source home path or inherited scheduler claim in the payload. A broader substring scan has only the unchanged third-party credits `Anya Danilova` (font dataset/license) and `Astral_Journeyer` (voxel source), which must retain attribution. Sentence/list starts using lowercase generic owner labels and `unless he` were also absent. Private feedback identity, family details and dated permissions are omitted; the complete operative methods and evidence caveats remain.

The native skill validator could not run because PyYAML is missing in the requested interpreter. Edited skill metadata passed basic frontmatter field/name/description-length/scaffold checks; no complete YAML-validator pass is claimed and no dependency was installed. Model behavior/quality, fresh native client discovery, new live hooks, schedulers, external services and human acceptance were not exercised. No additional agents or push were used. Local Git staging was refused when creating `.git/index.lock` (`Permission denied`), so the release remains as reviewed changes in the `main` working tree rather than local commits.

### 0.2.3 clarification update

On 18 October 2026 (Asia/Vladivostok), the approved clarification paragraph was verified identical in the active source base and exported base. Package integrity passed for all 296 payload files. The complete existing local Windows suite passed: 23 tests in 141.988 seconds, including full startup preservation, instruction-budget refusal, all four client layouts, installation/removal ownership and memory helpers.

Only the global base instruction and its release/provenance documentation changed; specialist instructions, runtime helpers and installer code are unchanged. These checks establish text fidelity and package behavior. No model pilot, independent review or product-quality improvement is claimed.

### 0.2.1 refresh

On 17 October 2026, the refresh includes 296 payload files and 23 custom skill entries. Package integrity passed. The public Markdown check covered 364 local links/anchors with no newly broken references; the bounded scan of changed files found none of the source-machine/private-memory/credential identifiers it checks.

The first local Windows run executed all 23 tests in 114.213 seconds: 22 passed, and the startup-budget fixture failed because the shorter source instructions now fit where the old fixture expected overflow. The fixture was corrected to put the existing project instructions exactly at the declared default limit, so any added full bootstrap must be refused before writes. Its targeted rerun passed in 13.044 seconds, including preservation and the explicit higher-budget installation. Installer/runtime logic was unchanged; this is not a claim of a second complete local suite run.

The native skill-creator validator could not run in the source environment because PyYAML was absent. The edited simple metadata was checked separately; no dependency was installed and no complete YAML validation is claimed. No model pilots, additional agents, measured token savings or fresh client-capability acceptance are claimed by this refresh. Earlier independent-review/media results below remain historical.

### 0.2.0 refresh

On 15 October 2026 the refreshed package passed all **23 local Windows tests** in119.225seconds: the existing20 installation/ownership/MCP tests and3 new destination-memory scenarios. The new scenarios exercise current/history ranking with separate INBOX results; missing coverage/navigation setup; a valid synthetic registry/topology; detection of a lost reachable topic or an incorrect direct-root link; and unchanged vault bytes after read-only checks.

The source comparison covered298 files including141 Markdown instruction/reference documents. Seven existing source files changed since0.1.0 and six source files were added. The export adds three original synthetic setup templates, yielding292 payload files and the same23 custom skill entry points. Global base, general workflow, independent-review procedure, pinned capture/sync core and existing voxel validators remain byte-identical to0.1.0 after their established portable bindings. Dataset and license bytes are retained.

The illustrated guide was reviewed locally at900px. Its36-frame robot camera orbit has an infinite loop and a static alternative; independent inspection observed motion after late arrival. This is documentation/media evidence, not a new model-quality benchmark. The original0.1.0 evidence below remains historical evidence at its stated scope.

### Original 0.1.0 record

| Executed check | Observed result |
|---|---|
| Original configuration/workflow/custom-skill snapshot | All284 source files unchanged; source hooks unchanged since first inspection |
| Public payload | 283 files, 6,583,730 bytes, 23 custom entrypoints |
| Source/export fidelity | 243 byte-identical files; 40 files with recorded environment/owner/runtime/link/hook-template transformations |
| Searchable datasets and font attribution | All41 files match source SHA; Anya Danilova attribution preserved |
| Own package Markdown links | No unresolved actual local reference; fenced hypothetical project examples excluded |
| Syntax | 38 Python files compiled in memory; 8 Node modules passed node --check |
| Bounded privacy scan | No matching source-machine roots, private memory remote, actual VM UUID/MAC/name or credential-pattern values in payload |

The manifest preserves source/export hashes and transformation details. The scan is bounded, not proof against every possible secret encoding. No original notes, chats, connection settings or trust records are exported.

## Installer behavior

The current20-test author suite passed. Checks use the real CLI and synthetic targets, including:

- Complete startup body and UTF8BOM/CRLF roundtrip; preserved unrelated user text.
- Idempotent installation; all four native layouts; whole-workflow expansion to23 modules.
- Named sibling closure and skills-only actual-consent startup guard.
- Conflict before writes; modified owned files and identical preexisting user-owned files preserved.
- Arbitrary/canonical-neighbor, rehashed payload/policy, pruned completeness and mutually consistent destination metadata forgeries rejected.
- Independent private ownership record; no-write plan; unrelated neighbors preserved.
- Explicit empty memory initialization, repeat/conflict preservation and knowledge retained after removal.
- Codex default instruction budget/AGENTS.override guards and declared larger budget without global config changes.
- Real memory capture/read-back/idempotence and limited MCP rejection of unknown fields/operations.
- Dataset/source-hash and third-party font-author regression.

Removal needs the original private record and matching owned content. A second removal returns a no-receipt error and makes no writes; it is not a second successful removal. The installer/store must remain trusted; malicious rewriting of both trusted source/store and destination is outside the ownership boundary.

## Actual helpers and discovery

| Executed scenario | Result and scope |
|---|---|
| UI/UX search, design-system generation and stack search, same inputs before/after relocation | Three outputs byte-identical |
| All40 existing Gen2.1 voxel recipes before/after relocation, same seed | All121 VOX/OBJ/MTL/manifest files byte-identical; no new visual verdict inferred |
| Empty knowledge vault | Capture/read-back, repeat, conflicting identity rejection, search, checkpoint and status; no real private sync |
| Limited stdio MCP | Initialize/list/capture/checkpoint; two tools; unknown fields/operations, traversal-shaped input and synthetic credentials rejected |
| Quality ledger and task state | Technical fixture ready before edit, stale after edit; same linked Python validator executed with HARNESS_PYTHON |
| Hook handlers with synthetic native-event inputs | Prompt instruction; bounded memory continuation; checkpoint releases Stop; quality diagnostic nonblocking/deduplicated |
| Impeccable0.1.14 | Pinned binary SHA verified; mechanical detector executed on a controlled static fixture |
| Preserved PowerShell context wrapper | Execution rejected by signing policy; no protection disabled; wrapper execution not claimed |
| Codex CLI0.160.0 native catalog | Fresh skills/list forceReload found23/23 enabled target skills without errors; isolated CODEX_HOME, no model generation |

The restricted sandbox initially denied Node-to-Python spawning and an app-server SQLite write under the original home. The validator was exercised in an authorized isolated synthetic test; discovery used an isolated Codex home. These are execution conditions, not hidden successful checks. Native hooks were not registered/trusted during handler tests.

## Independent acceptance

Three different fresh-context reviewers examined successive versions. Author technical testing remained with the author. Reviewers received the original objective and expectations, recorded first impressions before author reports, and chose their own canaries.

- Round01 rejected receipt/ownership weakness, missing named dependency, damaged attribution, skills-only permission composition and startup-budget/override gap. Findings were repaired and regressed.
- Round02 confirmed those repairs and rejected two receipt defects: rehashed edited policy and missing entrypoint hidden by pruned metadata. Original ownership state is now separately recorded outside destination data.
- Round03 executed8 focused canary groups (40 CLI commands), verified source/composition and metadata boundaries, and found no confirmed blocker to publishing preserved methods, installer and documented compatibility. This is scoped package acceptance, not a creative/model benchmark or a human verdict on future output.

Private raw review/test artifacts contain local paths and stay local. This record reports their actual conclusions and limits.

## Deliberately unestablished

- Live Claude/DeepSeek/generic model trials and cross-model output/cost parity.
- Actual destination startup interpretation, native hook registration/trust and persistent MCP approval.
- Browser/image/format service availability in another client.
- Human perception of new artifacts or proof that a model obeys every condition.
- Private remote sync, scheduler/cloud curator activation or provisioned lab access.

Repository CI runs hashes and the author suite on Windows/Ubuntu. Its actual run status is the GitHub Actions result, separate from this local record. Follow INTEGRATIONS.md for destination acceptance; missing layers remain missing.

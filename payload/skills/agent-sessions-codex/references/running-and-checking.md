# Running and checking sessions

Start only what the user approved in the summary. Use the run command given in SKILL.md for your worker client.

## Before starting

1. **One place per writer.** Each session that changes files gets its own folder or git worktree. Two sessions never share files. Read-only sessions may share a folder.
2. **A known starting point.** Make sure each working folder has a clean state you can compare against: `git status` is clean, or you note the current commit. Without it you cannot tell later what the session changed.
3. **Briefs outside the project.** Keep briefs, logs and final messages in a local folder that is not tracked or published (your scratch directory, or a git-ignored folder). They contain the user's quotes, local paths and notes.
4. **A session log.** Keep one table for the whole task and update it after every run:

   ```
   | Session | Thread ID | Brief | Effort | Status | Verdict |
   |---------|-----------|-------|--------|--------|---------|
   | <name>  | <id>      | <file>| <level>| running / completed / failed | accepted / fix requested / redo |
   ```

   The thread ID comes from the JSON line the run prints last. You need it to continue the same session instead of starting a new one.

## Starting

- Run each session in the background and wait to be notified when it ends. Do not poll in a loop, and do not sleep-wait.
- Start independent sessions together. A session that waits for another starts only after you have checked and accepted the one it depends on.
- Tell the user the session names and where to watch them.
- If a run exits with 3 (client could not start) or 4 (unsupported option), nothing was created. Tell the user; do not retry with different settings on your own.

## Checking a finished session

The final message is the worker's claim. Check it against the files before you accept anything.

1. **Read the report.** Write down what the worker says it did, which checks it ran and what it says it did not verify. If the final message is about something else (a hook or memory error), read the event log for the real report.
2. **See what actually changed.** `git status` and `git diff --stat` in the working folder, against the starting point. Then read the diff of the files that matter. Look for changes nobody asked for.
3. **Rerun the checks.** Run the tests, builds and commands from the brief's acceptance yourself, at least the cheap ones. A test the worker reports as passed but that fails for you is a failure.
4. **Go through the requirements.** For each numbered requirement in the brief, name the evidence: a file and line, a test, a command output. A requirement without evidence is not done.
5. **Check the boundaries.** Nothing changed outside the scope; nothing pushed, published or deleted; no new dependencies unless allowed; old names or leftovers really gone if the brief said so.
6. **Try the behaviour, not only the tests.** Run the real scenario the user cares about, including an edge case: install and then upgrade, open the screen, feed an empty or very large input, run from a fresh clone. Tests passing while the real scenario fails is common. Typical findings of this step: files left behind after a migration, logic that works for only one version, a pipeline that fails in a clean environment.
7. **Decide.**
   - **Accepted:** every requirement has evidence and nothing is outside the boundaries.
   - **Fix requested:** something specific is wrong or missing. Continue the same session with a short follow-up brief (see [writing the brief](brief-writing.md)): what is wrong, what to do, how it will be checked. Pass the same settings again.
   - **Redo:** the result is wrong at its core. Continue the same session with a new brief, one effort level higher if the task was harder than its level.
   - Fix it yourself only when it is small and continuing the session is not worth it. Say that you did.
8. **Update the log** with the verdict and what you verified.

## Reporting

After all sessions are accepted, or when you need the user's decision, report in the user's language, per session:

- what it did;
- what you verified and how (which commands you ran, what you opened);
- what remains unverified and why;
- what the user needs to decide next: commit, push, publish, a choice between variants.

Do not commit, push or publish anything unless the user asked for it in this task.

# Finding out the requirements

A worker session only knows what the brief says. Before you write it, find out what the user wants well enough to write acceptance that can be checked. Talk to the user in their language.

The round-based interview below follows the "grilling" approach from Matt Pocock's skills: decisions form a tree, and each round asks everything that can be decided now.

## When to skip

Skip the interview when the task is small and unambiguous, when an accepted brief or plan already exists, or when the user said to proceed without questions. Restate the task in one line and continue.

## 1. Restate the goal

In one or two sentences, say what you understood: what should exist or change, and for whom. If the user corrects you, restate again before asking anything else.

## 2. Collect the facts yourself

Facts are your job, not the user's. Read the files, the code, earlier decisions and the conversation before asking. Never ask the user something you can look up: which framework is used, where a file is, what the current behaviour is.

## 3. List the open decisions

Go through this checklist and write down every point that is still open and would change the plan:

1. **Goal and audience.** What the result is for, and who uses or reads it.
2. **Done.** What the user will look at to decide it is finished: a screen, a passing check, a file, a number.
3. **Scope.** What is included, and what must not be touched.
4. **Existing material.** Designs, decisions, the user's own ideas that the result must build on.
5. **Constraints.** Stack, platform, design system, performance, deadlines, budget.
6. **Irreversible actions.** Deleting, publishing, pushing, sending, spending, migrating data.
7. **Priorities.** What wins when quality, speed and scope conflict.

Some decisions depend on others: the file format only matters once you know there is an export at all. Note which ones wait for which.

## 4. Ask in rounds

A round contains every open decision that can be answered now, that is, every one that does not depend on another question still open. A question that depends on an answer you do not have yet goes to a later round.

Number the questions. Give each one a short title, concrete options where they exist, and your recommended answer. The recommendation is what you will do if the user does not object.

```
**Q1 - <title>:** <question, with concrete options>
➡️ Recommended: <your answer and a one-line reason>

**Q2 - <title>:** <question>
➡️ Recommended: <your answer>
```

After the answers, update the list: settled decisions unblock the ones that waited for them. Ask the next round. There is no limit on the number of rounds; continue until no open decision would change the plan.

Keep each round readable. If more than about five questions are open at once, ask the ones that change the plan most and move the rest to the next round. That limits the size of a round, not the interview.

Do not ask about details the worker can decide well on its own, and do not ask again about something the user already decided.

## 5. Confirm

When nothing open would change the plan, show the user a short summary:

- **Goal:** one line.
- **Done when:** observable checks.
- **Not included:** what stays untouched.
- **Decided:** the answers from the rounds, including recommendations the user accepted by not objecting.

Wait for the user's yes or corrections, then write the session plan and the briefs.

## Example

User: "Add an export button to the expenses dashboard."

Restate: "You want to download the expenses shown on the dashboard and work with them in a spreadsheet. Right?"

Facts collected without asking: the dashboard is React; the table is built from `src/data/expenses.ts`; filters live in `src/components/Filters.tsx`.

Round 1:

**Q1 - What to export:** only the rows that match the current filters, or all expenses?
➡️ Recommended: the filtered rows, since that is what you see when you press the button.

**Q2 - Format:** CSV or an Excel file?
➡️ Recommended: CSV; it opens in Excel and Google Sheets and needs no new library.

After the answers (filtered rows, CSV), a decision that waited for Q2 opens.

Round 2:

**Q3 - Excel in Russian:** the file should open correctly in Russian Excel by double click, which needs `;` separators and decimal commas. Is that how you open it?
➡️ Recommended: yes, format for Russian Excel.

Summary:

- **Goal:** download the currently filtered expenses as CSV for analysis in a spreadsheet.
- **Done when:** the button next to the filters downloads a CSV; the rows match the table on screen; Russian text and amounts open correctly in Excel by double click; an empty filter gives a file with headers only.
- **Not included:** changes to the filters, charts or data source.
- **Decided:** filtered rows; CSV for Russian Excel; button next to the filters.

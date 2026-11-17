# Authoring rules for handbook chapters

`python3 build.py` builds `src/**/*.md` into `docs/`. It prints a warning for every standard a chapter misses. `python3 build.py --strict` fails on any warning; run it before publishing.

## Files

| Path | What |
| --- | --- |
| `src/<track>/mNN-name.md` | One chapter. Front matter needs `title`, `book`, `module`, `kicker`, `home`, `lab`, `difficulty`, `status`, `verified`, `footer` |
| `src/<track>/index.md` | Track home. `[[chapters]]` lists the chapters automatically |
| `figures/<track>_mNN.py` | That chapter's diagrams, registered with `@diagram("mNN-name")` |
| `verification/<track>/mNN-name.md` | Verification report against the official module. Never built into `docs/` |
| `archive/` | Superseded versions. Not built |

## Tags (standard B)

| Write | Effect |
| --- | --- |
| `## 3. Host discovery {U}` | Tag badge on a heading. Every numbered `##` section must have one |
| `### Ports {M: Port ranges: 0-1023 well-known; ...}` | Badge, and the short fact goes to the cheat sheet |
| `... a sentence. {M}` or a table row containing `{M}` | Badge, and the whole line or row is copied to the cheat sheet |
| `| Port | Service {M} |` in a table header | The whole table is copied to the cheat sheet |
| `{U}` `{R}` `{D}` | Badge only |

Prefer the short form `{M: fact}`. The cheat sheet must print on one landscape page; if it runs over, shorten facts or demote them. Tag a fact MEMORISE only if the exam could ask it directly.

## Boxes (standards A, C, D, F)

Each chapter needs at least one of every box. Write them as `!!! kind "Title"` with the body indented four spaces.

| Kind | Use |
| --- | --- |
| `story` | The everyday analogy. One per concept |
| `before` | "Before you start": assumed ideas with one-line refreshers |
| `why` | Why it matters: exam candidate, defender, sensitive-data worker |
| `try` | One command to run in the lab |
| `remember` | A mnemonic |
| `recap` | Five lines. Required at the end of every numbered section |
| `exam` | "Exam answer / In practice", where the two differ |
| `trap` | Exam traps |
| `cpent`, `coasp` | Depth and link insets |
| `hospital` | The one healthcare worked example. Add a line carrying it to another industry |

Markers on their own line: `[[meta]]` (reading time, lab time, difficulty), `[[legend]]`, `[[cheatsheet]]`.

## Quiz

Twelve questions in a ```` ```quiz ```` block, separated by blank lines:

    Q: Question text, `code` allowed
    - wrong option
    - * the one correct option
    - wrong option
    WHY: one-sentence explanation
    TAG: M

Options are shuffled in the browser, so never write "all of the above" or refer to option letters.

## Writing

- Paragraphs under 110 words (the build warns). One idea each.
- Original words, diagrams and examples only. Read the official module for facts and coverage; never paste or closely reword it, in the chapter or in the report.
- Where the official answer and the RFC or tool documentation disagree, teach both in an `exam` box and make the exam answer the MEMORISE item.

## Updated boxes (courseware that has fallen behind)

Where the official module describes a standard, law, framework or tool that has since changed, check the owner's own website and add an `update` box:

    !!! update "Updated: April 2026"
        **What changed.** One or two sentences, with the month and year in bold.

        **The exam still expects:** the courseware's version, stated plainly.

Rules: the title carries the month and year of the change. Say when the status was checked if it could move again. If the exam still expects the old answer, that old answer stays the MEMORISE item; the update is UNDERSTAND. Record the source of each update in the chapter's verification report, and say there if the source was not the owner's own site.

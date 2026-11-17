# Cybersecurity Study Handbook

By **Dr. Atul Tiwari**

Original, plain-language study handbooks for ethical hacking (CEH), penetration testing (CPENT level) and offensive AI security (COASP). Written for anyone: students, IT staff, clinicians, career-changers.

**Read it online:** https://atultiwari.github.io/cybersecurity-study-handbook/

## What each chapter gives you

- An opening anyone can follow: what the chapter is about, what it assumes, why it matters.
- MEMORISE / UNDERSTAND / RECOGNISE / DO tags on every section and key fact.
- "Try it" lab commands, "Remember" mnemonics, a five-line recap per section.
- "Exam answer / In practice" boxes where the exam and the real world differ.
- "Updated" boxes, with month and year, where a standard, law or tool has moved on since the official courseware was written.
- A 12-question quiz and a one-page exam cheat sheet.

## Status

| Track | Chapters published |
| --- | --- |
| Ethical hacking (CEH v13 syllabus) | Module 1, Module 2, Module 3 (review drafts) |
| Penetration testing bridge | Not started |
| Offensive AI security (COASP) | Not started |

The hands-on labs the chapters refer to (L01 onwards) are not in this repository yet.

## Build it yourself

    pip install markdown
    python3 build.py --strict

`src/` holds the chapters in Markdown, `figures/` the diagrams, `docs/` the built site that GitHub Pages serves. Authoring rules are in `AUTHORING.md`.

## Independence and copyright

This is unofficial, independent study material. It is not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Every chapter is written in the author's own words, with original diagrams and examples, from public standards and tool documentation; official courseware is used only to check coverage.

© 2026 Dr. Atul Tiwari. All rights reserved.

Use the techniques described here only on systems you own or are authorised in writing to test.

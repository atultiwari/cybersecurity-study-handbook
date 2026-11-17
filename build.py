#!/usr/bin/env python3
"""Builds the study handbook: src/**/*.md -> docs/**/*.html (self-contained pages, GitHub Pages ready).

    python3 build.py            build everything, print lint warnings
    python3 build.py --strict   same, but exit 1 if any chapter has a warning (use before publishing)

Requires: pip install markdown.   Authoring rules: see AUTHORING.md.
"""
import html, importlib.util, pathlib, re, sys
import markdown

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
import diagrams  # noqa: E402

for _f in sorted((ROOT / "figures").glob("*.py")):
    _spec = importlib.util.spec_from_file_location("fig_" + _f.stem, _f)
    _spec.loader.exec_module(importlib.util.module_from_spec(_spec))

CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")

TAGS = {"M": ("MEMORISE", "Likely to be asked directly. Know it exactly."),
        "U": ("UNDERSTAND", "Needed to reason through scenario questions. Do not recite it."),
        "R": ("RECOGNISE", "Know the name and what it does when you see it in an option list."),
        "D": ("DO", "A hands-on skill for the practical exams. Run it at a keyboard.")}
TAG = re.compile(r"\{([MURD])(?::\s*([^}]*))?\}")   # {M} or {M: short fact for the cheat sheet}
# Every chapter must contain at least one of each of these boxes (standards A, C, D, F).
REQUIRED_BOXES = ["before", "why", "story", "try", "remember", "recap", "exam", "trap", "cpent", "coasp", "hospital"]
REQUIRED_MARKERS = ["[[meta]]", "[[legend]]", "[[cheatsheet]]"]
AUTHOR = "Dr. Atul Tiwari"
YEAR = "2026"
QUIZ_SIZE = 12
MAX_PARA_WORDS = 110
FENCE = re.compile(r"^\s*(```|~~~)")
SEP = re.compile(r"^\|?\s*:?-{3,}")


def front_matter(text):
    meta = {}
    if text.startswith("---"):
        _, head, text = text.split("---", 2)
        for line in head.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, text


def tag_html(code):
    name, tip = TAGS[code]
    return f'<span class="tag tag-{code}" title="{tip}">{name}</span>'


def clean_title(s):
    return re.sub(r"^\d+\.\s*", "", TAG.sub("", s)).strip()


def scan_source(text):
    """One pass over the Markdown, outside code fences. Returns
    (text with heading tags turned into classes, cheat-sheet Markdown, lint warnings)."""
    out, warns, sheet, order = [], [], {}, []
    fence = False
    h2 = None
    header = None            # current table header line, when inside a table
    para = 0
    sec = {}                 # numbered h2 -> has a recap box
    lines = text.splitlines()

    def note(key, item):
        if key not in sheet:
            sheet[key] = []; order.append(key)
        sheet[key].append(item)

    def facts(s):
        """Short-form facts on a line: the text of every {M: ...} tag."""
        return [m.group(2).strip() for m in TAG.finditer(s) if m.group(1) == "M" and m.group(2)]

    def plain_m(s):
        return any(m.group(1) == "M" and not m.group(2) for m in TAG.finditer(s))
    for i, line in enumerate(lines):
        s = line.strip()
        if FENCE.match(line):
            fence = not fence
        if fence or FENCE.match(line):
            out.append(line); para = 0; continue
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            title = m.group(2)
            t = TAG.search(title)
            if m.group(1) == "##":
                h2 = clean_title(title)
                if re.match(r"\d+\.", title):
                    sec[h2] = False
                    if not t:
                        warns.append(f"section '{h2}' has no {{M}}/{{U}}/{{R}}/{{D}} tag")
            if t:
                for f in facts(title):
                    note((h2, None), f)
                line = f"{m.group(1)} {TAG.sub('', title).strip()} {{: .tg-{t.group(1)} }}"
            out.append(line); para = 0; header = None; continue
        if s.startswith("!!! recap") and h2 in sec:
            sec[h2] = True
        # tables: remember the header so memorise rows can be rebuilt in the cheat sheet
        if s.startswith("|"):
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if header is None and SEP.match(nxt):
                header = s
            elif header is not None and not SEP.match(s):
                if facts(s):
                    for f in facts(s):
                        note((h2, None), f)
                elif plain_m(s) or plain_m(header):
                    note((h2, header), s)
            para = 0
        else:
            header = None
            if facts(s):
                for f in facts(s):
                    note((h2, None), f)
            elif plain_m(s) and not s.startswith("!!!"):
                note((h2, None), re.sub(r"^([-*]|\d+\.)\s+", "", s))
            if s and not s.startswith(("!!!", "[[", "-", "*", ">", "<")) and not re.match(r"\d+\.\s", s):
                para += len(s.split())
                if para > MAX_PARA_WORDS:
                    warns.append(f"paragraph over {MAX_PARA_WORDS} words near line {i + 1}: '{s[:50]}...'")
                    para = -10 ** 6
            else:
                para = 0
        out.append(line)
    for name, ok in sec.items():
        if not ok and not re.match(r"(?i)(quiz|lab)", name):
            warns.append(f"section '{name}' has no recap box")
    # build the cheat sheet, grouped by section in reading order
    md, seen = [], []
    for h in [k[0] for k in order]:
        if h in seen:
            continue
        seen.append(h)
        md.append(f"\n**{h or 'General'}**\n")
        bullets = [x for k in order if k == (h, None) for x in sheet[k]]
        md += [f"- {TAG.sub('', b).strip()}" for b in bullets]
        for k in order:
            if k[0] == h and k[1]:
                cols = k[1].count("|") - 1
                md += ["", TAG.sub("", k[1]), "|" + " --- |" * cols] + [TAG.sub("", r) for r in sheet[k]] + [""]
    return "\n".join(out), "\n".join(md), warns


def quiz(block, warns):
    """Blocks separated by blank lines:  Q: text / - option / - * correct option / WHY: text / TAG: M"""
    out, n = ['<div class="quiz">'], 0
    for chunk in re.split(r"\n\s*\n", block.strip()):
        q, why, tag, opts = "", "", "", []
        for l in chunk.strip().splitlines():
            l = l.strip()
            if l.startswith("Q:"): q = l[2:].strip()
            elif l.startswith("WHY:"): why = l[4:].strip()
            elif l.startswith("TAG:"): tag = l[4:].strip()
            elif l.startswith("- "): opts.append(l[2:].strip())
        good = [o for o in opts if o.startswith("* ")]
        n += 1
        if not q or not why or len(good) != 1 or len(opts) < 3:
            warns.append(f"quiz question {n} is malformed (needs Q:, 3+ options, exactly one '- * ' answer, WHY:)")
            continue
        badge = tag_html(tag) if tag in TAGS else ""
        out.append(f'<div class="q"><p><b>{n}.</b> {inline(q)} {badge}</p>')
        for o in opts:
            ok = o.startswith("* ")
            out.append(f'<button type="button"{" data-ok" if ok else ""}>{inline(o[2:] if ok else o)}</button>')
        out.append(f'<p class="why" hidden>{inline(why)}</p></div>')
    if n != QUIZ_SIZE:
        warns.append(f"quiz has {n} questions, expected {QUIZ_SIZE}")
    out.append('<p class="score" aria-live="polite"></p></div>')
    return "\n".join(out)


def inline(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s))


def outside_code(body, fn):
    parts = re.split(r"(<pre.*?</pre>|<code.*?</code>)", body, flags=re.S)
    return "".join(p if i % 2 else fn(p) for i, p in enumerate(parts))


def legend():
    rows = "".join(f"<li>{tag_html(c)} {tip}</li>" for c, (_, tip) in TAGS.items())
    return f'<ul class="legend">{rows}</ul>'


def chapters(folder):
    """Chapters (files with a module: number) in one track folder, in module order."""
    found = []
    for f in sorted(folder.glob("*.md")):
        meta, _ = front_matter(f.read_text(encoding="utf-8"))
        if meta.get("module", "").isdigit():
            found.append((int(meta["module"]), f, meta))
    return sorted(found, key=lambda c: c[0])


def chapter_table(folder, prefix=""):
    rows = ["| Module | Chapter | Status | Checked against |", "| --- | --- | --- | --- |"]
    for num, f, meta in chapters(folder):
        rows.append(f"| {num} | [{meta.get('title', f.stem)}]({prefix}{f.stem}.html) | {meta.get('status', '')} | {meta.get('verified', '')} |")
    return "\n".join(rows) if len(rows) > 2 else "No chapters built yet."


def build(src):
    meta, text = front_matter(src.read_text(encoding="utf-8"))
    is_chapter = meta.get("module", "").isdigit()
    warns = []
    text, sheet_md, w = scan_source(text)
    if is_chapter:
        warns += w
        for mk in REQUIRED_MARKERS:
            if mk not in text:
                warns.append(f"missing {mk}")
        for box in REQUIRED_BOXES:
            if not re.search(rf"^\s*!!! {box}\b", text, flags=re.M):
                warns.append(f"no '!!! {box}' box")
        if not re.search(r"^## .*Coverage", text, flags=re.M):
            warns.append("no coverage table section")
        if not sheet_md.strip():
            warns.append("nothing tagged {M}, so the cheat sheet is empty")
        report = ROOT / "verification" / src.relative_to(ROOT / "src")
        if not report.exists():
            warns.append(f"no verification report at {report.relative_to(ROOT)}")

    text = text.replace("[[cheatsheet]]", f'<div class="cheat" markdown="1">\n{sheet_md}\n</div>')
    if "[[chapters]]" in text:
        if src.parent == ROOT / "src":
            parts = []
            for d in sorted(p for p in src.parent.iterdir() if p.is_dir()):
                parts.append(f"### {d.name.upper()} track\n\n{chapter_table(d, d.name + '/')}")
            text = text.replace("[[chapters]]", "\n\n".join(parts))
        else:
            text = text.replace("[[chapters]]", chapter_table(src.parent))

    stash = []
    def keep(h):
        stash.append(h); return f"\n\nSTASH{len(stash)-1}END\n\n"
    def fig(m):
        try:
            return keep(f'<figure class="dg">{diagrams.render(m.group(1))}<figcaption>{html.escape(m.group(2).strip())}</figcaption></figure>')
        except KeyError as e:
            warns.append(str(e)); return ""
    text = re.sub(r"```diagram\s+(\S+)\n(.*?)```", fig, text, flags=re.S)
    text = re.sub(r"```quiz\n(.*?)```", lambda m: keep(quiz(m.group(1), warns)), text, flags=re.S)
    if is_chapter and "class=\"quiz\"" not in "".join(stash):
        warns.append("no quiz")
    text = text.replace("[[legend]]", keep(legend())).replace("[[meta]]", "\n\nMETASTRIP\n\n")

    md = markdown.Markdown(extensions=["tables", "fenced_code", "admonition", "toc", "attr_list", "sane_lists", "md_in_html"],
                           extension_configs={"toc": {"toc_depth": "2-3"}})
    body = md.convert(text)
    body = re.sub(r"<p>STASH(\d+)END</p>", lambda m: stash[int(m.group(1))], body)
    body = re.sub(r'<(h[234])([^>]*class="tg-([MURD])"[^>]*)>(.*?)</\1>',
                  lambda m: f"<{m.group(1)}{m.group(2)}>{m.group(4)} {tag_html(m.group(3))}</{m.group(1)}>", body, flags=re.S)
    body = outside_code(body, lambda p: TAG.sub(lambda m: tag_html(m.group(1)), p))
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    read = max(5, round(words / 200 / 5) * 5)   # 200 words a minute, rounded to 5 minutes
    strip = "".join(f"<span><b>{k}</b> {html.escape(v)}</span>" for k, v in [
        ("Reading", f"about {read} min"), ("Lab", meta.get("lab", "") and meta["lab"] + " min"),
        ("Difficulty", meta.get("difficulty", "")), ("Checked", meta.get("verified", ""))] if v)
    body = body.replace("<p>METASTRIP</p>", f'<p class="meta">{strip}</p>')

    nav = ""
    if is_chapter:
        sib = chapters(src.parent)
        i = [c[1] for c in sib].index(src)
        prev = f'<a href="{sib[i-1][1].stem}.html">← Module {sib[i-1][0]}</a>' if i else "<span></span>"
        nxt = f'<a href="{sib[i+1][1].stem}.html">Module {sib[i+1][0]} →</a>' if i + 1 < len(sib) else "<span></span>"
        nav = f'<nav class="pn" aria-label="Chapters">{prev}{nxt}</nav>'

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="author" content="{AUTHOR}"><title>{html.escape(meta.get('title','Handbook'))}</title><style>{CSS}</style></head>
<body><header class="top"><button type="button" id="menu" class="mbtn" aria-expanded="false" aria-controls="side">Contents</button><a href="{meta.get('home','index.html')}">{html.escape(meta.get('book','Handbook'))}</a>
<input id="find" type="search" placeholder="Filter sections" aria-label="Filter sections"></header>
<div class="wrap"><nav class="side" id="side" aria-label="Contents">{md.toc}</nav>
<main><p class="kicker">{html.escape(meta.get('kicker',''))}</p>{body}{nav}
<footer><p>Written and maintained by <b>{AUTHOR}</b>. &copy; {YEAR} {AUTHOR}. All rights reserved.</p><p>{html.escape(meta.get('footer',''))}</p></footer></main></div>
<script>{JS}</script></body></html>"""
    out = ROOT / "docs" / src.relative_to(ROOT / "src").with_suffix(".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {words} words" + ("" if not warns else f"  {len(warns)} warning(s)"))
    for x in warns:
        print("   ! " + x)
    return len(warns)


if __name__ == "__main__":
    total = sum(build(f) for f in sorted((ROOT / "src").rglob("*.md")))
    if total and "--strict" in sys.argv:
        sys.exit(f"{total} warning(s): fix them before publishing")

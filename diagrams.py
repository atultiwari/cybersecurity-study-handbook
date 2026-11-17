"""Diagram toolkit for the handbook: SVG primitives plus a registry.

Chapter diagrams live in figures/<track>_<module>.py and register themselves:

    from diagrams import diagram, flow, seq, pair, tree, svg, text

    @diagram("m03-method")
    def method():
        return flow(nodes, edges, 730, 525, "Scanning workflow")

A chapter then uses  ```diagram m03-method  followed by a caption line.
Every diagram is original work. Never trace a vendor's figure.
"""
import html

REG = {}

DEFS = ('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path class="ar" d="M0 0L10 5L0 10z"/></marker></defs>')


def diagram(name):
    """Register a zero-argument function that returns an <svg> string."""
    def wrap(fn):
        if name in REG:
            raise ValueError(f"diagram name used twice: {name}")
        REG[name] = fn
        return fn
    return wrap


def render(name):
    if name not in REG:
        raise KeyError(f"unknown diagram '{name}'. Known: {', '.join(sorted(REG))}")
    return REG[name]()


def svg(w, h, body, label):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{html.escape(label)}">{DEFS}{body}</svg>'


def text(x, y, s, cls="", anchor="middle"):
    lines = s.split("\n")
    y0 = y - (len(lines) - 1) * 8
    return "".join(f'<text x="{x}" y="{y0 + i * 16}" text-anchor="{anchor}" class="{cls}">{html.escape(l)}</text>'
                   for i, l in enumerate(lines))


# ---------------------------------------------------------------- sequence
def seq(lanes, msgs, x0=0, w=None, title=None, gap=None):
    """lanes: names. msgs: (frm, to, label[, style]) style: ''|'x' (no reply / dropped)|'note'."""
    n = len(lanes)
    gap = gap or (230 if n == 2 else 200)
    w = w or gap * (n - 1) + 160
    xs = [x0 + 80 + i * gap for i in range(n)]
    out, y = [], 22
    if title:
        out.append(text(x0 + w / 2, y, title, "h")); y += 22
    for x, name in zip(xs, lanes):
        out.append(f'<rect class="b" x="{x-62}" y="{y}" width="124" height="28" rx="6"/>' + text(x, y + 19, name, "h"))
    top = y + 28
    y = top + 30
    rows = []
    for m in msgs:
        frm, to, label = m[0], m[1], m[2]
        style = m[3] if len(m) > 3 else ""
        if style == "note":
            rows.append(text(x0 + w / 2, y, label, "s")); y += 26; continue
        a, b = xs[frm], xs[to]
        d = 1 if b > a else -1
        if style == "x":
            mid = a + (b - a) * 0.62
            rows.append(f'<line class="ln da" x1="{a}" y1="{y}" x2="{mid}" y2="{y}"/>'
                        f'<text x="{mid + 8*d}" y="{y+5}" text-anchor="middle" class="bad h">✕</text>')
        else:
            rows.append(f'<line class="ln" x1="{a + 3*d}" y1="{y}" x2="{b - 3*d}" y2="{y}" marker-end="url(#a)"/>')
        rows.append(text((a + b) / 2, y - 7, label, "s"))
        y += 40
    bottom = y - 14
    for x in xs:
        out.append(f'<line class="lf" x1="{x}" y1="{top}" x2="{x}" y2="{bottom}"/>')
    return "".join(out + rows), w, bottom + 8


def pair(left, right, lanes=("Scanner", "Target"), label=""):
    """Two sequence diagrams side by side, e.g. open port versus closed port."""
    b1, w1, h1 = seq(lanes, left[1], title=left[0])
    b2, w2, h2 = seq(lanes, right[1], x0=w1 + 30, title=right[0])
    h = max(h1, h2)
    div = f'<line class="lf" x1="{w1+15}" y1="6" x2="{w1+15}" y2="{h}"/>'
    return svg(w1 + w2 + 30, h + 6, b1 + div + b2, label)


def single(lanes, msgs, label, gap=250):
    b, w, h = seq(lanes, msgs, gap=gap)
    return svg(w, h + 6, b, label)


# -------------------------------------------------------------------- flow
def flow(nodes, edges, w, h, label):
    """nodes: id -> (cx, cy, w, h, text, cls)  cls: b box | t rounded | d decision diamond.
    edges: (a, b, label, mode)  mode: v | h | hv | vh, or a raw SVG path starting with 'M'
    for the rare arrow the four modes cannot route."""
    out = []
    for a, b, lab, mode in edges:
        if mode.startswith("M"):
            out.append(f'<path class="ln" d="{mode}" marker-end="url(#a)"/>')
            continue
        ax, ay, aw, ah = nodes[a][:4]; bx, by, bw, bh = nodes[b][:4]
        if mode == "v":
            y1, y2 = (ay + ah / 2, by - bh / 2) if by > ay else (ay - ah / 2, by + bh / 2)
            out.append(f'<line class="ln" x1="{ax}" y1="{y1}" x2="{bx}" y2="{y2}" marker-end="url(#a)"/>')
            lx, ly = ax + 8, (y1 + y2) / 2 + 4; anc = "start"
        elif mode == "h":
            x1, x2 = (ax + aw / 2, bx - bw / 2) if bx > ax else (ax - aw / 2, bx + bw / 2)
            out.append(f'<line class="ln" x1="{x1}" y1="{ay}" x2="{x2}" y2="{by}" marker-end="url(#a)"/>')
            lx, ly = (x1 + x2) / 2, ay - 6; anc = "middle"
        elif mode == "hv":
            x1 = ax + aw / 2 if bx > ax else ax - aw / 2
            y2 = by - bh / 2 if by > ay else by + bh / 2
            out.append(f'<path class="ln" d="M{x1} {ay}H{bx}V{y2}" marker-end="url(#a)"/>')
            lx, ly = (x1 + bx) / 2, ay - 6; anc = "middle"
        else:  # vh
            y1 = ay + ah / 2 if by > ay else ay - ah / 2
            x2 = bx - bw / 2 if bx > ax else bx + bw / 2
            out.append(f'<path class="ln" d="M{ax} {y1}V{by}H{x2}" marker-end="url(#a)"/>')
            lx, ly = ax + 8, (y1 + by) / 2 + 4; anc = "start"
        if lab:
            out.append(f'<text x="{lx}" y="{ly}" text-anchor="{anc}" class="s h">{html.escape(lab)}</text>')
    for cx, cy, bw, bh, t, cls in nodes.values():
        if cls == "d":
            pts = f"{cx},{cy-bh/2} {cx+bw/2},{cy} {cx},{cy+bh/2} {cx-bw/2},{cy}"
            out.append(f'<polygon class="d" points="{pts}"/>')
        else:
            out.append(f'<rect class="{cls}" x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="{18 if cls=="t" else 6}"/>')
        out.append(text(cx, cy + 5, t))
    return svg(w, h, "".join(out), label)


# -------------------------------------------------------------------- tree
def tree(rows, label, w=640, rh=36, ind=30):
    """Indented family tree. rows: (depth, text[, cls]) in display order."""
    out, last = [], {}
    for i, r in enumerate(rows):
        d, t = r[0], r[1]
        cls = r[2] if len(r) > 2 else ("t" if d == 0 else "b")
        x, y = 14 + d * ind, 8 + i * rh
        bw = min(w - x - 14, max(110, int(7.4 * len(t)) + 26))
        if d and d - 1 in last:
            px, py = 14 + (d - 1) * ind + 12, last[d - 1]
            out.append(f'<path class="lf" d="M{px} {py + 26}V{y + 13}H{x}"/>')
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{bw}" height="26" rx="6"/>'
                   + text(x + 12, y + 18, t, "h" if d < 2 else "", "start"))
        last[d] = y
    return svg(w, 8 + len(rows) * rh, "".join(out), label)


# -------------------------------------------------------------------- bar
def bar(segs, label, w=660, h=96, note=""):
    """A row of labelled segments. segs: (width_weight, top_text, bottom_text, cls)."""
    tot = sum(s[0] for s in segs)
    x, out = 10, []
    for wt, top, bot, cls in segs:
        sw = (w - 20) * wt / tot
        out.append(f'<rect class="{cls}" x="{x}" y="14" width="{sw}" height="50" rx="4"/>'
                   + text(x + sw / 2, 36, top, "h") + text(x + sw / 2, 54, bot, "s"))
        x += sw
    if note:
        out.append(text(w / 2, 84, note, "s"))
    return svg(w, h, "".join(out), label)


# ------------------------------------------------------------------ ladder
def ladder(rows, label, w=660, bw=230, rh=50):
    """Numbered steps down the page with a one-line note beside each. rows: (title, note[, cls])."""
    out = []
    for i, r in enumerate(rows):
        y = 8 + i * rh
        cls = r[2] if len(r) > 2 else "b"
        out.append(f'<rect class="{cls}" x="14" y="{y}" width="{bw}" height="32" rx="6"/>'
                   + text(14 + bw / 2, y + 21, r[0], "h"))
        if r[1]:
            out.append(text(14 + bw + 16, y + 21, r[1], "s", "start"))
        if i + 1 < len(rows):
            out.append(f'<line class="ln" x1="{14 + bw / 2}" y1="{y + 32}" x2="{14 + bw / 2}" y2="{y + rh}" marker-end="url(#a)"/>')
    return svg(w, 8 + len(rows) * rh - (rh - 32) + 8, "".join(out), label)

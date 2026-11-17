"""Diagrams for CEH Module 1, Introduction to Ethical Hacking. All original."""
from diagrams import diagram, bar, ladder, tree, svg, text


@diagram("m01-elements")
def elements():
    return bar([(2, "Confidentiality", "only the right eyes", "t"), (2, "Integrity", "not altered", "t"),
                (2, "Availability", "there when needed", "t"), (2, "Authenticity", "genuinely from them", "d"),
                (2, "Non-repudiation", "cannot deny it later", "d")],
               "The five elements of information security", w=690,
               note="The first three are the classic CIA triad. The exam counts all five.")


@diagram("m01-attack")
def attack():
    out = []
    xs = [(20, "Motive", "why: the goal"), (240, "Method", "how: the TTPs"), (460, "Vulnerability", "where: the weakness")]
    for x, t, s in xs:
        out.append(f'<rect class="b" x="{x}" y="14" width="170" height="50" rx="6"/>' + text(x + 85, 36, t, "h") + text(x + 85, 54, s, "s"))
    out.append(text(215, 46, "+", "h") + text(435, 46, "+", "h"))
    out.append(f'<line class="ln" x1="325" y1="64" x2="325" y2="92" marker-end="url(#a)"/>')
    out.append(f'<rect class="d" x="240" y="94" width="170" height="34" rx="6"/>' + text(325, 116, "Attack", "h"))
    return svg(650, 136, "".join(out), "Attack equals motive plus method plus vulnerability")


@diagram("m01-phases")
def phases():
    return ladder([("1. Reconnaissance", "Footprinting, scanning, enumeration. Passive or active."),
                   ("2. Vulnerability scanning", "Find and classify the weaknesses."),
                   ("3. Gaining access", "Exploit, crack passwords, then escalate privileges."),
                   ("4. Maintaining access", "Keep control: backdoors, use the host as a launchpad."),
                   ("5. Clearing tracks", "Erase logs and evidence to stay undetected.")],
                  "The CEH ethical hacking framework")


@diagram("m01-killchain")
def killchain():
    return ladder([("1. Reconnaissance", "Research the target, find weak points."),
                   ("2. Weaponization", "Build the payload: exploit plus backdoor."),
                   ("3. Delivery", "Send it: email, link, USB, watering hole."),
                   ("4. Exploitation", "The code runs by abusing a vulnerability."),
                   ("5. Installation", "Install malware to stay in."),
                   ("6. Command and control", "Two-way channel back to the attacker."),
                   ("7. Actions on objectives", "Steal, disrupt or destroy.")],
                  "The seven phases of the cyber kill chain", rh=46)


@diagram("m01-diamond")
def diamond():
    pts = {"Adversary": (330, 30), "Infrastructure": (120, 150), "Capability": (540, 150), "Victim": (330, 270)}
    out = ['<polygon class="lf" points="330,46 150,150 330,254 510,150"/>',
           '<line class="lf" x1="330" y1="46" x2="330" y2="254"/>', '<line class="lf" x1="150" y1="150" x2="510" y2="150"/>']
    for name, (x, y) in pts.items():
        out.append(f'<rect class="t" x="{x-70}" y="{y-16}" width="140" height="32" rx="6"/>' + text(x, y + 5, name, "h"))
    out.append(text(215, 92, "uses", "s") + text(445, 92, "develops", "s") + text(215, 215, "connects to", "s") + text(445, 215, "exploits", "s"))
    return svg(660, 296, "".join(out), "The Diamond Model: adversary, capability, infrastructure, victim")


@diagram("m01-did")
def did():
    layers = ["Policies, procedures and awareness", "Physical", "Perimeter", "Internal network", "Host", "Application", "Data"]
    out = []
    for i, name in enumerate(layers):
        x, y, w, h = 12 + i * 34, 8 + i * 28, 640 - i * 68, 246 - i * 28 - (i * 6)
        out.append(f'<rect class="{"d" if i == 6 else "b"}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                   + text(x + w / 2, y + 19, name, "h" if i == 6 else "s"))
    return svg(664, 262, "".join(out), "Defence in depth: layers of protection around the data")


@diagram("m01-risk")
def risk():
    cols = ["Low", "Medium", "High"]
    grid = [["Medium", "High", "Extreme"], ["Low", "Medium", "High"], ["Low", "Low", "Medium"]]
    rows = ["Likely", "Possible", "Unlikely"]
    cls = {"Low": "t", "Medium": "b", "High": "d", "Extreme": "d"}
    out = [text(380, 20, "Consequence", "h"), text(54, 120, "Likelihood", "h")]
    for j, c in enumerate(cols):
        out.append(text(230 + j * 150, 44, c, "s"))
    for i, r in enumerate(rows):
        out.append(text(128, 80 + i * 46, r, "s"))
        for j in range(3):
            v = grid[i][j]
            out.append(f'<rect class="{cls[v]}" x="{160 + j * 150}" y="{56 + i * 46}" width="140" height="38" rx="4"/>'
                       + text(230 + j * 150, 80 + i * 46, v, "h" if v in ("High", "Extreme") else ""))
    return svg(640, 204, "".join(out), "A simple risk matrix: likelihood against consequence")


@diagram("m01-intel")
def intel():
    return ladder([("Strategic", "For executives and the CISO. Business risk, trends, money. Long-term."),
                   ("Tactical", "For security and SOC managers, architects. Attacker TTPs."),
                   ("Operational", "For incident response heads, defenders. Specific incoming threats."),
                   ("Technical", "For SOC staff and IR teams. Individual IoCs. Shortest-lived.")],
                  "Four types of threat intelligence, by who consumes them", w=690, bw=150)


@diagram("m01-ihr")
def ihr():
    return ladder([("1. Preparation", "Policies, team, tools, training."),
                   ("2. Recording and assignment", "Report it, log it, raise a ticket."),
                   ("3. Triage", "Analyse, validate, categorise, prioritise."),
                   ("4. Notification", "Tell management, vendors, clients."),
                   ("5. Containment", "Stop it spreading."),
                   ("6. Evidence and forensics", "Collect evidence, investigate."),
                   ("7. Eradication", "Remove the root cause."),
                   ("8. Recovery", "Restore systems and data."),
                   ("9. Post-incident activities", "Document, assess impact, revise policy, disclose.")],
                  "The nine steps of incident handling and response", rh=42)

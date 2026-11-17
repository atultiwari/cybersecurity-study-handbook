"""Diagrams for CEH Module 2, Footprinting and Reconnaissance. All original."""
from diagrams import diagram, flow, ladder, pair, single, tree, svg, text


@diagram("m02-types")
def types():
    out = []
    cols = [(20, "Passive footprinting", "t", ["No direct contact with the target", "Search engines, social networks,", "archives, paid databases, shared intel", "Very hard for the target to notice"]),
            (350, "Active footprinting", "d", ["Direct contact with the target", "DNS interrogation, social engineering,", "network and port scanning, enumeration", "May leave traces and raise an alert"])]
    for x, title, cls, lines in cols:
        out.append(f'<rect class="{cls}" x="{x}" y="10" width="300" height="34" rx="6"/>' + text(x + 150, 32, title, "h"))
        out.append(f'<rect class="b" x="{x}" y="50" width="300" height="92" rx="6"/>')
        for i, l in enumerate(lines):
            out.append(text(x + 150, 72 + i * 19, l, "s" if i else ""))
    return svg(670, 152, "".join(out), "Passive footprinting compared with active footprinting")


@diagram("m02-choose")
def choose():
    n = {"q1": (170, 50, 260, 70, "Does the technique send\nanything to the target's\nown systems or people?", "d"),
         "p": (520, 50, 230, 50, "Passive\nsearch engines, archives, Whois", "t"),
         "q2": (170, 170, 260, 70, "Is it inside your signed\nscope and time window?", "d"),
         "a": (520, 170, 230, 50, "Active, allowed\nDNS queries, zone transfer, calls", "t"),
         "s": (170, 275, 260, 44, "Stop. Ask the client first.", "b")}
    e = [("q1", "p", "no", "h"), ("q1", "q2", "yes", "v"), ("q2", "a", "yes", "h"), ("q2", "s", "no", "v")]
    return flow(n, e, 650, 305, "Deciding whether a footprinting step is passive or active, and whether it is allowed")


@diagram("m02-funnel")
def funnel():
    return ladder([("1. A name", "All you start with: \"Kestrel Freight\"."),
                   ("2. Domains", "Search engines, company registers, Whois."),
                   ("3. Subdomains and hosts", "DNS records, zone transfers, certificate and archive data."),
                   ("4. Network ranges", "Regional registry records, traceroute."),
                   ("5. People and email addresses", "Staff pages, social networks, job adverts."),
                   ("6. Technology in use", "Banners, job adverts, document metadata."),
                   ("7. A footprint report", "The blueprint that scanning (Module 3) is aimed with.")],
                  "Footprinting narrows an organisation's name down to hosts, people and technology", rh=44)


@diagram("m02-webs")
def webs():
    out = []
    rows = [("Surface web", "Indexed by search engines. Any browser.", "t", 12, 646),
            ("Deep web", "Not indexed: behind logins, forms and databases. Mostly ordinary.", "b", 46, 578),
            ("Dark web", "Hidden services reached only with special software such as Tor Browser.", "d", 80, 510)]
    for i, (name, note, cls, x, w) in enumerate(rows):
        y = 10 + i * 58
        h = 176 - i * 58
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                   + text(x + 14, y + 22, name, "h", "start") + text(x + 14, y + 40, note, "s", "start"))
    return svg(670, 196, "".join(out), "Surface web, deep web and dark web as nested layers")


@diagram("m02-registries")
def registries():
    rows = [(0, "Who keeps which registration record?"),
            (1, "Names:  ICANN sets the rules for generic domains"),
            (2, "Registry: runs one top-level domain, such as .com or .org"),
            (3, "Registrar: sells the name; holds the customer's contact details"),
            (1, "Numbers:  IANA hands address blocks to five regional registries (RIRs)"),
            (2, "ARIN,  RIPE NCC,  APNIC,  LACNIC,  AFRINIC"),
            (3, "ISPs and organisations: hold the IP ranges and AS numbers")]
    return tree(rows, "Domain names and IP numbers are registered through two separate hierarchies", w=660)


@diagram("m02-axfr")
def axfr():
    left = ("Ordinary lookup", [(0, 1, "A record for portal?"), (1, 0, "10.77.0.20"),
                                (0, 1, "A record for erp-legacy?"), (1, 0, "NXDOMAIN: no such name")])
    right = ("Zone transfer left open", [(0, 1, "AXFR: send me the whole zone"), (1, 0, "Every record, hidden hosts included")])
    return pair(left, right, lanes=("You", "Name server"), label="An ordinary DNS lookup compared with a zone transfer")


@diagram("m02-traceroute")
def traceroute():
    m = [(0, 1, "Probe 1, TTL = 1"), (1, 0, "ICMP time exceeded: router 1 revealed"),
         (0, 2, "Probe 2, TTL = 2"), (2, 0, "ICMP time exceeded: router 2 revealed"),
         (0, 3, "Probe 3, TTL = 3"), (3, 0, "Final reply: the target is reached"),
         (0, 0, "Each router subtracts 1 from the TTL. At 0 it discards the packet and reports back.", "note")]
    return single(("You", "Router 1", "Router 2", "Target"), m, "How traceroute uses the TTL field to reveal each router on a path", gap=180)


@diagram("m02-mail")
def mail():
    return ladder([("Sender's device", "The oldest Received line, at the bottom, may show its IP address."),
                   ("Sender's mail server", "Adds a Received line and the authentication results."),
                   ("Relays in between", "Each one adds another Received line on top."),
                   ("Recipient's mail server", "The newest Received line is at the top."),
                   ("Recipient's mailbox", "Read the header from the bottom up to follow the journey.")],
                  "Each mail server on the way adds a Received line to the top of the email header", w=690, bw=200)

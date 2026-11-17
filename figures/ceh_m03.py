"""Diagrams for CEH Module 3, Scanning Networks. All original."""
from diagrams import diagram, flow, pair, single, tree, bar, svg, text


@diagram("m03-method")
def method():
    n = {"s": (110, 40, 180, 44, "Scope and rules\nof engagement", "t"),
         "h": (110, 130, 180, 44, "1. Host discovery\nWho is alive?", "b"),
         "p": (110, 220, 180, 44, "2. Port scan\nWhich doors are open?", "b"),
         "v": (110, 310, 180, 44, "3. Service and version\nWhat is behind each door?", "b"),
         "o": (110, 400, 180, 44, "4. OS discovery\nWhat is the host?", "b"),
         "n": (110, 490, 180, 44, "Next: enumeration and\nvulnerability analysis", "t"),
         "f": (400, 220, 190, 70, "Many ports\nfiltered or no\nreplies?", "d"),
         "e": (400, 355, 190, 56, "Adjust: evasion and\ntiming techniques,\nthen rescan", "b"),
         "l": (640, 130, 150, 56, "Log every command\nand save output\n(-oA)", "b")}
    e = [("s", "h", "", "v"), ("h", "p", "", "v"), ("p", "v", "", "v"), ("v", "o", "", "v"), ("o", "n", "", "v"),
         ("p", "f", "", "h"), ("f", "e", "yes", "v"), ("e", "p", "", "M305 355H250V242"),
         ("h", "l", "at every step", "h")]
    return flow(n, e, 730, 525, "Scanning workflow")


@diagram("m03-ranges")
def ranges():
    return bar([(3, "0 to 1023", "Well-known", "t"), (5, "1024 to 49151", "Registered", "b"),
                (4, "49152 to 65535", "Dynamic / private", "d")],
               "The three port ranges", note="Widths are not to scale. TCP and UDP each have their own set of 65,536 ports.")


@diagram("m03-tcpheader")
def tcpheader():
    rows = [[("Source port", 16), ("Destination port", 16)], [("Sequence number", 32)], [("Acknowledgement number", 32)],
            [("Offset", 4), ("Rsvd", 4), ("C", 1), ("E", 1), ("U", 1), ("A", 1), ("P", 1), ("R", 1), ("S", 1), ("F", 1), ("Window size", 16)],
            [("Checksum", 16), ("Urgent pointer", 16)], [("Options (if any) and padding", 32)]]
    u, x0, y, out = 20, 20, 40, []
    for b in (0, 4, 8, 16, 24, 31):
        out.append(text(x0 + b * u + (u / 2 if b in (0, 31) else 0), 28, f"bit {b}", "s"))
    for r in rows:
        x = x0
        for name, bits in r:
            cls = "t" if bits == 1 else "b"
            out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{bits*u}" height="34"/>' + text(x + bits * u / 2, y + 22, name, "h" if bits == 1 else ""))
            x += bits * u
        y += 34
    out.append(text(x0 + 16 * u, y + 22, "Flag bits, left to right: CWR, ECE, then the classic six URG, ACK, PSH, RST, SYN, FIN", "s"))
    return svg(680, y + 34, "".join(out), "TCP header layout")


@diagram("m03-handshake")
def handshake():
    m = [(0, 1, "1. SYN  seq=x"), (1, 0, "2. SYN/ACK  seq=y, ack=x+1"), (0, 1, "3. ACK  ack=y+1"),
         (0, 0, "Connection established: data flows both ways", "note"),
         (0, 1, "PSH/ACK  data"), (1, 0, "ACK"),
         (0, 0, "Orderly close: each side sends FIN and gets an ACK", "note"),
         (0, 1, "FIN/ACK"), (1, 0, "ACK"), (1, 0, "FIN/ACK"), (0, 1, "ACK")]
    return single(("Client", "Server"), m, "TCP three-way handshake, data transfer and close", gap=300)


@diagram("m03-states")
def states():
    n = {"p": (330, 36, 200, 40, "SYN probe sent to a port", "t"),
         "q": (330, 130, 220, 70, "What came back?", "d"),
         "o": (90, 250, 150, 50, "SYN/ACK\nopen", "b"), "c": (250, 250, 150, 50, "RST\nclosed", "b"),
         "f": (410, 250, 150, 50, "Nothing after retries\nfiltered", "b"), "i": (575, 250, 160, 50, "ICMP unreachable\nfiltered", "b")}
    e = [("p", "q", "", "v"), ("q", "o", "", "hv"), ("q", "c", "", "M300 158L258 225"),
         ("q", "f", "", "M360 158L402 225"), ("q", "i", "", "hv")]
    return flow(n, e, 670, 290, "Reading the reply to a SYN probe")


@diagram("m03-discover")
def discover():
    n = {"q1": (150, 50, 230, 70, "Target on your own\nnetwork segment?", "d"),
         "a1": (480, 50, 210, 44, "ARP ping:  nmap -sn -PR", "t"),
         "q2": (150, 160, 230, 70, "Does ICMP echo\nget replies?", "d"),
         "a2": (480, 160, 210, 44, "ICMP sweep:  nmap -sn -PE", "t"),
         "q3": (150, 270, 230, 70, "Other ICMP types\nor TCP probes\nanswered?", "d"),
         "a3": (480, 270, 210, 56, "nmap -sn -PP -PM\n-PS22,80,443 -PA80", "t"),
         "q4": (150, 380, 230, 70, "UDP or other\nIP protocols\nanswered?", "d"),
         "a4": (480, 380, 210, 44, "nmap -sn -PU53,161 -PO", "t"),
         "a5": (150, 480, 230, 44, "Skip discovery:  nmap -Pn", "t")}
    e = [("q1", "a1", "yes", "h"), ("q1", "q2", "no", "v"), ("q2", "a2", "yes", "h"), ("q2", "q3", "no", "v"),
         ("q3", "a3", "yes", "h"), ("q3", "q4", "no", "v"), ("q4", "a4", "yes", "h"), ("q4", "a5", "no", "v")]
    return flow(n, e, 610, 515, "Choosing a host discovery method")


@diagram("m03-family")
def family():
    rows = [(0, "Port scanning techniques"),
            (1, "TCP scanning"),
            (2, "Open:  TCP connect / full-open  (-sT)"),
            (2, "Stealth"),
            (3, "Half-open / SYN  (-sS)"),
            (3, "Inverse TCP flag:  FIN (-sF),  NULL (-sN),  Xmas (-sX),  Maimon (-sM)"),
            (3, "ACK flag probe (-sA):  TTL-based,  Window-based (-sW)"),
            (2, "Third-party and spoofed:  IDLE / IP ID header  (-sI)"),
            (1, "UDP scanning  (-sU)"),
            (1, "SCTP scanning:  INIT (-sY),  COOKIE ECHO (-sZ)"),
            (1, "SSDP scanning  and  list scan (-sL)"),
            (1, "IPv6 scanning  (-6)")]
    return tree(rows, "Family tree of port scanning techniques", w=660)


@diagram("m03-choose")
def choose():
    n = {"q1": (150, 50, 230, 70, "Root or admin\nrights on the\nscanning host?", "d"),
         "a1": (480, 50, 220, 44, "TCP connect:  -sT", "t"),
         "q2": (150, 160, 230, 70, "Goal is to map\nfirewall rules?", "d"),
         "a2": (480, 160, 220, 44, "ACK or Window:  -sA, -sW", "t"),
         "q3": (150, 270, 230, 70, "Looking for UDP\nor SCTP services?", "d"),
         "a3": (480, 270, 220, 44, "-sU,  -sY,  -sZ", "t"),
         "q4": (150, 380, 230, 70, "Must hide your\nown address?", "d"),
         "a4": (480, 380, 220, 44, "Idle scan:  -sI zombie", "t"),
         "q5": (150, 490, 230, 70, "Stateless filter\nand a non-Windows\ntarget?", "d"),
         "a5": (480, 490, 220, 44, "FIN, Xmas, NULL, Maimon", "t"),
         "a6": (150, 590, 230, 44, "Default choice: SYN scan  -sS", "t")}
    e = [("q1", "a1", "no", "h"), ("q1", "q2", "yes", "v"), ("q2", "a2", "yes", "h"), ("q2", "q3", "no", "v"),
         ("q3", "a3", "yes", "h"), ("q3", "q4", "no", "v"), ("q4", "a4", "yes", "h"), ("q4", "q5", "no", "v"),
         ("q5", "a5", "yes", "h"), ("q5", "a6", "no", "v")]
    return flow(n, e, 620, 625, "Choosing a port scan type")


P = {
    "connect": (("Port open", [(0, 1, "SYN"), (1, 0, "SYN/ACK"), (0, 1, "ACK"), (0, 1, "RST (scanner hangs up)")]),
                ("Port closed", [(0, 1, "SYN"), (1, 0, "RST/ACK")])),
    "syn": (("Port open", [(0, 1, "SYN"), (1, 0, "SYN/ACK"), (0, 1, "RST (never completes)")]),
            ("Port closed", [(0, 1, "SYN"), (1, 0, "RST/ACK")])),
    "inverse": (("Port open", [(0, 1, "FIN, or FIN+PSH+URG, or no flags"), (1, 0, "no reply", "x")]),
                ("Port closed", [(0, 1, "FIN, or FIN+PSH+URG, or no flags"), (1, 0, "RST/ACK")])),
    "ack": (("No firewall in the way", [(0, 1, "ACK"), (1, 0, "RST  (port is unfiltered)")]),
            ("Stateful firewall", [(0, 1, "ACK", "x"), (0, 0, "No reply, or ICMP unreachable: filtered", "note")])),
    "udp": (("Port open", [(0, 1, "UDP datagram"), (1, 0, "UDP reply, or often nothing", "x")]),
            ("Port closed", [(0, 1, "UDP datagram"), (1, 0, "ICMP type 3 code 3 (port unreachable)")])),
    "sctp": (("Port open", [(0, 1, "INIT chunk"), (1, 0, "INIT-ACK")]),
             ("Port closed", [(0, 1, "INIT chunk"), (1, 0, "ABORT")])),
}
for _k, _v in P.items():
    diagram("m03-" + _k)(lambda v=_v, k=_k: pair(v[0], v[1], label=k + " scan: open versus closed port"))


def _idle(open_):
    L = ("Scanner", "Zombie", "Target")
    if open_:
        m = [(0, 1, "1. SYN/ACK probe"), (1, 0, "RST, IP ID = 1000"),
             (0, 2, "2. SYN, source address forged as Zombie"), (2, 1, "3. SYN/ACK (port is open)"),
             (1, 2, "RST, IP ID = 1001"), (0, 1, "4. SYN/ACK probe"), (1, 0, "RST, IP ID = 1002: rose by 2, so OPEN")]
    else:
        m = [(0, 1, "1. SYN/ACK probe"), (1, 0, "RST, IP ID = 1000"),
             (0, 2, "2. SYN, source address forged as Zombie"), (2, 1, "3. RST (port is closed)"),
             (0, 0, "Zombie ignores an unexpected RST: IP ID unchanged", "note"),
             (0, 1, "4. SYN/ACK probe"), (1, 0, "RST, IP ID = 1001: rose by 1, so CLOSED")]
    return single(L, m, "Idle scan, " + ("open port" if open_ else "closed port"))


diagram("m03-idle-open")(lambda: _idle(True))
diagram("m03-idle-closed")(lambda: _idle(False))


@diagram("m03-fragment")
def fragment():
    return bar([(2, "IP header", "fragment 1", "b"), (2, "TCP bytes 0-7", "ports + sequence", "t"),
                (2, "IP header", "fragment 2", "b"), (2, "TCP bytes 8-15", "ack no. + FLAGS", "d"),
                (2, "IP header", "fragment 3", "b"), (2, "TCP bytes 16-19", "checksum, urgent", "t")],
               "A 20-byte TCP header split across three 8-byte fragments", w=680,
               note="The ports travel in fragment 1 and the flags in fragment 2.")


@diagram("m03-spoofdetect")
def spoofdetect():
    m = [(0, 2, "Packet claiming to come from Host A"), (2, 1, "Probe sent to the real Host A"),
         (1, 2, "Reply shows A's real TTL and IP ID"),
         (0, 0, "Values do not match the suspect packet: the source was forged", "note")]
    return single(("Attacker", "Real Host A", "Defender"), m,
                  "Detecting a spoofed source address by probing the claimed sender")

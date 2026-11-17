---
title: Module 3 - Scanning Networks
book: Ethical Hacking Study Handbook
module: 3
kicker: Ethical hacking track · Module 3 of 20
home: index.html
lab: 90
difficulty: Beginner to intermediate
status: Review draft
verified: 17 Nov 2026: CEH v13 courseware Module 03, RFC 9293, Nmap reference guide
footer: Unofficial, independent study material. Not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Written in our own words from public protocol standards and tool documentation. Use these techniques only on systems you own or are authorised in writing to test.
---

# Scanning Networks

[[meta]]

## What this chapter is about

Scanning is how you find out what is actually there on a network. You start with a list of addresses. You finish with a map: which machines are switched on, which services each one offers, what software provides them, and what operating system sits underneath.

!!! story "An everyday picture"
    Imagine walking down a street at night with a notebook. First you note which buildings have lights on (**host discovery**). Then you try every door and window of the lit ones to see which open (**port scanning**). You read the nameplate beside each open door (**service and version detection**). Last, you look at the brickwork to guess who built the place (**OS discovery**). You have not gone inside. You have only looked, knocked and written things down. That is scanning.

Everything later in an attack, or in a penetration test, is aimed using this map. Defenders use the very same techniques to find out what they are exposing before someone else does.

!!! before "Before you start"
    This chapter assumes six ideas. If one is new, the one-line version here is enough to carry on.

    - **IP address.** The number that identifies a machine on a network, such as `10.77.0.20`. `10.77.0.0/24` means the 256 addresses from `10.77.0.0` to `10.77.0.255`.
    - **Packet.** A small envelope of data with a "from" address and a "to" address. Everything on a network travels as packets.
    - **Port.** A number from 0 to 65535 that says which program on the machine a packet is for. Section 1 teaches this.
    - **Client and server.** The client starts the conversation; the server waits for it. A web browser is a client. A website is a server.
    - **Firewall.** A device or program that decides which packets may pass. Module 12 covers firewalls in depth.
    - **Root or administrator.** The all-powerful account on a computer. Some scans need it because they build packets by hand.

    You do not need to have read Modules 1 and 2. Where this chapter leans on them, it says so.

!!! why "Why this matters to you"
    - **Exam candidate.** This is one of the most heavily tested modules. Questions give you a flag combination, a reply or an Nmap switch and ask what it means. The practical exams (CEH Practical, CPENT) start every task with a scan.
    - **Defending a network.** You cannot protect a service you do not know is running. Scanning your own network is how you find the forgotten test server before an attacker does. Section 9 is written for you.
    - **Working with sensitive data.** If you work in a hospital, a bank or a school, your organisation is scanned from the internet every day. This chapter shows what those scans can see, and why "nobody knows that system exists" is not a defence.

### How the tags work

Every section, table and key fact carries one of four tags. They tell you how to study it.

[[legend]]

Facts tagged MEMORISE are collected automatically into the [cheat sheet](#exam-cheat-sheet) at the end.

**How to use this chapter.** Read sections 1 to 4 in order; each builds on the last. Run every "Try it" box in lab L01 as you reach it. Tick "Mark done" on each heading. Finish with the lab walk-through and the quiz.

| After this chapter you can | Section |
| --- | --- |
| Name the TCP flags and predict the reply to any probe | 1 |
| Recognise the scanning tools and read an hping3 command | 2 |
| Find live hosts even when ping is blocked | 3 |
| Choose a port scan for a situation and read its result | 4, 5 |
| Identify services, versions and operating systems | 6, 7 |
| Explain how scans evade detection and how defenders respond | 8, 9 |
| Use an AI assistant to draft scan commands safely | 10 |

## 1. Scanning concepts {U}

### Three kinds of scanning {M: Three kinds of scanning: port scanning lists open ports and services; network scanning lists live hosts; vulnerability scanning lists known weaknesses}

Footprinting (Module 2) collected information *about* a target, mostly without touching it. Scanning is where you send packets *to* the target and study what comes back. It is active and it leaves traces. Without permission it is illegal in most countries.

| Kind of scan | What it lists | Typical tool |
| --- | --- | --- |
| Port scanning | Open ports and the services on them | Nmap, hping3 |
| Network scanning | Live hosts and their IP addresses | Nmap `-sn`, Angry IP Scanner |
| Vulnerability scanning | Known weaknesses in those hosts | Nessus, OpenVAS (Module 5) |

### What scanning is for {U}

The objectives, in the order you usually reach them:

1. Live hosts, their IP addresses and open ports.
2. The operating system and system architecture. Finding this is called **fingerprinting**.
3. The services listening on each host, and their exact versions.
4. Vulnerabilities in any of those systems.
5. The layout of the network: routers, switches, firewalls and how they connect.

```diagram m03-method
The scanning workflow. Each step narrows the target list for the next. When a firewall hides the answers, you loop through the evasion techniques in section 8.
```

### Ports {M: Port ranges: 0-1023 well-known; 1024-49151 registered; 49152-65535 dynamic or private}

An IP address gets a packet to the right machine. A **port** number gets it to the right program on that machine. Think of the IP address as a building's street address and the port as the flat number.

```diagram m03-ranges
The three port ranges. Memorise the boundaries.
```

| Range | Name | Used for |
| --- | --- | --- |
| 0 to 1023 | Well-known ports | Standard services such as web, mail and DNS |
| 1024 to 49151 | Registered ports | Assigned to particular products |
| 49152 to 65535 | Dynamic or private ports | Temporary ports chosen by clients |

Nothing forces a service to use its usual port. A web server can listen on 8081. A forgotten system can hide on 48620. That is why a default scan, which checks only the 1,000 most common ports, misses things.

**The must-know ports.** The official courseware prints a table of about a hundred. These are the ones worth knowing by heart.

| Port | Service {M} | Port | Service |
| --- | --- | --- | --- |
| 20, 21 TCP | FTP data, FTP control | 137, 138, 139 | NetBIOS name, datagram, session |
| 22 TCP | SSH | 143 TCP | IMAP |
| 23 TCP | Telnet | 161, 162 UDP | SNMP, SNMP trap |
| 25 TCP | SMTP (mail) | 389 | LDAP |
| 53 TCP and UDP | DNS | 443 TCP | HTTPS |
| 67, 68 UDP | DHCP server, client | 445 TCP | SMB (Microsoft-DS) |
| 69 UDP | TFTP | 500 UDP | ISAKMP / IKE (VPN) |
| 80 TCP | HTTP | 514 UDP | Syslog |
| 88 | Kerberos | 1433, 1434 | Microsoft SQL Server, monitor |
| 110 TCP | POP3 | 2049 | NFS |
| 111 | RPC portmapper | 3306 TCP | MySQL |
| 123 UDP | NTP | 3389 TCP | Remote Desktop (RDP) |
| 135 TCP | Microsoft RPC | 5060, 5061 | SIP (voice calls) |

!!! remember "Remember"
    Three mail ports in rising order of age of the idea: **25** sends (SMTP), **110** collects (POP3), **143** syncs (IMAP). The NetBIOS trio is consecutive: **137, 138, 139**, then SMB at **445**.

### TCP and its flags {M: Six TCP flags (exam: 1 bit each, 6 bits): SYN opens, ACK acknowledges, FIN closes politely, RST aborts, PSH delivers now, URG goes first. SYN, ACK, FIN, RST manage the connection; PSH and URG instruct about data}

**TCP** is the reliable transport protocol. It sets up a connection, numbers every byte and confirms delivery. Each TCP segment starts with a header.

```diagram m03-tcpheader
The TCP header. The single-bit flags in the fourth row control the life of a connection. Scan types differ mainly in which flags they set.
```

A **flag** is one bit that is either on (1) or off (0).

| Flag | Name | What it tells the receiver | Everyday analogy |
| --- | --- | --- | --- |
| SYN | Synchronise | "I want to open a connection; here is my starting sequence number" | Dialling a number |
| ACK | Acknowledge | "I received everything up to this byte" | "Yes, I hear you" |
| FIN | Finish | "I have no more data; let us close politely" | "Goodbye" |
| RST | Reset | "Stop. This connection does not exist or must end now" | Slamming the phone down |
| PSH | Push | "Hand this data to the application now, do not buffer it" | "Read this immediately" |
| URG | Urgent | "Process this data ahead of everything else" | Jumping the queue |

SYN, ACK, FIN and RST manage the connection itself. PSH and URG give instructions about the data.

!!! exam "Exam answer / In practice"
    **Exam answer:** TCP has **six** flags, each 1 bit, so the flags field is **6 bits**.

    **In practice:** the current TCP standard defines **eight** control bits. CWR and ECE were added in 2001 for congestion signalling. No classic scan type uses them, which is why the courseware still counts six. Answer six in the exam.

!!! update "Updated: August 2022"
    **What changed.** RFC 793, the 1981 TCP specification the courseware cites throughout, was replaced by **RFC 9293** in **August 2022**. The behaviour scans rely on (how open and closed ports answer stray segments) is the same in both.

    **The exam still expects:** "RFC 793". When a question says a scan works only on "RFC 793-compliant" systems, that wording is the answer.

!!! remember "Remember"
    The six flags in header order: **U**nskilled **A**ttackers **P**ester **R**eal **S**ecurity **F**olk: URG, ACK, PSH, RST, SYN, FIN.

### The three-way handshake {M: Handshake: SYN, SYN/ACK, ACK. Close: FIN then ACK from each side, or a single RST}

Every TCP connection opens with the same three segments: **SYN**, then **SYN/ACK**, then **ACK**.

```diagram m03-handshake
A full TCP conversation: three-way handshake, data, and an orderly close.
```

A connection ends in one of two ways. The polite way is a **FIN** from one side, an ACK back, then a FIN from the other side. The abrupt way is a single **RST**.

### Five rules that explain every scan {U}

These follow from the TCP standard. If you understand them, you can work out the big table in section 4 instead of memorising it.

1. A **SYN** to an **open** port is answered with **SYN/ACK**.
2. A **SYN** to a **closed** port is answered with **RST** (strictly, RST/ACK).
3. Any other stray segment arriving at a **closed** port is answered with **RST**.
4. A stray segment with no SYN, RST or ACK that arrives at an **open** port is silently **dropped**.
5. A stray **ACK** is answered with **RST**, whether the port is open or closed.

Rules 1 and 2 power the connect and SYN scans. Rules 3 and 4 power the FIN, Xmas and NULL scans. Rule 5 powers the ACK scan.

### UDP and ICMP {M: ICMP types: echo 8/0; timestamp 13/14; address mask 17/18. Type 3 code 3 = port unreachable (closed UDP port). Type 3 codes 1, 2, 3, 9, 10, 13 = filtered. A ping is 64 bytes: 56 data + 8 header}

**UDP** is the other main transport protocol. It has no handshake, no flags and no acknowledgements. A program either answers a UDP datagram or it does not. That makes UDP scanning slow and ambiguous.

**ICMP** is the network's error and diagnostics channel. Ping uses it. It has message *types*, not ports.

| ICMP type | Message | Why a scanner cares |
| --- | --- | --- |
| 8 and 0 | Echo request and echo reply | Ordinary ping |
| 13 and 14 | Timestamp request and reply | A ping that works when echo is blocked |
| 17 and 18 | Address mask request and reply | Another alternative ping |
| 3, code 3 | Destination unreachable: port unreachable | A closed UDP port |
| 3, codes 1, 2, 3, 9, 10, 13 | Other "unreachable" errors | A filter is blocking the probe |
| 11 | Time exceeded | Used by traceroute |

A standard ping packet carries **64 bytes**: 56 bytes of data plus an 8-byte ICMP header.

!!! exam "Exam answer / In practice"
    **Exam answer:** the "filtered" ICMP error list is **type 3, codes 1, 2, 3, 9, 10 or 13**.

    **In practice:** Nmap's documentation also includes code 0 (network unreachable). For a UDP scan, code 3 is not in the filtered list, because there it means "closed".

### The six port states {M: Six Nmap port states: open; closed; filtered; unfiltered (ACK scan got RST); open|filtered (no reply to UDP, FIN, NULL, Xmas, Maimon); closed|filtered (idle scan only)}

Nmap reports one of six states for every port.

| State | Meaning | Typical cause |
| --- | --- | --- |
| open | A program accepted the probe | A service is listening |
| closed | The host answered, but nothing is listening | RST received |
| filtered | No usable answer; something is dropping probes | Firewall: silence or an ICMP error |
| unfiltered | The port is reachable, but open or closed is unknown | ACK scan got a RST |
| open\|filtered | Cannot tell open from filtered | No reply to a UDP, FIN, Xmas, NULL or Maimon probe |
| closed\|filtered | Cannot tell closed from filtered | Seen only in the idle scan |

```diagram m03-states
How a SYN scan decides a port's state from the reply.
```

!!! try "Try it"
    In lab L01, from the attacker container, watch the handshake rules happen. `--reason` prints why Nmap chose each state.

    ```bash
    nmap -sS -p 80,81 --reason 10.77.0.20
    ```

    Port 80 should show `syn-ack` (rule 1) and port 81 `reset` (rule 2).

!!! recap "Recap: section 1"
    - Three kinds of scan: port (open ports), network (live hosts), vulnerability (known weaknesses).
    - Port ranges: 0-1023 well-known, 1024-49151 registered, 49152-65535 dynamic.
    - Six flags for the exam: SYN, ACK, FIN, RST, PSH, URG. Handshake: SYN, SYN/ACK, ACK.
    - Open ports answer SYN with SYN/ACK; closed ports answer with RST; open ports ignore flag-less strays.
    - Six port states: open, closed, filtered, unfiltered, open|filtered, closed|filtered.

## 2. The scanning toolbox {R}

You need to recognise these names and know what each is for. Only Nmap and hping3 need command-level knowledge.

| Tool | What it is |
| --- | --- |
| **Nmap** {R} | The standard scanner: host discovery, every scan type, version and OS detection, and a scripting engine (NSE). **Zenmap** is its graphical front end; the courseware's screenshots use it |
| **hping3** {R} | Command-line packet crafter. Builds one packet at a time with any flags, spoofed sources or fragments. Used for firewall testing, idle scans and denial-of-service demonstrations |
| **Metasploit** {R} | Exploitation framework. Its auxiliary modules include port scanners, for example `auxiliary/scanner/portscan/tcp` |
| **NetScanTools Pro** {R} | Windows investigation toolkit: lists addresses, hostnames and ports, and crafts packets |
| sx, RustScan, MegaPing, SolarWinds Engineer's Toolset, PRTG Network Monitor {R} | Additional scanners named in the courseware |
| masscan, Unicornscan, arp-scan, netdiscover | Not in the official tool list but common in practice: very fast scanning, TTL display, local ARP discovery |

Nmap's basic shape is always the same: `nmap [options] [target]`.

!!! update "Updated: March 2026"
    **What changed.** The courseware's screenshots show older Nmap builds in the Zenmap window, and its text still uses retired switches such as `-sP`, `-P0` and the old ICMP options `-P`, `-L` and `-T`. The newest release listed in Nmap's own changelog is **7.99**, **March 2026**. Current builds use `-sn` and `-Pn`; the scan types and their results are unchanged.

    **The exam still expects:** you to recognise the old switches as well as the new. `-sP` means the same as `-sn`; `-P0` and `-PN` mean the same as `-Pn`.

### hping3 commands {M: hping3 modes: -1 ICMP, -2 UDP, -8 scan, -9 listen. Flags: -S -A -F -P -U -R. `-a` spoofs the source; `-Q` collects sequence numbers; `--flood` floods}

hping3 sends TCP by default. A number switch changes the mode; a capital letter sets a flag.

| Command | What it does |
| --- | --- |
| `hping3 -1 10.0.0.25` | ICMP ping (`-1` or `--icmp`) |
| `hping3 -A 10.0.0.25 -p 80` | ACK scan on port 80: tests for a firewall |
| `hping3 -2 10.0.0.25 -p 80` | UDP mode (`-2` or `--udp`) |
| `hping3 -8 50-60 -S 10.0.0.25 -V` | Scan mode (`-8` or `--scan`): SYN scan of ports 50 to 60 |
| `hping3 -F -P -U 10.0.0.25 -p 80` | FIN, PSH and URG set: an Xmas probe |
| `hping3 -1 10.0.1.x --rand-dest -I eth0` | Ping sweep of a whole subnet in random order |
| `hping3 192.168.1.103 -Q -p 139` | Collect the target's TCP sequence numbers (`-Q`) |
| `hping3 -S 72.14.207.99 -p 80 --tcp-timestamp` | Read the TCP timestamp to guess uptime |
| `hping3 -9 HTTP -I eth0` | Listen mode (`-9`): capture packets containing "HTTP" |
| `hping3 -S 192.168.1.1 -a 192.168.1.254 -p 22 --flood` | SYN flood with a spoofed source (`-a`): a DoS attack |

!!! remember "Remember"
    hping3 number modes: **-1** ICMP, **-2** UDP, **-8** scan, **-9** listen. "One ping, two UDP, eight scans, nine listens." Capital letters are the flags themselves: `-S -A -F -P -U -R`.

!!! exam "Exam answer / In practice"
    **Exam answer:** an hping3 ACK probe (`-A`) that gets a **RST** back means the host is alive and the port is not filtered. An Xmas probe (`-F -P -U`) gets **no reply from an open port** and **RST from a closed port**.

    **In practice:** the RST to an ACK probe says nothing about whether the port is open (rule 5). And a ping sweep finds live *hosts*; ICMP has no ports, whatever a carelessly worded option says.

!!! try "Try it"
    hping3 is not installed in the L01 attacker container, so do the same Xmas probe with Nmap and watch the packets:

    ```bash
    nmap -sX -p 80 --packet-trace 10.77.0.20
    ```

!!! recap "Recap: section 2"
    - Nmap is the standard; Zenmap is its GUI. Syntax: `nmap [options] [target]`.
    - hping3 crafts single packets. Modes: -1 ICMP, -2 UDP, -8 scan, -9 listen.
    - hping3 flags are capital letters: -S, -A, -F, -P, -U. `-a` spoofs the source, `--flood` floods.
    - Metasploit and NetScanTools Pro also scan; recognise sx, RustScan, MegaPing, PRTG, SolarWinds.
    - An ACK probe answered by RST means "reachable, not filtered", not "open".

## 3. Host discovery {U}

Scanning 65,536 ports on an address nobody is using wastes hours. **Host discovery** finds the live addresses first. A sweep across a whole range is called a **ping sweep**.

The difficulty is that the classic ping is blocked on most modern networks. So you need several ways to make a host reveal itself.

!!! story "The idea"
    A teacher taking the register calls each name. A pupil who shouts "here" is present. So is a pupil who shouts "leave me alone". Only silence is ambiguous. In host discovery, **any reply at all, even a refusal, proves a machine is there.**

### The techniques {M: Host discovery: ARP `-PR` (local segment only); UDP `-PU`; ICMP echo `-PE` (8/0), timestamp `-PP` (13/14), address mask `-PM` (17/18); TCP SYN `-PS`; TCP ACK `-PA`; IP protocol `-PO`. Any reply, even RST, means the host is up}

| Technique | Nmap option | Probe sent | A live host replies with |
| --- | --- | --- | --- |
| ARP ping | `-PR` | ARP request: "who has this IP?" | ARP reply with its MAC address |
| UDP ping | `-PU` | UDP datagram to port **40125** by default | ICMP port unreachable |
| ICMP echo ping | `-PE` | ICMP type 8 | ICMP type 0 |
| ICMP echo ping sweep | `-sn -PE` with a range | Type 8 to every address | Type 0 from each live host |
| ICMP timestamp ping | `-PP` | ICMP type 13 | ICMP type 14 |
| ICMP address mask ping | `-PM` | ICMP type 17 | ICMP type 18 |
| TCP SYN ping | `-PS` | SYN to port **80** by default | SYN/ACK or RST |
| TCP ACK ping | `-PA` | ACK to port **80** by default | RST |
| IP protocol ping | `-PO` | Bare packets for protocols **1** (ICMP), **2** (IGMP) and **4** (IP-in-IP) | Any reply |

What each is good for:

- **ARP ping** works only on your own network segment, because ARP does not cross routers. There it is the most accurate method, and a host firewall cannot hide from it. Nmap uses it automatically on a local network; `--disable-arp-ping` turns that off.
- **UDP ping** finds hosts behind firewalls that filter TCP strictly and forgot UDP.
- **Timestamp and address-mask pings** work when an administrator blocked echo requests and nothing else.
- **TCP SYN ping** gets through firewalls that allow web traffic. Port lists go straight after the switch with no space: `-PS22,80,443`.
- **TCP ACK ping** gets past simple filters that block only SYN.

When you give no discovery options, a privileged Nmap sends four probes at once to a remote network: ICMP echo, SYN to 443, ACK to 80 and ICMP timestamp. {U}

```diagram m03-discover
Picking a discovery method. Start with the cheapest, most reliable probe and fall back only when it fails.
```

### Commands {M: `-sn` = no port scan (old `-sP`). `-Pn` = no ping (old `-P0`, `-PN`). `-sL` = list targets only. Defaults: `-PS` and `-PA` port 80; `-PU` port 40125; `-PO` protocols 1, 2, 4}

```bash
nmap -sn 10.77.0.0/24                      # discovery only, no port scan
nmap -sn -PR 192.168.1.0/24                # ARP on the local segment
nmap -sn -PE -PP -PM 10.77.0.0/24          # all three ICMP types
nmap -sn -PS22,80,443 -PA80 10.77.0.0/24   # TCP pings
nmap -sn -PU53,161 10.77.0.0/24            # UDP ping
nmap -Pn -p 80,443 10.77.0.20              # skip discovery, assume the host is up
```

`-Pn` matters more than it looks. If a host ignores every discovery probe, Nmap marks it down and never scans its ports. `-Pn` treats every address as alive, at the cost of time.

!!! exam "Exam answer / In practice"
    **Exam answer:** `-sn` disables the **port scan** (older name `-sP`). `-Pn` disables the **ping** (older names `-P0`, `-PN`).

    **Exam answer:** for a UDP ping, "a response means the host is active; errors such as host or network unreachable, or TTL exceeded, mean it is offline or unreachable."

    **In practice:** the usual "response" to a UDP ping is an ICMP port unreachable, because port 40125 is almost never open. The courseware's AI-generated script still uses `-sP`; current Nmap accepts it, but write `-sn`.

!!! remember "Remember"
    Read the letters. **-sn** = **s**can: **n**o. **-Pn** = **P**ing: **n**o. And the ICMP trio pairs up with its numbers: **E**cho 8/0, **P** timestamp 13/14, **M**ask 17/18.

!!! trap "Exam traps"
    - `-sn` does not mean "no ping". It means discovery only.
    - ARP ping cannot discover hosts on another subnet.
    - A RST in reply to a TCP ping means the host is **up**. The port is closed, but that is not the question.
    - Pinging a broadcast address to sweep a subnet is unreliable. The courseware notes Windows hosts do not answer it; in practice almost nothing modern does.

### Ping sweep tools {R}

Recognise the names: **Angry IP Scanner** (the featured one: multi-threaded, pings each address, then optionally resolves the hostname and MAC and scans ports), SolarWinds Engineer's Toolset, NetScanTools Pro, Colasoft Ping Tool, Advanced IP Scanner and OpUtils. They differ in interface, not technique.

!!! cpent "CPENT depth: discovery on a real engagement"
    - **Large ranges.** Sweep first with `nmap -sn --min-rate` or masscan, write live hosts to a file, and feed it to detailed scans with `-iL`.
    - **Through a pivot.** ARP and ICMP usually cannot pass a SOCKS proxy. Discovery becomes a TCP connect sweep (`-sT -Pn`) of a few common ports through proxychains, or a one-liner run on the pivot itself.
    - **Quiet discovery.** The pivot's ARP cache, routing table and DNS records reveal neighbours without sending a single probe.

!!! try "Try it"
    ```bash
    nmap -sn -oG - 10.77.0.0/24 | awk '/Up$/{print $2}' > live.txt
    ```

    This writes only the live IP addresses to `live.txt`. You should see five lab hosts plus your own.

!!! recap "Recap: section 3"
    - Discover hosts before scanning ports. Any reply, even a RST, means "up".
    - ARP (`-PR`) is the most accurate, but local segment only.
    - ICMP pings: `-PE` 8/0, `-PP` 13/14, `-PM` 17/18. TCP pings: `-PS` and `-PA`, default port 80.
    - `-PU` default port 40125. `-PO` default protocols 1, 2 and 4.
    - `-sn` = no port scan. `-Pn` = no ping.

## 4. TCP port scans {U}

This is the heart of the module. Each technique sends a slightly different probe and reads the reply using the five rules from section 1.

### The family tree {M: Scan families: open = TCP connect; stealth = half-open (SYN), inverse flag (FIN, NULL, Xmas, Maimon), ACK probe (TTL, window); third-party and spoofed = IDLE/IPID}

The exam asks which family a scan belongs to. Learn the three TCP groups.

```diagram m03-family
How the courseware classifies port scans. "Stealth" covers half-open, inverse-flag and ACK-probe scans.
```

- **Open TCP scanning**: TCP connect, also called full-open.
- **Stealth TCP scanning**: half-open (SYN); inverse TCP flag (FIN, NULL, Xmas, Maimon); ACK flag probe (TTL-based, window-based).
- **Third-party and spoofed TCP scanning**: IDLE / IP ID header scan.

```diagram m03-choose
Picking a scan type. In practice the SYN scan is the default and the others are tools for special situations.
```

### TCP connect scan (full-open) {U}

The scanner asks its own operating system to open a normal connection with the `connect()` call. If the three-way handshake completes, the port is open. The scanner then sends RST to hang up.

```diagram m03-connect
TCP connect scan. The handshake completes, so the target application sees and usually logs the connection.
```

- **Needs:** no special privileges. Nmap uses it when you are not root.
- **Cost:** the most reliable TCP scan, and the easiest to detect and log.
- **Command:** `nmap -sT 10.77.0.20`

### Stealth scan (half-open, SYN scan) {U}

The scanner crafts a raw SYN. On SYN/ACK it knows the port is open and sends **RST instead of the final ACK**, so the connection never completes.

```diagram m03-syn
SYN scan. The handshake is abandoned after the second step.
```

- **Needs:** root or administrator rights, to craft raw packets.
- **Command:** `nmap -sS 10.77.0.20`. This is Nmap's default when run as root.

!!! exam "Exam answer / In practice"
    **Exam answer:** the half-open scan is "stealthy": it avoids the logging that a completed connection triggers and helps bypass firewall rules.

    **In practice:** that was true of application logs in the 1990s. Every modern firewall and intrusion detection system spots a SYN scan. The name is historical.

### Inverse TCP flag scans: FIN, NULL and Xmas {M: Inverse scans (FIN, NULL, Xmas, Maimon): open = no reply, closed = RST. Work on RFC 793-compliant UNIX and BSD stacks, not Windows. Need root. Xmas = FIN + URG + PSH}

These send a segment that should never start a conversation. A closed port answers RST (rule 3). An open port stays silent (rule 4). You learn "open" from *silence*, which is why they are called **inverse** scans.

```diagram m03-inverse
FIN, NULL and Xmas scans. An open port says nothing; a closed port resets.
```

| Scan | Flags set | Nmap |
| --- | --- | --- |
| FIN | FIN only | `-sF` |
| NULL | none | `-sN` |
| Xmas | FIN, URG and PSH | `-sX` |

- **Result:** silence could also be a firewall, so Nmap reports `open|filtered`.
- **Advantage:** probes with no SYN can pass simple filters that only watch for SYN.
- **Disadvantages:** needs raw-socket (root) privileges, and does not work against Microsoft Windows.

!!! exam "Exam answer / In practice"
    **Exam answer:** inverse scans work only against systems that follow RFC 793, mainly UNIX and BSD-derived stacks. They are **not effective against Windows**.

    **In practice:** Windows answers RST from every port, open or closed, so Nmap shows every port as **closed**. One line of the courseware says such a scan shows all ports as open; if an option list forces a choice, the safe reading is "the scan cannot tell you anything about a Windows host". RFC 793 was replaced by RFC 9293 in 2022, with the same behaviour.

!!! remember "Remember"
    Xmas = **F**IN + **U**RG + **P**SH: "**F**airy lights **U**p, **P**lease". NULL = nothing lit. FIN = one bulb.

### TCP Maimon scan {U}

The probe is **FIN/ACK**. By the standard a RST should come back either way. Many BSD-derived systems instead drop the probe when the port is open. So: no reply means `open|filtered`, RST means closed, an ICMP unreachable error means filtered. Command: `nmap -sM`.

### ACK flag probe scan {M: ACK scan: RST = unfiltered (no stateful firewall); no reply = filtered. TTL-based: RST with TTL below 64 = open. Window-based (-sW): non-zero window = open}

An ACK probe does not find open ports in the normal way. Its main job answers a different question: *is a stateful firewall in the way?*

```diagram m03-ack
ACK scan. A reset proves the probe reached the host, so no stateful filter is in the way.
```

Any host that receives a stray ACK replies RST (rule 5). A **stateful** firewall, which remembers connections, knows this ACK belongs to nothing and drops it.

- **RST received:** the port is **not filtered**; no stateful firewall.
- **No reply:** the port is **filtered**; a stateful firewall is present.
- **Command:** `nmap -sA 10.77.0.20`

Two older variants read open or closed from the RST itself, on BSD-derived stacks:

| Variant | Look at | The port is open if |
| --- | --- | --- |
| TTL-based | TTL field of the RST | TTL is **less than 64** |
| Window-based (`-sW`) | Window field of the RST | Window is **non-zero** |

Use the window version when every RST carries the same TTL.

!!! exam "Exam answer / In practice"
    **Exam answer:** TTL below the boundary value 64 means open; a non-zero window means open. The courseware gives `nmap --ttl` as the TTL-based command and `-sW` for the window scan.

    **In practice:** both rely on quirks of old BSD stacks and are unreliable today; Nmap's own guide warns the window scan cannot always be trusted. In current Nmap `--ttl` only sets the TTL of the packets you *send*. There is no automatic TTL-based scan.

### IDLE / IPID header scan {M: Idle scan: probe the zombie with SYN/ACK, spoof a SYN to the target as the zombie, probe again. Zombie IP ID +2 = open, +1 = closed. Zombie must be idle with incremental, global IP IDs}

The idle scan finds open ports on a target **without sending it a single packet from your own address**. It bounces the scan off a third machine, the **zombie**.

It relies on one fact. Every IP packet carries an identification number, the **IP ID**. Some systems increase it by exactly one for each packet they send. If the zombie is otherwise idle, any jump in its IP ID was caused by you.

```diagram m03-idle-open
Idle scan when the target port is open. The zombie sends one extra packet, so its IP ID rises by 2 between your two probes.
```

```diagram m03-idle-closed
Idle scan when the target port is closed. The zombie sends nothing extra, so its IP ID rises by only 1.
```

The three steps:

1. Send **SYN/ACK** to the zombie. It replies RST, revealing its IP ID.
2. Send a **SYN** to the target with the **zombie's address as the source**.
3. Probe the zombie again and compare.

| IP ID change | Meaning |
| --- | --- |
| Increased by 2 | Port is **open** |
| Increased by 1 | Port is **closed** (Nmap says `closed|filtered`) |

- **Zombie requirements:** it must be idle, and it must assign IP IDs incrementally and globally.
- **What the target logs:** the zombie's address, not yours.
- **Command:** `nmap -Pn -sI zombie.example.lab target.example.lab`

!!! remember "Remember"
    Count the zombie's packets. Open port: the zombie sends **two** (one RST to the target, one to you), so **+2**. Closed port: only the **one** to you, so **+1**.

### The whole section on one screen {M}

| Scan | Nmap {M} | Probe | Open port replies | Closed port replies | Needs root |
| --- | --- | --- | --- | --- | --- |
| Connect | `-sT` | Full handshake | SYN/ACK | RST | No |
| SYN / half-open | `-sS` | SYN | SYN/ACK | RST | Yes |
| FIN | `-sF` | FIN | Nothing | RST | Yes |
| NULL | `-sN` | No flags | Nothing | RST | Yes |
| Xmas | `-sX` | FIN+URG+PSH | Nothing | RST | Yes |
| Maimon | `-sM` | FIN/ACK | Nothing (BSD) | RST | Yes |
| ACK | `-sA` | ACK | RST (unfiltered) | RST (unfiltered) | Yes |
| Window | `-sW` | ACK | RST, window > 0 | RST, window = 0 | Yes |
| Idle | `-sI` | Spoofed SYN via zombie | Zombie IP ID +2 | Zombie IP ID +1 | Yes |

!!! trap "Exam traps"
    - "Which scan completes the three-way handshake?" Only TCP connect.
    - "Which scan needs no privileges?" Only TCP connect.
    - The ACK scan never reports `open`. It reports `unfiltered` or `filtered`.
    - In the idle scan the first probe to the zombie is **SYN/ACK**, not SYN.

!!! cpent "CPENT depth: how professionals actually scan"
    - **Two-pass method.** Pass one: a fast sweep of every port, `nmap -p- --min-rate 2000 -n -oA all <host>`. Pass two: `-sC -sV -O` against only the open ports. Much faster than `-A -p-`.
    - **Firewall rule inference.** Run SYN and ACK scans against the same ports. Filtered on SYN but unfiltered on ACK means a stateless filter. Filtered on both means stateful.
    - **Through a pivot.** Only full TCP connections pass a SOCKS proxy, so you are limited to `-sT -Pn`.

!!! try "Try it"
    Run a SYN scan and an ACK scan against the same host and compare the STATE columns.

    ```bash
    nmap -sS -p 21,80 10.77.0.20 ; nmap -sA -p 21,80 10.77.0.20
    ```

!!! recap "Recap: section 4"
    - Three TCP families: open (connect), stealth (SYN, inverse flag, ACK probe), third-party (idle).
    - Connect `-sT` completes the handshake and needs no root. SYN `-sS` sends RST instead of the last ACK.
    - FIN, NULL, Xmas, Maimon: open = silence, closed = RST. Not effective against Windows.
    - ACK `-sA` maps firewalls: RST = unfiltered. TTL below 64 or non-zero window = open.
    - Idle `-sI`: zombie IP ID +2 = open, +1 = closed.

## 5. UDP, SCTP, SSDP, list and IPv6 scans {U}

### UDP scan {M: UDP scan (-sU, root): closed = ICMP type 3 code 3; open = UDP reply or silence (open|filtered). Slow because of ICMP rate limiting}

```diagram m03-udp
UDP scan. Closed ports are loud; open ports are often silent.
```

- **Closed:** ICMP port unreachable, type 3 code 3.
- **Open:** a UDP reply, or very often nothing, reported as `open|filtered`.
- **Command:** `nmap -sU`. It needs root.

UDP scanning is slow because operating systems limit how many ICMP errors they send. Old Linux kernels allowed one per second, so a full scan of one host could take 18 hours. The courseware adds that Windows usually applies no such limit, so UDP scans of Windows hosts run quickly. {U}

A UDP scan reports ports only. Add `-sV` to send real protocol payloads, which turns many `open|filtered` results into `open`:

```bash
nmap -sU --top-ports 50 -sV 10.77.0.10
```

Do not skip UDP. DNS (53), SNMP (161), NTP (123), TFTP (69) and IKE (500) live there and are frequent weak points.

There is an unprivileged variant, **UDP `recvfrom()` and `write()` scanning**. A normal user cannot read ICMP errors directly, but the operating system reports them indirectly: a second `write()` to a closed port fails, and `recvfrom()` returns "connection refused" instead of "try again". {R}

### SCTP INIT and COOKIE ECHO scans {M: SCTP: four-way handshake (INIT, INIT-ACK, COOKIE-ECHO, COOKIE-ACK). INIT scan -sY: INIT-ACK = open, ABORT = closed. COOKIE ECHO scan -sZ: no reply = open|filtered, ABORT = closed}

**SCTP** is a third transport protocol, used in telephone signalling (SS7/SIGTRAN) and voice over IP. It opens with a **four-way** handshake: INIT, INIT-ACK, COOKIE-ECHO, COOKIE-ACK.

```diagram m03-sctp
SCTP INIT scan, the SCTP equivalent of the SYN scan.
```

| Scan | Nmap | Open | Closed | Note |
| --- | --- | --- | --- | --- |
| SCTP INIT | `-sY` | INIT-ACK | ABORT | Half-open, like SYN. Tells open, closed and filtered apart clearly |
| SCTP COOKIE ECHO | `-sZ` | No reply | ABORT | Less conspicuous, but reports `open|filtered` |

### SSDP scan and list scan {R}

- **SSDP** (Simple Service Discovery Protocol) is how Universal Plug and Play (UPnP) devices announce themselves. Querying it reveals routers, cameras and printers and whether their UPnP service is exposed to buffer overflow or denial-of-service attacks. The courseware demonstrates it with the UPnP SSDP **M-SEARCH** discovery tool. On the wire it is UDP port 1900 and the multicast address 239.255.255.250.
- **List scan**, `nmap -sL`, sends nothing to the targets. It lists the addresses in a range and reverse-resolves their names, so every host shows as "not scanned". Use it as a sanity check on your target list.

### IPv6 scan {M: IPv6: 128-bit addresses, 2^64 hosts per subnet, so sweeps are infeasible. Harvest addresses from traffic, logs and email headers, then scan with -6}

IPv6 addresses are **128 bits** long against IPv4's 32. A single standard subnet has 64 bits of host addresses, that is 2^64 of them. Sweeping a range is hopeless.

So IPv6 scanning depends on *finding* addresses first: from network traffic, logs, email headers, DNS, or the "all hosts" link-local multicast address once you control one machine on the segment. Then scan as usual with `-6`:

```bash
nmap -6 -sS -p 22,80,443 fd00:77::20
```

!!! exam "Exam answer / In practice"
    **Exam answer:** at one probe per second, sweeping a 2^64 subnet "would take about 5 billion years".

    **In practice:** the arithmetic gives about 585 billion years. Either way: impossible. Networks often filter IPv4 carefully and forget IPv6, so a host can be closed on one and open on the other.

!!! try "Try it"
    ```bash
    nmap -sL 10.77.0.0/29
    ```

    No packet reaches the targets. If the lab DNS server answers, you get hostnames for free.

!!! recap "Recap: section 5"
    - UDP `-sU`: closed = ICMP type 3 code 3; open = reply or silence (`open|filtered`). Slow because of ICMP rate limits.
    - SCTP has a four-way handshake. `-sY` INIT: INIT-ACK open, ABORT closed. `-sZ` COOKIE ECHO: silence open.
    - SSDP finds UPnP devices; the M-SEARCH tool queries them.
    - `-sL` lists and resolves names without scanning.
    - IPv6: 128-bit addresses, 2^64 per subnet, so harvest addresses, then use `-6`.

## 6. Service versions and faster scans {U}

### Service version discovery {M: `-sV` version detection; `-sC` default scripts; `-O` OS detection; `-A` = -sV, -sC, -O and traceroute}

A port number is only a hint. Version detection, **`-sV`**, connects to each open port, sends probes from Nmap's `nmap-service-probes` database and matches the replies to name the product and version.

```bash
nmap -sV 10.77.0.20                        # version detection
nmap -sV --version-intensity 9 10.77.0.20  # try every probe (default is 7)
nmap -sC -sV 10.77.0.20                    # add the default NSE scripts
nmap -A 10.77.0.20                         # -sV, -sC, -O and traceroute together
```

Illustrative output:

```text
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
25/tcp open  smtp    Sendmail 8.14.4
80/tcp open  http    Apache httpd 2.4.49 ((Unix))
```

Each version string is a lead for Module 5: an exact version tells you which known vulnerabilities to look up. Treat it as a claim, though. Administrators can change banners.

### Nmap scan time reduction {M: Seven scan-time reductions: omit non-critical tests; optimise timing; separate UDP scans; upgrade Nmap; run concurrent instances; scan from a favourable network location; increase bandwidth and CPU time}

The courseware names seven techniques. Know the list.

| Technique | What it means |
| --- | --- |
| Omit non-critical tests | Limit the ports; use `-sn` if you only need to know who is up; leave out `-sC`, `-sV`, `-O`, `--traceroute` and `-A`; switch DNS off with `-n` |
| Optimise timing parameters | Use the `-T` templates |
| Separate and optimise UDP scans | UDP has different timing; run it apart from TCP |
| Upgrade Nmap | Newer versions are faster and fix bugs |
| Execute concurrent Nmap instances | Split the range and run several scans in parallel |
| Scan from a favourable network location | Scan from inside the local network when you can |
| Increase available bandwidth and CPU time | More of both shortens the scan |

| Template | Name | Behaviour |
| --- | --- | --- |
| `-T0` | Paranoid | One probe at a time, 5 minutes apart. For IDS evasion |
| `-T1` | Sneaky | 15 seconds between probes |
| `-T2` | Polite | 0.4 seconds between probes; spares fragile hosts |
| `-T3` | Normal | The default |
| `-T4` | Aggressive | For fast, reliable networks |
| `-T5` | Insane | Sacrifices accuracy for speed |

!!! remember "Remember"
    T0 to T5: **P**lease **S**top **P**ushing, **N**obody **A**cts **I**nsane: Paranoid, Sneaky, Polite, Normal, Aggressive, Insane.

### Port and output options {M: Timing: T0 Paranoid (5 min apart), T1 Sneaky (15 s), T2 Polite (0.4 s), T3 Normal (default), T4 Aggressive, T5 Insane. Options: `-p-` all ports; `-F` top 100; `-iL` targets from file; `-n` no DNS; `-oN` normal, `-oX` XML, `-oG` greppable, `-oA` all}

| Option | Meaning |
| --- | --- |
| `-p 22,80` / `-p 1-1024` / `-p-` | A list, a range, all 65,535 ports |
| `-F` | Fast: the 100 most common ports |
| `-iL file` | Read targets from a file |
| `-oN` / `-oX` / `-oG` / `-oA` | Output as Normal, XML, Greppable, or All three |
| `--open`, `--reason`, `-v` | Show only open ports; show why; be verbose |
| `-n` | No DNS resolution |

!!! try "Try it"
    ```bash
    nmap -sV --version-light -p 21,25,80 10.77.0.20,30,40
    ```

    Three hosts, three ports, with the service version of whatever is open.

!!! recap "Recap: section 6"
    - `-sV` detects versions; `-sC` runs default scripts; `-A` is -sV, -sC, -O and traceroute.
    - Seven ways to cut scan time: omit tests, tune timing, separate UDP, upgrade, run concurrently, scan from nearby, add bandwidth and CPU.
    - `-T0` Paranoid to `-T5` Insane; `-T3` is the default.
    - `-p-` all ports, `-F` top 100, `-iL` targets from a file, `-n` no DNS.
    - `-oN`, `-oX`, `-oG`, `-oA`: normal, XML, greppable, all.

## 7. OS discovery {U}

Knowing the operating system tells you which exploits and which privilege-escalation paths apply. The standards leave many small choices to each implementer, and every operating system chose slightly differently. **Fingerprinting** measures those choices.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware treats **banner grabbing** and **OS fingerprinting** as the same thing: determining the operating system of a remote host.

    **In practice:** working testers use "banner grabbing" for reading the text a *service* announces (`nc`, `curl -I`), and "OS fingerprinting" for analysing the TCP/IP stack. The exam uses the terms interchangeably.

### Active and passive {M: Banner grabbing = OS fingerprinting (exam). Active: send crafted packets, compare replies with a database. Passive: error messages, sniffing traffic, page extensions. Passive fields: TTL, window size, DF bit, TOS. Nmap -O needs one open and one closed port}

| Type | How it works | Detectable |
| --- | --- | --- |
| Active banner grabbing | Send specially crafted packets to the host and compare the replies with a database | Yes |
| Passive banner grabbing | Never probe. Read error messages, **sniff** existing traffic, or infer from page extensions such as `.aspx` (IIS on Windows) | No |

Passive fingerprinting of a sniffed packet looks at **four fields**: **TTL**, **window size**, the **DF** (don't fragment) bit and **TOS** (type of service).

For the active method, the courseware lists Nmap's nine classic tests:

| Test | Probe | Sent to |
| --- | --- | --- |
| 1 {R} | SYN + ECN-Echo | Open TCP port |
| 2 {R} | No flags (NULL) | Open TCP port |
| 3 {R} | URG, PSH, SYN, FIN | Open TCP port |
| 4 {R} | ACK | Open TCP port |
| 5 {R} | SYN | Closed TCP port |
| 6 {R} | ACK | Closed TCP port |
| 7 {R} | URG, PSH, FIN | Closed TCP port |
| 8, "PU" {R} | UDP datagram | Closed UDP port, to draw an ICMP port unreachable |
| 9, "TSeq" {R} | Six SYN packets | Open TCP port, to sample sequence numbers |

This is why Nmap's OS detection needs **at least one open and one closed port**.

!!! exam "Exam answer / In practice"
    **Exam answer:** Nmap uses a series of **nine tests**.

    **In practice:** that describes Nmap's first-generation engine. The current engine sends up to 16 probes. The principle is unchanged.

### TTL and window size {M: TTL / window (exam table): Linux 64 / 5840; FreeBSD 64 / 65535; OpenBSD 255 / 16384; Windows 128 / 65,535 bytes to 1 GB; Cisco routers 255 / 4128; Solaris 255 / 8760; AIX 255 / 16384}

The quickest manual clue is the **TTL** of a reply. It starts at a fixed value and drops by one at each router, so a reply arriving with TTL 61 most likely started at 64.

| Operating system | Initial TTL | TCP window size |
| --- | --- | --- |
| Linux | 64 | 5840 |
| FreeBSD | 64 | 65535 |
| OpenBSD | 255 | 16384 |
| Windows | 128 | 65,535 bytes to 1 gigabyte |
| Cisco routers | 255 | 4128 |
| Solaris | 255 | 8760 |
| AIX | 255 | 16384 |

!!! exam "Exam answer / In practice"
    **Exam answer:** the table above, exactly as written.

    **In practice:** it is a snapshot from the early 2000s. Current OpenBSD and Solaris start at 64, modern Linux advertises a far larger window, and windows scale dynamically. TTL still gives a dependable first guess: about 64 is Unix-like, about 128 is Windows, about 255 is network equipment.

!!! remember "Remember"
    TTL roughly doubles up the list: **64** Linux and BSD, **128** Windows, **255** Cisco and the old Unix giants.

### The tools {M: OS discovery tools: Wireshark (read TTL and window), `nmap -O`, Unicornscan (TTL), NSE `--script smb-os-discovery`, IPv6 `nmap -6 -O`}

| Tool | How |
| --- | --- |
| Wireshark | Capture a reply and read the TTL and window size in the first TCP packet |
| Nmap | `nmap -O <target>` |
| Unicornscan | `unicornscan <target>`; read the OS from the TTL it prints |
| Nmap Scripting Engine | `nmap --script smb-os-discovery <target>` asks Windows file sharing directly. `-sC` runs the default scripts; `--script` names specific ones |
| IPv6 fingerprinting | `nmap -6 -O <target>` |

IPv6 fingerprinting uses a separate detection engine and nearly 18 probes, in this order: sequence generation (S1 to S6), ICMPv6 echo (IE1, IE2), node information query (NI), neighbour solicitation (NS), UDP (U1), TCP explicit congestion notification (TECN), then TCP (T2 to T7). {R}

!!! try "Try it"
    Guess the OS two ways and compare.

    ```bash
    ping -c 1 10.77.0.20 | grep ttl ; nmap -O --osscan-guess 10.77.0.20
    ```

    Lab hosts are Linux containers, so expect a TTL of 64.

!!! recap "Recap: section 7"
    - Exam vocabulary: banner grabbing = OS fingerprinting. Active sends crafted packets; passive sniffs and reads.
    - Passive looks at TTL, window size, DF bit and TOS.
    - TTL: Linux and FreeBSD 64, Windows 128, Cisco, Solaris, AIX and (exam table) OpenBSD 255.
    - `nmap -O` needs one open and one closed port. `smb-os-discovery` asks Windows directly.
    - Also Wireshark, Unicornscan and `nmap -6 -O`.

## 8. Scanning beyond IDS and firewall {U}

A **firewall** decides which packets may pass. An **intrusion detection system (IDS)** watches traffic and raises alerts on patterns, such as one source touching a thousand ports in two seconds. Evasion attacks one of three things: the filter's rules, the detector's pattern matching, or the link between the scan and you.

### The techniques {M: Evasion: fragmentation `-f` / `--mtu`; source routing (loose or strict); source port `-g` / `--source-port`; decoys `-D RND:10` or `-D a,b,ME,c`; IP spoofing `hping3 -a`; MAC spoofing `--spoof-mac` 0, vendor or MAC; custom packets (Colasoft Packet Builder); `--randomize-hosts`; `--badsum`; proxy servers and chaining; anonymizers. A spoofed source cannot complete the handshake. A reply to `--badsum` came from a firewall or IDS. Anonymizers: networked or single-point. Censorship circumvention: AstrillVPN, Tails}

| Technique | Nmap or tool | What it does |
| --- | --- | --- |
| Packet fragmentation | `-f`, `--mtu` | Splits the probe into tiny IP fragments so the TCP header is spread over several packets |
| Source routing | IP options | The sender lists the routers the packet must pass (loose or strict), steering it around a firewall |
| Source port manipulation | `-g` or `--source-port` | Sends from a trusted-looking port such as 80 (HTTP), 53 (DNS) or 20 (FTP data) |
| IP address decoy | `-D RND:10` or `-D a,b,ME,c` | Mixes your probes with identical ones from forged addresses |
| IP address spoofing | `hping3 <target> -a <fake IP>` | Sends probes with a false source address |
| MAC address spoofing | `--spoof-mac 0`, a vendor name, or a full MAC | Fakes the hardware address to pass MAC filters |
| Creating custom packets | Colasoft Packet Builder, NetScanTools Pro | Builds packets by hand so they match no signature |
| Randomising host order | `--randomize-hosts` | Shuffles the target order |
| Sending bad checksums | `--badsum` | Sends deliberately corrupt TCP, UDP or SCTP checksums |
| Proxy servers and proxy chaining | Proxy Switcher, CyberGhost VPN | Routes the scan through intermediaries |
| Anonymizers | Whonix, Psiphon, TunnelBear, I2P | Hides the origin and bypasses censorship |

### The details the exam asks about {U}

**Fragmentation.** The courseware calls its example **SYN/FIN scanning using IP fragments**: the TCP header is split over several fragments so that no single fragment shows a filter the full picture.

```diagram m03-fragment
How -f splits a TCP header into 8-byte pieces. A filter that judges fragments one by one never sees ports and flags together.
```

**Decoys.** `-D RND:10` generates ten random decoy addresses. `ME` in a manual list fixes where your real address sits; without it Nmap picks a random position. Decoys fail if the defender traces router paths or drops responses, and many decoys slow the scan.

**Spoofing.** With a spoofed source you **cannot complete a three-way handshake**, because the replies go to the forged address. That limits spoofing to blind techniques such as the idle scan and to denial of service.

**MAC spoofing** has three forms: `--spoof-mac 0` for a random address, `--spoof-mac Dell` for a vendor's prefix, and `--spoof-mac 00:11:22:33:44:55` for an exact one.

**Colasoft Packet Builder** has three views: **Packet List**, **Decode Editor** and **Hex Editor**. {R}

**Randomising** shuffles hosts in groups of up to **16384**. {R}

**Bad checksums.** A real host drops a packet with a bad checksum. If you get a **reply**, it came from a firewall or IDS that did not bother to verify it.

**Proxy chaining.** Each proxy strips identifying information and passes the request on. The more proxies, the greater the anonymity and the slower the connection. Other proxy tools to recognise: Burp Suite, Tor, Hotspot Shield, Proxifier, IPRoyal. {R}

**Anonymizers** come in two types. A **networked** anonymizer relays you through several computers: hard to trace, but every hop is a risk to confidentiality. A **single-point** anonymizer relays you through one site: simpler, but weaker against traffic analysis. **Censorship circumvention tools**: AstrillVPN and Tails (a live operating system run from a USB stick that leaves no trace).

!!! exam "Exam answer / In practice"
    **Exam answer:** fragmentation works because most IDS skip fragmented packets during port scans to save processing.

    **In practice:** current firewalls and intrusion detection systems reassemble fragments before judging them, and source routing is disabled almost everywhere. These techniques survive in exam questions and against old or badly configured equipment.

!!! try "Try it"
    Watch fragmentation and a decoy scan happen. `--packet-trace` prints every packet sent.

    ```bash
    nmap -sS -f -D RND:3 -p 80 --packet-trace 10.77.0.20
    ```

!!! recap "Recap: section 8"
    - Fragment with `-f`; change source port with `-g`; decoy with `-D`; spoof MAC with `--spoof-mac`.
    - Spoofed source means no completed handshake: replies go elsewhere.
    - `--badsum`: a reply reveals a firewall or IDS that skipped checksum verification.
    - Proxies and proxy chains hide the origin. Anonymizers are networked or single-point.
    - Tools: Colasoft Packet Builder, Proxy Switcher, CyberGhost VPN, Whonix, AstrillVPN, Tails.

## 9. Countermeasures {M}

This is the defender's half of the module, and the exam weights it. A penetration-test report is judged on this section: finding open ports is easy; recommending the right fix is the value.

### Against ping sweeps {M: Ping sweep defence: block ICMP echo; cut off any host sending more than 10 ICMP echo requests; in the DMZ allow only echo reply, host unreachable and time exceeded; Snort}

- Configure firewalls to block incoming ICMP echo requests from unknown sources.
- Use an IDS or IPS such as **Snort** to detect and prevent sweeps.
- **Terminate the connection with any host sending more than 10 ICMP echo requests.**
- Use a DMZ and allow only ICMP **echo reply, host unreachable and time exceeded** in it.
- Limit ICMP with access-control lists; rate-limit ICMP packets.
- Segment the network, and hide internal addresses behind private ranges and NAT.

### Against port scanning {M: Port scan defence: fewest open ports; filter 135-159, 256-258, 389, 445, 1080, 1745, 3268; block outbound ICMP type 3; honeypots; port knocking; TCP wrappers}

- Configure firewall and IDS rules to detect and block probes. The firewall should inspect packet **data**, not only the TCP header.
- Run port scanners against your own hosts to check that the firewall detects them.
- Keep router, IDS and firewall firmware up to date.
- Keep as few ports open as possible. **Filter ports 135-159, 256-258, 389, 445, 1080, 1745 and 3268.**
- Block inbound ICMP message types and **all outbound ICMP type 3 unreachable messages** at border routers.
- Block source routing, and make sure filters cannot be bypassed by a chosen source port.
- Configure anti-scanning and anti-spoofing rules; use TCP wrappers to limit access by domain or address.
- Use proxy servers to block fragmented or malformed packets.
- Divert scans to empty hosts or **honeypots**. Hide open ports with **port knocking**.
- Use an IPS to blacklist scanning addresses; use NAT, egress filtering and VLANs.

### Against banner grabbing {M: Banner defence: Apache `ServerSignature Off`, `ServerTokens Prod`, mod_headers; IIS UrlScan `RemoveServerHeader 1`, `AlternateServerName`; hide file extensions (mod_negotiation); false banners}

**Disable or change the banner.**

- Display false banners; turn off unnecessary services; use server masking tools.
- Apache: use `mod_headers` to rewrite the Server header; set **`ServerSignature Off`**; change **`ServerTokens`** from `Full` to **`Prod`** in `httpd.conf`.
- IIS: set **`RemoveServerHeader`** from 0 to **1** in `UrlScan.ini`; set `AlternateServerName` to a false value; remove `X-Powered-By` through `customHeaders` in `web.config`.
- Disable unneeded HTTP methods such as CONNECT, PUT, DELETE and OPTIONS.

**Hide file extensions.** Replace mappings such as `.asp` with `.htm`; Apache users can use **`mod_negotiation`**. Best of all, use no extensions.

**Other measures.** Filter access to ports that leak banners, monitor with IDS/IPS, and replace clear-text protocols (HTTP, FTP, Telnet) with encrypted ones (HTTPS, SFTP, SSH).

### IP spoofing detection {M: Spoofing detection: direct TTL probes (attacker on a different subnet); IP identification number (works on the same subnet); TCP flow control (SYN/ACK with zero window: an ACK carrying data is spoofed). Initial TTLs: TCP/UDP 64 and 128; ICMP 128 and 255}

| Technique | How it works | Limit |
| --- | --- | --- |
| Direct TTL probes | Send a probe to the claimed source and compare the reply's TTL with the suspect packet's. Different TTL: spoofed | Works when the attacker is on a **different subnet** from the victim |
| IP identification number | Probe the claimed source and compare IP IDs. The reply's IP ID should be close to, and slightly above, the suspect packet's | Works **even on the same subnet** |
| TCP flow control method | A spoofer never sees your replies, so cannot obey your window size. Send SYN/ACK with the **window set to zero**: an ACK that arrives **with data** is spoofed | Applied during the handshake |

```diagram m03-spoofdetect
Direct TTL probe: ask the host the packet claims to be from, and compare.
```

Common initial TTL values: **64 and 128 for TCP and UDP; 128 and 255 for ICMP.**

### IP spoofing countermeasures {M: Spoofing prevention: avoid IP-based trust; firewalls and ACLs; random initial sequence numbers; ingress filtering; egress filtering; encryption (IPsec, the best method)}

- **Avoid trust relationships:** do not authenticate by IP address alone.
- **Use firewalls and filtering**, with ACLs, on both incoming and outgoing packets.
- **Use random initial sequence numbers**, so the next sequence number cannot be predicted.
- **Ingress filtering:** drop incoming packets whose source address is outside the expected range.
- **Egress filtering:** drop outgoing packets whose source address is not your own.
- **Use encryption**, such as IPsec. The courseware calls this the best prevention.
- **SYN flooding countermeasures** also help.
- Others: migrate to IPv6, digital certificates, a VPN on public networks, DHCP static address tables on switches.

### Scanning detection and prevention tools {R}

**ExtraHop** is the featured tool: it discovers and classifies every device and analyses all traffic in real time, including encrypted traffic. Recognise also Splunk Enterprise Security, Scanlogd, Vectra Detect, IBM Security QRadar XDR and Cynet 360 AutoXDR.

!!! hospital "Worked example: scanning a hospital network safely"
    A hospital asks you to assess the segment that carries its lab analysers, an imaging archive and a patient portal. The clinical risk is not your report. It is that an aggressive scan can freeze an old imaging console or an analyser mid-run.

    1. **Agree the window and method with biomedical engineering first.** Which devices are fragile, which hours are safe, and who stands beside the device during the test.
    2. **Discover gently.** `nmap -sn -PE -PS443 -T2 10.20.0.0/24`, excluding any range the biomedical team flags, written to `live.txt`.
    3. **Port scan conservatively.** `nmap -sS -T2 --max-retries 1 -iL live.txt -oA hosp`. No `-T4` or `-T5`, and no version detection yet: `-sV` sends unexpected data that old devices handle badly.
    4. **Add `-sV` only to hosts cleared for it.** Expect clinical protocols: DICOM (104, 11112) on the imaging archive and HL7 (often 2575) on the lab interface.
    5. **Report in clinical terms.** "The lab interface on 10.20.0.45 accepts unauthenticated connections" means "anyone on this network could read or alter patient results". That sentence, not the Nmap output, is the deliverable.

    The same discipline applies in a factory, a power station or a warehouse full of barcode scanners: fragile, old devices first, speed last.

!!! try "Try it"
    Be the defender. The lab web server announces its version. Read the banner you would have to hide:

    ```bash
    curl -s -D - -o /dev/null http://10.77.0.20/ | grep -i -E 'server|powered'
    ```

!!! recap "Recap: section 9"
    - Ping sweeps: block ICMP echo, cut off hosts sending more than 10 echo requests, allow only echo reply, host unreachable and time exceeded in the DMZ.
    - Port scans: fewest open ports; filter 135-159, 256-258, 389, 445, 1080, 1745, 3268; honeypots and port knocking.
    - Banners: `ServerSignature Off`, `ServerTokens Prod`, `RemoveServerHeader 1`, hide file extensions.
    - Spoofing detection: direct TTL probes, IP ID number, TCP flow control (zero window).
    - Spoofing prevention: no IP-based trust, ingress and egress filtering, random sequence numbers, encryption.

## 10. Scanning with an AI assistant {D}

The v13 syllabus adds AI-assisted steps to every stage: hping3 scans, host discovery, port scanning, version discovery, OS discovery, and a custom script that chains them. In each, you describe the task in plain language and the assistant returns a command. The exam may show a prompt and ask which command it produces, so read commands fluently.

| You ask for | A correct command looks like |
| --- | --- |
| Live hosts in a range, addresses only, saved to a file {D} | `nmap -sn 10.10.1.0/24 -oG - | awk '/Up$/{print $2}' > scan1.txt` |
| A fast scan of the hosts in that file, quiet output, saved {D} | `nmap -T4 -iL scan1.txt -oN scan2.txt -v0` |
| An ICMP echo ping sweep {D} | `nmap -sn -PE 10.10.1.0/24` |
| An Xmas scan {D} | `nmap -sX 10.10.1.11` |
| Open ports with service versions for a list of hosts {D} | `nmap -sV -iL scan1.txt --open` |
| A TCP port scan with Metasploit {D} | `msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS 10.10.1.22; run; exit"` |
| The OS from the TTL {D} | `ping -c 1 10.10.1.11`, then read the `ttl=` value |
| Ten ICMP packets with hping3 {D} | `hping3 --icmp --count 10 10.10.1.11` |

A three-line script covers the whole chapter: discover, save the live hosts, version-scan them.

```bash
#!/bin/bash
nmap -sn 10.10.1.0/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt &&
nmap -iL live_hosts.txt -sV -oA scan_results &&
cat scan_results.nmap
```

**A safe pattern for real work:**

1. **Describe the goal and the constraints.** "Find live hosts on 10.77.0.0/24 without ICMP and save all output formats" gets a better command than "scan this".
2. **Ask it to explain output.** Paste a confusing result and ask why a port is `open|filtered`.
3. **Verify before you run.** Assistants invent plausible switches. Check each one against `man nmap`. Case matters: `-sV` is version detection, `-sv` is an error; `-oG` is output, `-OG` is not.

A model drafting a command is not authorisation to scan. The permission rule does not change.

!!! coasp "COASP link: scanning AI systems"
    AI infrastructure is ordinary network software on unusual default ports, often deployed by data teams without authentication. Add these to your port list when the target runs machine-learning workloads, and confirm each against the product's documentation.

    | Port | Often found there |
    | --- | --- |
    | 11434 | Ollama model server |
    | 8888 | Jupyter notebook server |
    | 5000 | MLflow tracking server |
    | 7860, 8501 | Gradio and Streamlit demo apps |
    | 8000-8002 | NVIDIA Triton inference server |
    | 8080, 8081 | TorchServe inference and management |
    | 8265 | Ray dashboard |
    | 6333, 19530 | Qdrant and Milvus vector databases |

    The method is this chapter's method: discover, port scan, version-detect, read the HTTP response. An open model API that lists its models to anyone is the AI-era anonymous FTP server. In COASP the AI also becomes the *target*: the habit of reading a service's replies carefully becomes reading a model's responses for leaked instructions.

!!! try "Try it"
    Ask any AI assistant for "an Nmap command that scans all TCP ports of 10.77.0.45 quickly and saves every output format". Check each switch in `man nmap`, then run it in the lab.

!!! recap "Recap: section 10"
    - The assistant drafts; you verify and you own the decision to run.
    - Discovery to file: `nmap -sn <range> -oG - | awk '/Up$/{print $2}'`.
    - `-iL` reads that file; `-sV --open` lists services on open ports.
    - Metasploit one-liner: `msfconsole -q -x "use auxiliary/scanner/portscan/tcp; ..."`.
    - Check every generated switch; case matters.

## 11. Lab walk-through {D}

Run this in course lab L01. The generic skin (Kestrel Freight, a logistics firm) and the healthcare skin (Aarogya Demo Hospital) behave identically here. Work from the attacker container. Allow about 90 minutes including notes.

```bash
# 1. Host discovery: who is alive on the lab network?
nmap -sn 10.77.0.0/24

# 2. Default port scan of what you found. One host shows nothing. Why?
nmap 10.77.0.10,20,30,40,45

# 3. Full TCP range. The quiet host has a service on a high port.
nmap -p- --min-rate 1000 -oA ports 10.77.0.10,20,30,40,45

# 4. Service and OS detail against only the open ports
nmap -sC -sV -O -p <the ports you found> 10.77.0.20

# 5. UDP on the name server
nmap -sU -p 53,161 -sV 10.77.0.10

# 6. Banner-grab the legacy service by hand
nc 10.77.0.45 <its port>
```

Answer these in your log as you go:

1. Which discovery probe did Nmap use in step 1, and why that one? (You are on the same segment.)
2. Why did step 2 miss the legacy host's service?
3. What do the version strings in step 4 tell you to look up next?
4. Write one countermeasure from section 9 for each thing you found.

Write every command and its result in a log. That log is your evidence in a real engagement and your revision material before the exam.

## Quiz

Twelve questions. The options are shuffled every time you load the page.

```quiz
Q: A SYN scan receives SYN/ACK from a port. What is the port's state?
- Closed
- * Open
- Filtered
- Unfiltered
WHY: SYN/ACK is the open-port reply in the handshake. The scanner then sends RST instead of completing it.
TAG: M

Q: Which flags does an Xmas scan set?
- SYN, ACK and RST
- * FIN, URG and PSH
- FIN and ACK
- No flags at all
WHY: Xmas lights up FIN, URG and PSH. FIN/ACK is the Maimon scan; no flags is the NULL scan.
TAG: M

Q: An ACK probe gets a RST back. What have you learned?
- The port is open
- The port is closed
- * The port is not filtered
- The service version
WHY: The ACK scan maps filtering, not port state. A RST means no stateful firewall blocked the probe.
TAG: U

Q: In an idle scan the zombie's IP ID rises by 2 between your probes. The target port is?
- Closed
- Filtered
- * Open
- Unfiltered
WHY: The zombie sent one extra packet, a RST answering the target's SYN/ACK, so the port is open. A rise of 1 means closed.
TAG: M

Q: Which reply marks a closed UDP port?
- A UDP datagram
- * ICMP type 3 code 3, port unreachable
- RST/ACK
- No reply
WHY: Closed UDP ports answer with ICMP port unreachable. Open ones often stay silent.
TAG: M

Q: Which option makes Nmap skip the port scan and only report which hosts are up?
- `-Pn`
- * `-sn`
- `-sL`
- `-n`
WHY: -sn means no port scan. -Pn skips the ping, -sL only lists targets, -n turns off DNS resolution.
TAG: M

Q: A reply arrives with TTL 126. Using the exam table, the most likely system is?
- Linux
- * Windows
- A Cisco router
- Solaris
WHY: Windows starts at 128. Two router hops bring it to 126.
TAG: M

Q: You FIN-scan a Windows server and learn nothing useful. Why?
- A firewall always blocks FIN packets
- * Windows does not follow the RFC 793 behaviour the scan relies on
- FIN scans need a zombie host
- Windows has no TCP ports
WHY: Inverse scans rely on open ports staying silent. Windows resets from every port, so the scan cannot separate open from closed.
TAG: U

Q: With `--badsum`, you receive a reply to a probe. What does that suggest?
- The target host is misconfigured and vulnerable
- * A firewall or IDS answered without verifying the checksum
- The port is open
- The decoys worked
WHY: A real host discards a packet with a bad checksum. A reply came from a device in the path that did not check.
TAG: U

Q: Which spoofing detection technique works even when attacker and victim share a subnet?
- Direct TTL probes
- * IP identification number
- Ingress filtering
- Port knocking
WHY: TTL comparison needs the attacker to be a different number of hops away. The IP ID method does not.
TAG: M

Q: Which Apache setting stops the server version appearing in the banner?
- `RemoveServerHeader 1`
- * `ServerTokens Prod`
- `mod_negotiation On`
- `AlternateServerName`
WHY: ServerTokens Prod reduces the header to the product name. RemoveServerHeader and AlternateServerName are IIS UrlScan settings.
TAG: M

Q: On a hospital engagement, what comes before any scan?
- Running `-T5` to finish quickly
- * Agreeing timing and fragile-device exclusions with biomedical engineering
- Scanning UDP only
- Asking an AI assistant for permission
WHY: Aggressive scans can crash old medical devices, so the plan is agreed with the people responsible for them first.
TAG: U
```

## Exam cheat sheet

Only the MEMORISE items from this chapter, collected automatically. If a fact is not here, you need to understand or recognise it, not recite it.

[[cheatsheet]]

## Coverage check against the official Module 3

Each sub-topic of the official module, and where this chapter covers it. The full section-by-section verification report is kept with the handbook source as `verification/ceh/m03-scanning-networks.md`. This is a completeness map; no official text is reproduced.

| Official sub-topic | Covered in | Status |
| --- | --- | --- |
| Overview, types and objectives of network scanning | 1 | OK |
| TCP communication flags | 1 | OK, exam/practice note on six vs eight flags |
| TCP/IP communication: handshake and termination | 1 | OK |
| Scanning tools: Nmap, hping3 and its commands, Metasploit, NetScanTools Pro, others | 2 | OK |
| hping scan with AI | 10 | OK |
| Host discovery techniques (ARP, UDP, ICMP echo, sweep, timestamp, address mask, TCP SYN, TCP ACK, IP protocol) | 3 | OK |
| Host discovery with AI | 10 | OK |
| Ping sweep tools | 3 | OK |
| List of common ports and services | 1 | OK, reduced to a must-know list |
| Port scanning technique classification | 4 | OK |
| TCP connect, stealth, inverse flag, Xmas, Maimon, ACK flag probe (TTL, window), IDLE/IPID | 4 | OK |
| UDP scanning, including recvfrom() and write() | 5 | OK |
| SCTP INIT and COOKIE ECHO | 5 | OK |
| SSDP and list scanning; IPv6 scanning | 5 | OK |
| Port scanning with AI; service version discovery, and with AI | 6, 10 | OK |
| Nmap scan time reduction techniques | 6 | OK |
| OS discovery / banner grabbing: active, passive, why | 7 | OK |
| Identifying the target OS: TTL and window table | 7 | OK, exam/practice note |
| OS discovery with Wireshark, Nmap, Unicornscan, NSE, IPv6 fingerprinting, AI | 7, 10 | OK |
| Custom script to automate scanning with AI | 10 | OK |
| Scanning beyond IDS and firewall: all eleven techniques, proxy tools, anonymizers, censorship circumvention | 8 | OK |
| Countermeasures: ping sweep, port scanning, banner grabbing | 9 | OK |
| IP spoofing detection techniques and countermeasures | 9 | OK |
| Scanning detection and prevention tools | 9 | OK |
| Module summary | Recaps and cheat sheet | OK |

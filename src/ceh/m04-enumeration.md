---
title: Module 4 - Enumeration
book: Ethical Hacking Study Handbook
module: 4
kicker: Ethical hacking track · Module 4 of 20
home: index.html
lab: 60
difficulty: Beginner to intermediate
status: Review draft
verified: 18 Nov 2026: CEH v13 courseware Module 04, Microsoft Learn, Nmap reference guide, OpenLDAP admin guide
footer: Unofficial, independent study material. Not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Written in our own words from public protocol standards and tool documentation. Use these techniques only on systems you own or are authorised in writing to test.
---

# Enumeration

[[meta]]

## What this chapter is about

Scanning told you which doors are open. Enumeration walks up to each open door and asks the service behind it to list what it knows: user names, machine names, shared folders, running software. Many services answer far more freely than their owners realise.

!!! story "An everyday picture"
    You are in the lobby of an office block. Scanning was reading the board that shows which floors are occupied. Enumeration is going to each reception desk and asking, politely, "Who works here? Which rooms do you have? Is Mr Kapoor in?" A well-run desk says "I cannot tell you that." A badly run desk hands you the staff list. You have not broken anything. You asked, and the desk answered.

Every list you collect here feeds a later attack. User names feed password guessing. Share names feed data theft. Software versions feed exploit selection. That is why the defender's version of this chapter is short: stop the desk handing out the list.

!!! before "Before you start"
    This chapter assumes five ideas. The one-line version is enough to carry on.

    - **Port.** A number that says which program on a machine a connection is for. Port 25 is mail, port 53 is DNS. Module 3 covers ports.
    - **Service.** A program that waits on a port for requests: a mail server, a file server, a directory.
    - **TCP and UDP.** The two ways of carrying data. TCP sets up a connection and confirms delivery. UDP just sends.
    - **Protocol.** The agreed language a service speaks. Enumeration means speaking that language well enough to ask questions.
    - **Active Directory.** Microsoft's central list of an organisation's users, computers and groups. Section 4 explains how it is queried.

    Modules 2 and 3 help but are not required.

!!! why "Why this matters to you"
    - **Exam candidate.** This module is ports, protocols and commands. Expect "which port", "which tool", "which command returned this output" and "which countermeasure" for each of about a dozen services.
    - **Defending a network.** Every technique here works only because a service was left on, left open or left on its defaults. Section 10 lists the fix for each, and most are one configuration line.
    - **Working with sensitive data.** Shared folders, printers, scanners and medical or industrial devices often speak these old protocols with no password. If you run such a device, this chapter shows what it tells anyone on the network who asks.

### How the tags work

[[legend]]

Facts tagged MEMORISE are collected automatically into the [cheat sheet](#exam-cheat-sheet) at the end.

**How to use this chapter.** Read section 1 first. Sections 2 to 8 each cover one family of services and can be read in any order. Lab L01 offers DNS, web, FTP and mail services, so the "Try it" boxes for those are hands-on; for Windows-only services the box shows you how to confirm the service is absent and names what you would run where it is present.

| After this chapter you can | Section |
| --- | --- |
| Define enumeration and match each service to its port | 1 |
| Enumerate NetBIOS names and read an `nbtstat` table | 2 |
| Explain SNMP community strings, the MIB and `snmpwalk` | 3 |
| Query an LDAP directory | 4 |
| Use the NTP and NFS enumeration commands | 5 |
| Confirm user names through SMTP | 6 |
| Perform zone transfers, cache snooping and zone walking | 7 |
| Recognise IPsec, VoIP, RPC, Unix user and SMB enumeration | 8 |
| Read AI-generated enumeration commands | 9 |
| Recommend countermeasures for each service | 10 |

## 1. Enumeration concepts {U}

**Enumeration** is extracting user names, machine names, network resources, shares and services from a system or network. The attacker makes **active connections** to the target and sends **directed queries**.

```diagram m04-where
Scanning finds the open doors. Enumeration asks what is behind each one.
```

### What it collects {M: Enumeration = active connections and directed queries to extract usernames, machine names, network resources, shares and services; also routing tables, audit and service settings, SNMP and FQDN details, applications and banners. Works in an intranet environment}

Eight kinds of information: network resources; network shares; routing tables; audit and service settings; SNMP and fully qualified domain name (FQDN) details; machine names; users and groups; applications and banners.

The courseware adds that enumeration techniques work in an **intranet** environment: most of these services are meant to be reachable only from inside. It also warns that, unlike the earlier phases, enumeration may be illegal without authorisation.

!!! exam "Exam answer / In practice"
    **Exam answer:** the previous phases gathered information "without any illegal activity"; enumeration needs authorisation.

    **In practice:** you need written authorisation from the moment you send the first packet. Port scanning without permission is already an offence in many countries. Do not read the courseware's sentence as permission to scan freely.

### Seven techniques {M: Enumeration techniques: extract usernames from email IDs; use default passwords; brute-force Active Directory; DNS zone transfer; extract user groups from Windows; extract usernames using SNMP; extract network resources and topology using SNMP}

| Technique | The idea |
| --- | --- |
| Extract user names using email IDs | An address is `username@domain`; the part before the @ is usually the login name |
| Extract information using default passwords | Manufacturers publish default credentials; many are never changed |
| Brute-force Active Directory | Active Directory answers differently for valid and invalid user names, so names can be confirmed, then passwords guessed |
| Extract information using DNS zone transfer | A misconfigured name server hands over its whole list of hosts (section 7) |
| Extract user groups from Windows | A registered user can list the groups they belong to and their members |
| Extract user names using SNMP | Guess the community string, then read the user table (section 3) |
| Extract network resources and topology using SNMP | Walk the SNMP tree for interfaces, routes and neighbours |

### Services and ports {M: Ports: FTP 20/21; SSH and SFTP 22; Telnet 23; SMTP 25; DNS and zone transfer 53; TFTP UDP 69; RPC portmapper 111; NTP UDP 123; Microsoft RPC endpoint mapper 135; NetBIOS name UDP 137, datagram UDP 138, session TCP 139; SNMP UDP 161, trap 162; BGP 179; LDAP 389; SMB direct 445; ISAKMP/IKE UDP 500; NFS 2049; Global Catalog 3268; SIP 5060, 5061 (TLS)}

This table is the backbone of the module. The exam asks it directly.

| Port | Service |
| --- | --- |
| TCP 20, 21 | FTP (data, control) |
| TCP 22 | SSH and SFTP |
| TCP 23 | Telnet |
| TCP 25 | SMTP |
| TCP/UDP 53 | DNS, including zone transfer |
| UDP 69 | TFTP |
| TCP/UDP 111 | RPC portmapper (Unix) |
| UDP 123 | NTP |
| TCP/UDP 135 | Microsoft RPC endpoint mapper |
| UDP 137 | NetBIOS name service |
| UDP 138 | NetBIOS datagram service |
| TCP 139 | NetBIOS session service (SMB over NetBIOS) |
| UDP 161 | SNMP |
| TCP/UDP 162 | SNMP trap |
| TCP 179 | BGP |
| TCP/UDP 389 | LDAP |
| TCP/UDP 445 | SMB over TCP (direct host) |
| UDP 500 | ISAKMP / IKE (IPsec VPN) |
| TCP 2049 | NFS |
| TCP/UDP 3268 | Global Catalog service |
| TCP/UDP 5060, 5061 | SIP (5061 is encrypted with TLS) |

Notes worth understanding: {U}

- **DNS** normally answers over UDP. A reply larger than 512 bytes is cut short and flagged, and the client asks again over TCP. Zone transfers always use TCP.
- **Port 139** carries file and printer sharing on older Windows systems, including the anonymous "null session". The courseware calls restricting it a top priority.
- **Port 445** carries the same sharing protocol directly over TCP, without NetBIOS.
- **Global Catalog** (3268) is a domain controller's index of every object in the whole organisation, not just one domain.
- **FTP** and **Telnet** send passwords in clear text. **TFTP** has no login at all and is used to load firmware on to devices.
- **BGP** (179) is the protocol internet providers use to exchange routes.

!!! remember "Remember"
    The Windows cluster is consecutive: **135** RPC, **137** names, **138** datagrams, **139** sessions, then SMB alone at **445**. SNMP is a pair: **161** asks, **162** receives traps. LDAP **389**, and its organisation-wide cousin the Global Catalog **3268**.

!!! trap "Exam traps"
    - NetBIOS **name** service is UDP **137**. NetBIOS **session** service is TCP **139**. Questions swap them.
    - SNMP queries go to **161**. Traps go to **162**.
    - "SMB over NetBIOS" is 139. "SMB direct host" is 445.

!!! try "Try it"
    Decide which sections apply to the lab network. In the L01 attacker container:

    ```bash
    nmap -p 21,25,53,80,111,139,389,445,2049 --open 10.77.0.10,20,30,40 | grep -E 'report|open'
    ```

    Four services answer: DNS, web, FTP and mail. Those are the ones you can enumerate hands-on. The Windows and Unix file-sharing ports are closed here.

!!! recap "Recap: section 1"
    - Enumeration makes active connections and directed queries to list users, machines, shares and services.
    - It works mainly inside an intranet and needs authorisation.
    - Techniques: email IDs, default passwords, brute-forcing Active Directory, zone transfer, Windows groups, SNMP.
    - Know the port table: 25 SMTP, 53 DNS, 137/138/139 NetBIOS, 161/162 SNMP, 389 LDAP, 445 SMB, 2049 NFS.
    - 500 is IKE, 3268 the Global Catalog, 5060/5061 SIP, 179 BGP.

## 2. NetBIOS enumeration {M}

**NetBIOS** (Network Basic Input/Output System) is the naming and session layer Windows has used for file and printer sharing since the 1980s. The courseware treats it first because it gives away so much: the computers in a domain, the shares on each host, and policies and passwords.

### NetBIOS names {M: NetBIOS name: 16 ASCII characters, 15 for the device name, the 16th for the service type. Codes: `<00>` hostname or domain, `<03>` messenger, `<20>` server (file sharing), `<1D>` master browser, `<1B>` domain master browser. No NetBIOS name resolution for IPv6}

```diagram m04-nbname
The sixteenth character is a code that says which service the name belongs to.
```

A NetBIOS name is a unique **16-character** ASCII string. Fifteen characters name the device; the sixteenth is a code for the service or record type.

| Code | Type | What it means |
| --- | --- | --- |
| `<00>` | Unique | The host name (workstation service) |
| `<00>` | Group | The domain or workgroup name |
| `<03>` | Unique | Messenger service, for the computer or the logged-in user |
| `<20>` | Unique | Server service: the host is sharing files |
| `<1D>` | Group | Master browser for the subnet |
| `<1B>` | Unique | Domain master browser |

To enumerate NetBIOS names the remote system must have file and printer sharing enabled. Microsoft does not support NetBIOS name resolution for IPv6.

### nbtstat {M: `nbtstat -a <name>` remote name table by name; `-A <IP>` remote name table by IP address; `-c` name cache; `-n` local names; `-r` names resolved by broadcast and WINS; `-R` purge and reload the cache; `-RR` release and refresh; `-s` sessions by name; `-S` sessions by IP address}

**nbtstat** is the built-in Windows utility for NetBIOS over TCP/IP. Its switches are case-sensitive.

| Switch | Shows |
| --- | --- |
| `-a <name>` | The name table of a remote computer, given its **name** |
| `-A <IP>` | The name table of a remote computer, given its **IP address** |
| `-c` | The local cache of NetBIOS names and their IP addresses |
| `-n` | The names registered by the local computer |
| `-r` | Counts of names resolved by broadcast and by WINS |
| `-R` | Purges the cache and reloads it |
| `-RR` | Releases and refreshes the names registered with the name server |
| `-s` | Current sessions, with remote computers shown by name |
| `-S` | Current sessions, with remote computers shown by IP address |

!!! remember "Remember"
    Small letter, friendly form; capital letter, numbers. `-a` takes a n**a**me, `-A` takes an **A**ddress. `-s` shows names, `-S` shows addresses. `-c` is the **c**ache, `-n` is **n**ames of this machine.

### Other NetBIOS tools {R}

- **NetBIOS Enumerator**: scans a range of IP addresses for NetBIOS names, user names, domain names and MAC addresses.
- **Nmap**: the `nbstat` script returns NetBIOS names and the MAC address: `nmap -sV -v --script nbstat.nse <target>`.
- Also named: Global Network Inventory, Advanced IP Scanner, Hyena, Nsauditor Network Security Auditor.

### PsTools and Net View {M: PsTools: PsExec (run processes remotely), PsFile, PsGetSid, PsKill, PsInfo, PsList, PsLoggedOn, PsLogList, PsPasswd, PsShutdown. `net view \\computer` lists shares; `/ALL` adds hidden shares; `net view /domain` lists domains}

**PsTools** is Microsoft's suite of command-line tools for managing remote Windows systems. With valid credentials it enumerates a great deal.

| Tool | What it does |
| --- | --- |
| PsExec | Runs a process on a remote system; opens a remote command prompt |
| PsFile | Lists files on a system that are opened remotely |
| PsGetSid | Translates a security identifier (SID) to a name and back |
| PsKill | Kills processes locally or remotely |
| PsInfo | Shows key system facts: build, owner, processors, memory, install date |
| PsList | Shows process, CPU and memory details |
| PsLoggedOn | Shows who is logged on locally and through shared resources |
| PsLogList | Dumps event logs from a local or remote computer |
| PsPasswd | Changes account passwords, locally or remotely |
| PsShutdown | Shuts down or reboots a local or remote computer |

**Net View** lists shared resources:

| Command | Shows |
| --- | --- |
| `net view \\<computer>` | The shares on that computer |
| `net view \\<computer> /ALL` | All shares, including hidden ones |
| `net view /domain` | The domains on the network |
| `net view /domain:<name>` | The computers in that domain |

!!! exam "Exam answer / In practice"
    **Exam answer:** NetBIOS is enumerated first, with `nbtstat`, `net view` and the tools above, on ports 137 to 139.

    **In practice:** current Windows has largely left this behind (see the box below). On a modern network `net view` often returns an error, and testers enumerate shares and users over port 445 with tools such as `smbclient`, enum4linux-ng and NetExec. Old servers, printers and storage boxes still answer NetBIOS, which is why it stays worth checking.

!!! update "Updated: Windows has moved away from NetBIOS and SMBv1"
    Each line gives what changed and when. The exam still expects the courseware's version.

    | Topic | What changed | When | Exam still expects |
    | --- | --- | --- | --- |
    | SMB version 1 | No longer installed by default, starting with Windows 10 version 1709. The Computer Browser service that `net view` browsing relies on goes with it | **October 2017** | NetBIOS and SMB enumeration as described |
    | Computer Browser service | Listed by Microsoft as deprecated | **November 2023** | `net view` lists shares and domains |
    | NTLM authentication | Deprecated; NTLMv1 removed in Windows 11 24H2 and Windows Server 2025 | **June 2024** | NTLM named as an authentication option |
    | SMB signing and NetBIOS ports | Signing required by default; the NetBIOS ports are no longer in the built-in firewall rules, in Windows 11 24H2 and Windows Server 2025 | **October 2024** | Ports 137, 138 and 139 open on Windows hosts |

    Status checked 18 November 2026 on Microsoft Learn.

!!! try "Try it"
    The lab hosts are Linux, so NetBIOS is absent. Confirm it, and read why Nmap says so:

    ```bash
    nmap -p 139,445 --reason 10.77.0.20
    ```

    Both ports are `closed` with reason `reset`. On a Windows machine you own, run `nbtstat -n` and find the `<00>` and `<20>` entries.

!!! recap "Recap: section 2"
    - NetBIOS name: 16 characters, 15 for the name, the 16th a service code. Ports UDP 137, UDP 138, TCP 139.
    - `<00>` host or domain, `<03>` messenger, `<20>` server service, `<1D>` master browser, `<1B>` domain master browser.
    - `nbtstat -a` name, `-A` address, `-c` cache, `-n` local names.
    - PsTools manage remote Windows hosts; `net view` lists shares and domains.
    - In practice modern Windows has SMBv1 and NetBIOS browsing off by default.

## 3. SNMP enumeration {M}

The **Simple Network Management Protocol (SNMP)** lets administrators monitor and configure routers, switches, printers and servers from one place. It runs over UDP. Almost every network device has it, and a great many still accept the default password.

### Managers, agents and community strings {M: SNMP: application-layer protocol on UDP; agent listens on 161, traps go to 162. Two components: SNMP agent (on the device) and SNMP management station. Two passwords: read community string (default "public", view configuration) and read/write community string (default "private", change configuration). SNMP enumeration lists user accounts and devices}

- The **SNMP agent** runs on the managed device.
- The **SNMP management station** (the manager) sends requests to agents and receives their replies.
- A **community string** is SNMP's password. The **read** community string lets you view the device's configuration and is **public** by default. The **read/write** community string lets you change it and is **private** by default.

**SNMP enumeration** uses those strings to list user accounts and devices, and to read ARP tables, routing tables, device details and traffic statistics.

```diagram m04-snmp
The manager asks; the agent answers. A trap is the one message the agent sends without being asked.
```

| Message | Sent by | Purpose |
| --- | --- | --- |
| GetRequest | Manager | Read one value |
| GetNextRequest | Manager | Read the next value in the tree, without knowing its name |
| GetBulkRequest | Manager | Read many values in one request (added in SNMPv2) |
| SetRequest | Manager | Change a value |
| Response | Agent | The answer to any of the above |
| Trap | Agent | Unprompted alert about an event, such as a reboot or a failed link |
| InformRequest | Agent or manager | An alert that must be acknowledged; also used between managers |

!!! exam "Exam answer / In practice"
    **Exam answer:** the agent receives requests on port 161 "and responds to the managers on port 162".

    **In practice:** the agent sends its response back to whichever port the request came from. Port **162** is where the manager listens for **traps**. If a question separates the two, queries are 161 and traps are 162.

### The MIB {M: MIB (Management Information Base): virtual database describing every object SNMP manages, organized as a tree. OID: the numeric name of an object, from the root of the tree. Scalar objects have one instance; tabular objects group related instances}

The **Management Information Base (MIB)** is a virtual database holding a formal description of every object SNMP can manage. It is organised as a tree. Each object has an **object identifier (OID)**: a string of numbers that traces the path from the root.

```diagram m04-mib
Read an OID as directions: start at the root and take the numbered branch at each level.
```

**Scalar** objects have a single instance. **Tabular** objects group related instances, like the rows of an interface table. The manager uses the MIB as a codebook to turn OIDs into readable names.

| Windows MIB file | Covers |
| --- | --- |
| DHCP.MIB {R} | Traffic between DHCP servers and remote hosts |
| HOSTMIB.MIB {R} | Host resources |
| LNMIB2.MIB {R} | Workstation and server services |
| MIB_II.MIB {R} | The TCP/IP-based internet, using a simple architecture |
| WINS.MIB {R} | The Windows Internet Name Service |

### snmpwalk and Nmap {M: `snmpwalk -v1 -c public <target>` walks the tree (`-v2c` for SNMPv2c); `hrSWInstalledName` installed software, `hrMemorySize` RAM. Nmap `-sU -p 161 --script`: `snmp-processes`, `snmp-sysdescr` (server type, OS), `snmp-win32-software`, `snmp-info`}

**snmpwalk** starts at a point in the tree and issues GetNext requests until it runs out, printing every OID and value.

| Command | Result |
| --- | --- |
| `snmpwalk -v1 -c public <target>` | Everything the device will reveal to the string `public`, over SNMPv1 |
| `snmpwalk -v2c -c public <target>` | The same over SNMPv2c |
| `snmpwalk -v2c -c public <target> hrSWInstalledName` | Installed software |
| `snmpwalk -v2c -c public <target> hrMemorySize` | Amount of RAM |
| `nmap -sU -p 161 --script snmp-processes <target>` | Running processes |
| `nmap -sU -p 161 --script snmp-sysdescr <target>` | Server type and operating system |
| `nmap -sU -p 161 --script snmp-win32-software <target>` | Applications installed on a Windows host |
| `nmap -sU -p 161 --script snmp-info <target>` | Basic SNMP information |

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware lists `snmpwalk -v2c -c public <target> <OID> <new value>` as the command "to change an OID to a different value".

    **In practice:** `snmpwalk` only reads. Changing a value is a Set request, done with `snmpset` and the read/write community string. Recognise the courseware's line; use `snmpset` at a keyboard.

### Tools {R}

- **snmp-check**: gathers and neatly prints contact, description, devices, domain, hardware, storage, host name, listening ports, network interfaces, routing, software, uptime and **user accounts**.
- **SoftPerfect Network Scanner**: pings hosts, scans ports, finds shared folders and reads device details through SNMP, WMI, HTTP, SSH and PowerShell.
- Also named: Network Performance Monitor and Engineer's Toolset (SolarWinds), OpUtils (ManageEngine), PRTG Network Monitor.

!!! try "Try it"
    No lab host runs SNMP. See what "closed" looks like for a UDP port:

    ```bash
    nmap -sU -p 161,162 --reason 10.77.0.10
    ```

    The reason is `port-unreach`: the host itself said nothing is listening. Had the state been `open|filtered`, the next command would be `snmpwalk -v2c -c public 10.77.0.10`.

!!! recap "Recap: section 3"
    - SNMP runs on UDP: agent on 161, traps to 162.
    - Community strings are the passwords: read is "public", read/write is "private" by default.
    - The MIB is a tree of objects; an OID is an object's numeric path.
    - `snmpwalk -v1 -c public <target>` dumps the tree; Nmap has `snmp-processes`, `snmp-sysdescr`, `snmp-win32-software`.
    - Tools: snmp-check, SoftPerfect Network Scanner, OpUtils, PRTG.

## 4. LDAP enumeration {U}

The **Lightweight Directory Access Protocol (LDAP)** is how programs query a **directory**: an organised, tree-shaped store of records about users, groups and computers. Microsoft Active Directory is the best-known one.

### How LDAP works {M: LDAP: protocol for accessing distributed directory services such as Active Directory. Client connects to a Directory System Agent (DSA) on TCP port 389 (636 for secure LDAP); data is encoded with Basic Encoding Rules (BER). An anonymous query can reveal usernames, addresses, departmental details and server names}

```diagram m04-ldap
A directory is a tree. Every entry has a full name that spells out its path, and a set of attributes.
```

A client starts a session by connecting to a **Directory System Agent (DSA)**, normally on **TCP port 389**, and sending an operation request. Information travels in **Basic Encoding Rules (BER)** format. Secure LDAP uses port **636**.

If the server allows it, an attacker can query **anonymously** for user names, addresses, departmental details and server names.

### Manual and automated enumeration {M: `ldapsearch -h <target> -x` simple authentication; `-b` search base; `-s base namingcontexts` finds the naming context. Python: `ldap3`. Nmap `--script ldap-brute` brute-forces LDAP logins}

**With Python.** Install the `ldap3` library (`pip3 install ldap3`), then: create a server object for the target and port, asking for all server information; create a connection; call `bind()`. A result of `True` means you are connected. The server information reveals the **naming context**, the root of the tree. Searching from that root with a filter that matches every object class returns the directory's entries.

**With ldapsearch**, in the same order:

| Command | Purpose |
| --- | --- |
| `ldapsearch -h <target> -x` | Test a connection with simple (password-less) authentication |
| `ldapsearch -h <target> -x -s base namingcontexts` | Ask for the naming contexts |
| `ldapsearch -h <target> -x -b "DC=example,DC=local"` | List everything under that base |
| `ldapsearch -h <target> -x -b "DC=example,DC=local" '(objectClass=Employee)'` | Only entries of one object class |
| `... '(objectClass=Employee)' sAMAccountName sAMAccountType` | Only the login-name attributes of those entries |

**With Nmap**: `nmap -p 389 --script ldap-brute --script-args ldap.base='"cn=users,dc=CEH,dc=com"' <target>` tries a list of user names and passwords.

!!! exam "Exam answer / In practice"
    **Exam answer:** `ldapsearch -h <target> -x` connects with simple authentication.

    **In practice:** OpenLDAP 2.5 and later removed the `-h` and `-p` options. Current systems need a URI: `ldapsearch -H ldap://<target> -x`. On a patched Active Directory, anonymous binds return almost nothing; testers use any low-privileged domain account, which can read most of the directory.

### Tools {R}

**Softerra LDAP Administrator** (featured) browses and manages LDAP directories, including Active Directory. Also named: **AD Explorer** (Microsoft), LDAP Admin Tool, LDAP Account Manager and LDAP Search.

!!! cpent "CPENT depth: enumerating Active Directory for real"
    - **Start with one account.** Any valid domain user can read users, groups, computers and trust relationships. That is by design, and it is the heart of internal testing.
    - **Graph it.** BloodHound collects those objects and draws the shortest path from the account you hold to a domain administrator.
    - **Confirm names without logging on.** Kerberos answers differently for valid and invalid user names, so a tool such as kerbrute can test a name list against port 88 without causing failed logons.
    - **One tool, many protocols.** NetExec and enum4linux-ng wrap SMB, LDAP and RPC queries behind single commands. Learn what each wraps before you trust it.

!!! try "Try it"
    No lab host runs a directory. Check the three LDAP ports:

    ```bash
    nmap -p 389,636,3268 --reason 10.77.0.20
    ```

    Then, on paper, write the `ldapsearch` command you would run first if 389 were open, in both its exam form and its current form.

!!! recap "Recap: section 4"
    - LDAP queries a directory, such as Active Directory, through a Directory System Agent on TCP 389.
    - Data is BER-encoded; secure LDAP is 636; the Global Catalog is 3268.
    - Anonymous queries can reveal users, departments and server names.
    - `ldapsearch -x` with `-b` base; the naming context is the root. Python uses `ldap3`.
    - Tools: Softerra LDAP Administrator, AD Explorer; Nmap `ldap-brute`.

## 5. NTP and NFS enumeration {M}

### NTP enumeration {M: NTP: UDP 123; accurate to 10 ms over the Internet, 200 microseconds on a LAN. Reveals hosts connected to the server, client IPs, system names and OS. `ntpdate` collects time samples; `ntptrace` follows the chain to the primary source; `ntpdc` queries ntpd state; `ntpq` monitors ntpd}

The **Network Time Protocol (NTP)** keeps computer clocks in step. It uses **UDP port 123**. It can hold time to within **10 milliseconds** over the public internet and **200 microseconds** or better on a local network.

Administrators rarely think of a time server as sensitive. Queried in the right way it can reveal the hosts connected to it; clients' IP addresses, system names and operating systems; and internal addresses, if the server sits in the DMZ.

| Command | What it does | Switches to recognise |
| --- | --- | --- |
| `ntpdate` | Collects time samples from one or more servers | `-d` debug, `-q` query only, `-u` unprivileged port, `-v` verbose |
| `ntptrace` | Follows the chain of time servers back to the primary source | `-n` numeric addresses, `-m` maximum hosts |
| `ntpdc` | Asks the `ntpd` daemon for its state and statistics | `-l` list peers, `-p` peers with state, `-n` numeric, `-i` interactive |
| `ntpq` | Monitors `ntpd` operations and performance | `-p` peers, `-n` numeric, `-i` interactive, `-c` run a command |

In `ntptrace` output each line shows a **stratum** number: 1 is a server attached directly to a reference clock, and each step away adds one.

Tools named: PRTG Network Monitor (featured), Nmap, Wireshark, udp-proto-scanner and NTP Server Scanner. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** `ntpdc` and `ntpq` list the peers and clients of a time server.

    **In practice:** the NTP project's own manual marks `ntpdc` as deprecated in favour of `ntpq`, and current `ntpd` builds do not answer its query protocol unless an administrator switches it back on. That change followed the abuse of the "monlist" query for denial-of-service amplification. Many Linux systems now run chrony, which answers none of these commands.

### NFS enumeration {M: NFS: TCP 2049, uses RPC; `/etc/exports` lists allowed clients; before NFSv4 the only credential is the client's IP address. `rpcinfo -p` lists RPC services; `showmount -e` lists exports. Tools: RPCScan, SuperEnum}

The **Network File System (NFS)** lets a client use files on a remote server as if they were local. The server **exports** directories; the client **mounts** them. Requests are carried by **remote procedure call (RPC)**.

The server's `/etc/exports` file lists which clients may mount which directories. In versions before NFSv4 the only credential is the **client's IP address**, so an attacker who can spoof an allowed address gets the files.

```diagram m04-nfs
NFS enumeration in four steps.
```

Tools named: **RPCScan** (`python3 rpc-scan.py <target> --rpc`) and **SuperEnum**, a script that enumerates every open port it finds. {R}

!!! try "Try it"
    The lab has neither service. Confirm both in one line:

    ```bash
    nmap -sU -p 123 --reason 10.77.0.10; nmap -p 111,2049 --reason 10.77.0.30
    ```

    Where 111 and 2049 are open, `rpcinfo -p` and `showmount -e` are the next two commands.

!!! recap "Recap: section 5"
    - NTP: UDP 123; accurate to 10 ms on the internet, 200 microseconds on a LAN.
    - It can reveal connected hosts, client addresses, names and operating systems.
    - `ntpdate` samples time, `ntptrace` follows the chain, `ntpdc` and `ntpq` query the daemon.
    - NFS: TCP 2049, exports listed in `/etc/exports`, trust by IP address before version 4.
    - `rpcinfo -p` lists RPC services; `showmount -e` lists exports.

## 6. SMTP enumeration {M}

The **Simple Mail Transfer Protocol (SMTP)** moves email between servers. The courseware gives its ports as **TCP 25, 2525 or 587**. Three of its built-in commands let a stranger test whether a user exists.

### VRFY, EXPN and RCPT TO {M: SMTP (TCP 25, 2525, 587): VRFY validates a user; EXPN shows the delivery addresses of aliases and mailing lists; RCPT TO defines the recipient. Different replies for valid and invalid users (250, 550) reveal valid usernames}

| Command | Its proper purpose | What it leaks |
| --- | --- | --- |
| `VRFY <user>` | Validates a user | Whether that user exists |
| `EXPN <alias>` | Shows the real delivery addresses behind an alias or mailing list | The members of the list |
| `RCPT TO:<user>` | Names the recipient of a message | Whether the server would accept mail for that user |

```diagram m04-vrfy
The same question, two different answers. The difference is the leak.
```

A server that replies `250` for a real user and `550` for a made-up one has just confirmed the user name. Repeat with a list of likely names and you have the valid accounts.

The other SMTP commands in the courseware's table: `HELO` (introduce yourself), `MAIL FROM` (sender), `DATA` (message body), `HELP` and `QUIT`.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware's command table gives the reset command as `RESET`, and one Nmap example lists the mail ports as 25, 365 and 587.

    **In practice:** the SMTP reset command is `RSET`, and the encrypted mail submission port is **465**, not 365. Port 2525 is an unofficial alternative used by some providers. Most modern mail servers disable VRFY and EXPN, so testers fall back on RCPT TO.

### Tools {M: SMTP tools: Nmap scripts `smtp-commands` (supported commands), `smtp-open-relay` (open relay test), `smtp-enum-users` (user enumeration); Metasploit `auxiliary/scanner/smtp/smtp_enum` (uses VRFY with a wordlist, option USER_FILE); smtp-user-enum (`-M` mode VRFY, EXPN or RCPT; `-u` user; `-U` user file; `-t` host; `-T` host file); NetScanTools Pro}

| Tool | Use |
| --- | --- |
| Telnet or netcat | Type the commands by hand |
| `nmap -p 25 --script smtp-commands <target>` | Lists the commands the server supports |
| `nmap -p 25 --script smtp-open-relay <target>` | Tests whether the server will relay mail for anyone |
| `nmap -p 25 --script smtp-enum-users <target>` | Enumerates mail users |
| Metasploit `auxiliary/scanner/smtp/smtp_enum` | Tries a wordlist of names with VRFY. `set RHOSTS`, `set USER_FILE`, `run` |
| **smtp-user-enum** | Guesses names with VRFY, EXPN or RCPT TO. `-M` mode, `-u` one user, `-U` a file of users, `-t` one host, `-T` a file of hosts |
| NetScanTools Pro | Its SMTP Email Generator tests sending through a server and logs the session |

!!! remember "Remember"
    **V**RFY **v**erifies one person. **EXP**N **exp**ands a list into its members. **RCPT** TO is the **rec**i**p**ien**t**. Capital letter means "file" in smtp-user-enum: `-u` one user, `-U` a user file; `-t` one target, `-T` a target file.

!!! try "Try it"
    Confirm three accounts by hand. In the L01 attacker container (use `mnair` in the healthcare skin):

    ```bash
    for u in mfernandes nobody svc_backup; do printf "VRFY $u\r\nQUIT\r\n" | nc -w 3 10.77.0.40 25 | sed -n 2p; done
    ```

    Two names get `250`, one gets `550`. The staff page from Module 2 has just become a confirmed account list.

!!! recap "Recap: section 6"
    - SMTP on TCP 25 (also 2525, 587).
    - VRFY validates a user, EXPN expands a list, RCPT TO names a recipient.
    - Different replies for valid and invalid users (250, 550) reveal the valid names.
    - Tools: telnet or netcat, Nmap `smtp-enum-users`, Metasploit `smtp_enum`, smtp-user-enum.
    - smtp-user-enum: `-M` mode, `-u`/`-U` users, `-t`/`-T` targets.

## 7. DNS enumeration {M}

Module 2 introduced DNS records and the zone transfer as footprinting. Here they return as enumeration, with two further techniques.

### Zone transfer {M: Zone transfer copies the zone file from primary to secondary DNS server. `dig ns <domain>` then `dig @<nameserver> <domain> axfr`; nslookup `set querytype=soa` then `ls -d <domain>`; `dnsrecon -t axfr -d <domain>`}

A **zone transfer** copies the whole zone file from the primary name server to a secondary. An attacker pretends to be a secondary. If the server allows it, the reply lists DNS server names, host names, machine names, user names, IP addresses and aliases.

| Tool | Commands |
| --- | --- |
| `dig` (Linux) | `dig ns <domain>` to find the name servers, then `dig @<name server> <domain> axfr` |
| `nslookup` (Windows) | `set querytype=soa`, enter the domain, then `ls -d <domain>` |
| DNSRecon | `dnsrecon -t axfr -d <domain>` tests every name server for a zone transfer |

A properly configured server answers with a refusal.

### DNS cache snooping {M: DNS cache snooping: ask a DNS server for a cached record to learn which sites its users visited. Non-recursive: `dig @<server> <domain> A +norecurse` (RD bit 0), an answer = cached. Recursive: `+recurse`, a TTL lower than the original = cached}

A resolving DNS server remembers recent answers in its **cache**. **Cache snooping** asks the server whether a particular record is in that cache. If it is, someone who uses that server looked the name up recently. That reveals which banks, suppliers and services an organisation's staff use.

```diagram m04-snoop
The non-recursive method. The server may only answer from memory.
```

| Method | Command | How to read the result |
| --- | --- | --- |
| Non-recursive | `dig @<DNS server> <domain> A +norecurse` | The Recursion Desired bit is 0, so the server may not go and ask. An answer means **cached**. No answer, or a referral to other servers, means **not cached** |
| Recursive | `dig @<DNS server> <domain> A +recurse` | Compare the TTL in the answer with the record's normal TTL. A **lower** TTL means the record had already been sitting in the cache |

### DNSSEC zone walking {M: DNSSEC zone walking follows NSEC records to list a zone; NSEC3 hashes the names to prevent it. Tools: `ldns-walk @<server> <domain>`, `dnsrecon -d <domain> -z`, nsec3map, nsec3walker, DNSwalk}

**DNSSEC** adds digital signatures to DNS records so answers can be verified. To prove that a name does *not* exist, a signed zone returns an **NSEC** record that says "the next name after this one is...". Follow those records from one name to the next and you have walked the entire zone.

**NSEC3** fixes this by replacing the names with cryptographic hashes.

Tools: **LDNS** (`ldns-walk @<DNS server> <domain>`), **DNSRecon** (`dnsrecon -d <domain> -z`), nsec3map, nsec3walker and DNSwalk.

### OWASP Amass and Nmap {M: `amass enum -d <domain>` (`-passive`, or `-active -brute -w <wordlist>`). Nmap DNS scripts: `dns-brute`, `dns-recursion`, `dns-nsec-enum`, `dns-zone-transfer`}

| Command | Purpose |
| --- | --- |
| `amass enum -d <domain>` | Map a domain's DNS, subdomains and related addresses |
| `amass enum -passive -d <domain> -src` | Passive sources only |
| `amass enum -active -d <domain> -brute -w <wordlist>` | Active enumeration with brute-forced names |
| `amass track`, `amass db`, `amass viz -d3` | Compare scans, list stored results, draw a graph |
| `nmap -T4 -p 53 --script dns-brute <domain>` | Brute-force subdomains |
| `nmap -Pn -sU -p 53 --script dns-recursion <server>` | Check whether recursion is enabled |
| `nmap -sU -p 53 --script dns-nsec-enum --script-args dns-nsec-enum.domains=<domain> <server>` | Walk a DNSSEC zone |
| `nmap --script broadcast-dns-service-discovery` | Discover services advertised on the local network |

Other DNS enumeration tools named: Knock, Raccoon, Subfinder and Turbolist3r. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** the Amass subcommands `enum`, `track`, `db` and `viz` as listed.

    **In practice:** Amass has been restructured more than once since the courseware was written. As checked in November 2026 its documentation lists `enum`, `subs`, `track`, `viz`, `assoc` and `engine`; `db` has gone, and several options have changed. Run `amass -h` on your own version.

!!! try "Try it"
    Two questions for the lab's name server. In the L01 attacker container:

    ```bash
    dig axfr kestrel-freight.lab @10.77.0.10; dig @10.77.0.10 example.com A +norecurse | grep status
    ```

    The first hands over the zone: the leak. The second is `REFUSED`: this server answers only for its own zone and keeps no cache, so there is nothing to snoop. That second answer is what a well-separated authoritative server looks like.

!!! recap "Recap: section 7"
    - Zone transfer: `dig @<server> <domain> axfr`; nslookup `ls -d`; `dnsrecon -t axfr`.
    - Cache snooping: `+norecurse`, an answer means cached; `+recurse`, a lowered TTL means cached.
    - DNSSEC zone walking follows NSEC records; NSEC3 hashes the names to stop it.
    - Zone walking tools: `ldns-walk`, `dnsrecon -z`, nsec3map, nsec3walker, DNSwalk.
    - Amass `enum -d`; Nmap `dns-brute`, `dns-recursion`, `dns-nsec-enum`.

## 8. Other enumeration techniques {U}

### IPsec enumeration {M: IPsec: ESP, AH, IKE; ISAKMP on UDP 500 manages Security Associations. `nmap -sU -p 500` finds a VPN gateway; `ike-scan -M` fingerprints it. ike-scan: discovery, fingerprinting, transform enumeration, user enumeration, pre-shared key cracking (psk-crack)}

**IPsec** is the most common technology behind site-to-site and remote-access VPNs. It protects traffic with the **Encapsulating Security Payload (ESP)**, the **Authentication Header (AH)** and **Internet Key Exchange (IKE)**. **ISAKMP**, part of IKE, sets up, negotiates and deletes **security associations (SAs)** and keys on **UDP port 500**.

- `nmap -sU -p 500 <target>` shows whether a VPN gateway is present.
- `ike-scan -M <target>` goes further: it reports the encryption and hashing algorithms, authentication type, key distribution algorithm and SA lifetime.

**ike-scan** has five functions: **discovery** of IKE hosts; **fingerprinting** of the implementation, by retransmission back-off pattern or Vendor ID; **transform enumeration**; **user enumeration** on some VPN systems; and **pre-shared key cracking**, offline, for IKE Aggressive Mode, using the bundled `psk-crack`.

### VoIP enumeration {M: VoIP: SIP on ports 2000, 2001, 5060, 5061. Tools: Svmap, Metasploit SIP Username Enumerator. Attacks: DoS, session hijacking, caller ID spoofing, eavesdropping, SPIT, vishing}

**Voice over IP** carries phone calls over the data network. Calls are set up with the **Session Initiation Protocol (SIP)**, which the courseware places on **UDP/TCP ports 2000, 2001, 5060 and 5061**.

Enumeration yields VoIP gateways and servers, IP-PBX systems (the telephone exchange), and the addresses and extension numbers of phones. That enables denial of service, session hijacking, caller ID spoofing, eavesdropping, spam over internet telephony (**SPIT**) and voice phishing (**vishing**).

Tools: **Svmap**, which finds SIP devices and PBX servers across a range and can ring every phone at once with the INVITE method; and Metasploit's **SIP Username Enumerator**, which finds numeric extensions.

!!! exam "Exam answer / In practice"
    **Exam answer:** SIP uses ports 2000, 2001, 5060 and 5061.

    **In practice:** SIP's registered ports are 5060 and 5061. Port 2000 is Cisco's own phone protocol (SCCP), which is why it appears beside SIP on networks with Cisco phones.

### RPC enumeration {M: RPC portmapper: TCP and UDP 111. `nmap -sR <target>`; NetScanTools Pro RPC Info}

**Remote procedure call (RPC)** lets a program on one machine run a function on another. On Unix and Linux the **portmapper** listens on **TCP and UDP port 111** and tells clients which RPC services exist and where. Enumerating it shows which of those services might be vulnerable.

Commands: `nmap -sR <target>` and `nmap -T4 -A <target>`. NetScanTools Pro has an RPC Info tool for the same job.

!!! update "Updated: March 2011"
    **What changed.** Nmap's separate RPC scan no longer exists. Since **March 2011**, `-sR` has been only an alias for `-sV`: RPC identification is part of ordinary version detection and runs automatically when an RPC service is found.

    **The exam still expects:** `nmap -sR` as the RPC scan.

### Unix and Linux user enumeration {M: `rusers` users logged in to remote machines; `rwho` users on hosts of the local network; `finger` login name, real name, terminal, idle and login time, office, phone (`-l` long, `-s` short)}

| Command | Shows | Switches |
| --- | --- | --- |
| `rusers` | Users logged in to remote machines on the local network, like `who` | `-a` include hosts with nobody logged in; `-l` long listing; `-h`, `-u`, `-i` sort by host, user count, idle time |
| `rwho` | Users logged in to hosts on the local network running the rwho daemon | `-a` include users idle for an hour or more |
| `finger` | A user's login name, real name, terminal, idle time, login time, office and phone number | `-s` short; `-l` long, with home directory, shell and the `.plan`, `.project`, `.pgpkey` and `.forward` files; `-p` omit those files; `-m` no name matching |

These services are switched off on almost every current system. They survive on old Unix hosts and in exam questions.

### SMB enumeration {M: SMB: TCP 445, or via NetBIOS (UDP 137, 138, TCP 139). Nmap `--script smb-protocols`, `smb-enum-shares`. Tools: SMBMap, enum4linux, nullinux, SMBeagle}

**Server Message Block (SMB)** is the protocol Windows uses to share files, printers and serial ports. It runs directly on **TCP 445**, or through NetBIOS on UDP 137 and 138 and TCP 139.

SMB enumeration usually starts with banner grabbing for the operating system and SMB version, then lists shares and users. The results feed SMB relay and brute-force attacks.

| Command | Result |
| --- | --- |
| `nmap -p 445 -A <target>` | Operating system, version and script results for the SMB port |
| `nmap -p 445 --script smb-protocols <target>` | The SMB versions the server supports |
| `nmap -p 445 --script smb-enum-shares <target>` | The shares on the server |

Tools named: **SMBMap**, **enum4linux**, nullinux, SMBeagle and NetScanTools Pro.

!!! trap "Exam traps"
    - ISAKMP is **UDP 500**. `ike-scan` fingerprints VPN gateways; `psk-crack` cracks the pre-shared key.
    - The Unix portmapper is **111**. The Microsoft RPC endpoint mapper is **135**.
    - `finger -l` is the long form and shows the `.plan` file; `-p` suppresses it.
    - SPIT is spam over internet telephony. Vishing is voice phishing.

!!! try "Try it"
    FTP is in the port table and the lab has it. Enumerate the file server without a password:

    ```bash
    printf 'QUIT\r\n' | nc -w 3 10.77.0.30 21; curl -s ftp://10.77.0.30/pub/
    ```

    The first line is the banner, with a software name and version. The listing is what "anonymous" is allowed to see. Read the files; one tells you which account to verify in section 6.

!!! recap "Recap: section 8"
    - IPsec: ISAKMP on UDP 500; `ike-scan -M` fingerprints the gateway; `psk-crack` cracks Aggressive Mode keys.
    - VoIP: SIP on 5060 and 5061 (exam adds 2000, 2001); Svmap and Metasploit's SIP Username Enumerator.
    - RPC: portmapper on 111; `nmap -sR`.
    - Unix users: `rusers`, `rwho`, `finger`.
    - SMB: TCP 445; Nmap `smb-protocols`, `smb-enum-shares`; SMBMap, enum4linux.

## 9. Enumeration with an AI assistant {D}

The v13 syllabus pairs most techniques with an AI prompt. The exam may show the prompt and ask which command fits, so read these fluently.

| You ask for | A correct command looks like |
| --- | --- |
| NetBIOS enumeration of one host {D} | `nbtscan 10.10.1.11` |
| NetBIOS information with the associated names {D} | `nmblookup -A 10.10.1.11` |
| NetBIOS enumeration with Nmap {D} | `nmap -sU -p 137 --script nbstat.nse 10.10.1.22` |
| SNMP enumeration with SnmpWalk {D} | `snmpwalk -c public -v1 10.10.1.22` |
| SNMP enumeration with Nmap {D} | `nmap -sU -p 161 --script snmp-info 10.10.1.22` |
| SNMP processes with Nmap {D} | `nmap -sU -p 161 --script snmp-processes 10.10.1.22` |
| SMTP enumeration, results saved {D} | `nmap -p25 --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} 10.10.1.19 -oN smtp_enum.txt` |
| SMTP enumeration with Metasploit {D} | `msfconsole -q -x "use auxiliary/scanner/smtp/smtp_enum; set RHOSTS 10.10.1.19; run; exit"` |
| DNS enumeration with Nmap {D} | `nmap --script dns-brute --script-args dns-brute.domain=example.com`, then `nmap --script dns-zone-transfer -p 53 example.com` |
| DNS cache snooping, recursive method {D} | `dig @<DNS server> www.example.com +recurse` |
| IPsec enumeration with Nmap {D} | `nmap -sU -p 500 --script ike-version 10.10.1.22` |
| SMB shares with Nmap {D} | `nmap -p 445 --script smb-enum-shares 10.10.1.22` |

The courseware ends with an AI-written shell script. It sets a target range, creates an output folder, then runs four Nmap scans, each saved with `-oN`: a ping sweep (`-sn`), a quick scan (`-T4 -F`), a detailed scan (`-T4 -A`) and a version scan (`-sV`).

!!! exam "Exam answer / In practice"
    **Exam answer:** that script is presented as automating "network enumeration".

    **In practice:** all four commands are Module 3 scans. None of them asks a service for its users, shares or records. Real enumeration scripts loop over the open ports and run the right query for each. And the usual caution applies: check every generated switch against the tool's help, and remember that a drafted command is not authorisation.

!!! coasp "COASP link: enumerating AI services"
    The habit carries straight over: find the service, then ask it to list what it has.

    - **Model servers** usually have a "list models" request. An unauthenticated one tells you every model loaded, and often its size and version.
    - **Vector databases** list their collections. Collection names and counts reveal what documents an assistant was given.
    - **Experiment trackers and notebook servers** list runs, parameters and files.
    - **Tool servers** that connect an assistant to other systems publish the list of tools they offer. That list is the assistant's reach.

    Confirm each request against the product's own documentation. In COASP the same step has a new twist: you can also ask the *model* what it has, in plain language, and a badly guarded one will tell you its instructions and its tools.

!!! try "Try it"
    A real enumeration script: one banner per service, then a count of zone records. In the L01 attacker container:

    ```bash
    for p in "30 21" "40 25"; do set -- $p; printf 'QUIT\r\n' | nc -w 3 10.77.0.$1 $2 | head -1; done; dig +short axfr kestrel-freight.lab @10.77.0.10 | wc -l
    ```

    Ask an AI assistant for the same thing and compare. Did it speak each service's own language, or did it just run more scans?

!!! recap "Recap: section 9"
    - `nbtscan` and `nmblookup -A` for NetBIOS; `nbstat.nse` on UDP 137.
    - `snmpwalk -c public -v1`; Nmap `snmp-info`, `snmp-processes` on UDP 161.
    - `smtp-enum-users` with VRFY, EXPN, RCPT; Metasploit `smtp_enum`.
    - `dns-brute`, `dns-zone-transfer`; `dig +recurse` for cache snooping; `ike-version` on UDP 500.
    - `smb-enum-shares` on 445. Check generated commands; they are drafts.

## 10. Enumeration countermeasures {M}

Each service has its own list. The pattern is the same every time: switch it off if you do not need it; if you do, change the defaults, restrict who can reach it, encrypt it and log it.

### SNMP {M: SNMP defence: turn the service off or change default community strings; SNMPv3; block port 161; ACLs; no read-write; avoid NoAuthNoPriv}

- Remove the SNMP agent or turn the service off. If you cannot, **change the default community strings**.
- **Upgrade to SNMPv3**, which encrypts passwords and messages. Avoid its `NoAuthNoPriv` mode, which protects nothing.
- Block access to TCP/UDP port **161**; restrict SNMP to management addresses with access-control lists.
- Do not configure read-write access where read-only will do.
- Keep management traffic on a separate VLAN; log SNMP access and audit it.
- Windows-specific: apply the Group Policy option "Additional restrictions for anonymous connections"; restrict null session pipes and shares.

### LDAP {M: LDAP defence: SSL or STARTTLS; username different from email address; account lockout; disable anonymous binds; canary accounts and decoy Admin groups}

- LDAP traffic is unencrypted by default: use **SSL or STARTTLS**.
- Choose user names that differ from email addresses, and enable **account lockout**.
- **Disable anonymous binds**; limit what authenticated users can read with ACLs.
- Use NTLM, Kerberos or basic authentication to limit access to legitimate users; add multi-factor authentication.
- Deploy **canary accounts** and decoy groups with "Admin" in the name to mislead and detect attackers.
- Log access to the directory and watch for unusual query patterns.

### NFS {M: NFS defence: restrict `/etc/exports` and permissions; block 2049; `root_squash` on; tunnel through SSH; NFSv4 with Kerberos}

- Give exported file systems proper permissions; export only to named hosts in `/etc/exports`.
- Block NFS port **2049** at the firewall; use `/etc/hosts.allow` and `/etc/hosts.deny`.
- Keep **`root_squash`** on, so a client's root user is not trusted as root on the server.
- Tunnel NFS through SSH, or move to **NFSv4** with Kerberos, to authenticate and encrypt.
- Do not allow suid or sgid programs on exported file systems; log access.

### SMTP {M: SMTP defence: disable or restrict VRFY, EXPN, RCPT TO; disable open relay; ignore mail to unknown recipients; minimal error detail; SPF, DKIM, DMARC}

- Ignore messages to unknown recipients, and give **limited information in error replies**.
- **Disable open relay.**
- **Disable EXPN, VRFY and RCPT TO**, or restrict them to authenticated users.
- Limit the number of connections from one source; rate-limit requests.
- Implement **SPF, DKIM and DMARC**; require authentication and TLS; log and review.

### SMB {M: SMB defence: disable SMB on web, DNS and bastion hosts; block TCP 139 and 445; registry `RestrictNullSessAccess` = 1; SMBv3, not SMBv1}

- Web and DNS servers do not need SMB: disable it on them and on internet-facing ("bastion") hosts, or block **TCP 139 and 445**.
- Add the registry value **`RestrictNullSessAccess`**, set to **1**, under `LanmanServer\Parameters` (inside `HKLM\SYSTEM\CurrentControlSet\Services`) to restrict anonymous access.
- Use **SMBv3** or later; avoid SMBv1.
- Enable the Windows Firewall, patch, enforce strong passwords and tight share permissions.
- Use digitally signed communication; audit logs.

### DNS {M: DNS defence: restrict zone transfers to secondary nameserver IPs; restrict resolver access; disable recursion; DNSSEC; split DNS; keep private hosts out of public zones}

- **Restrict zone transfers** to the IP addresses of your own secondary name servers.
- **Restrict resolver access** to hosts inside the network, and **disable recursion** on servers that should not offer it.
- Randomise source ports and query IDs against cache poisoning.
- Use different servers for the authoritative and resolving roles; use **split DNS** so internal names stay internal.
- Keep private hosts out of public zone files; avoid host names that describe a server's purpose; delete old records.
- Use **DNSSEC**; restrict `version.bind` queries; patch the name server; log and rate-limit queries.

!!! hospital "Worked example: a hospital's printers, scanners and file shares"
    A hospital's network team asks what an ordinary computer on the staff network can learn in an hour. Nothing is exploited; services are only asked questions.

    1. **A ward printer answers SNMP with "public".** Its interface and ARP tables list the addresses of every device it has printed for, including two imaging consoles.
    2. **The imaging archive allows guest file transfer** so a scanner can drop studies there. Anyone can list the folder.
    3. **The mail server confirms accounts.** The staff directory becomes a list of valid logins, including a backup service account whose password never expires.
    4. **The name server gives its whole zone**, including an old laboratory interface nobody remembered.
    5. **A storage box exports a folder to "everyone"** over NFS; it holds scanned referral letters.

    Each fix is one line from section 10: change the community string or move to SNMPv3; give the scanner its own account; disable VRFY; restrict zone transfers; export to named hosts only. The lesson for the hospital is that the leaks came from devices, not from the main servers.

    The same hour in a warehouse finds the same things on label printers, barcode scanners and the dispatch system.

!!! try "Try it"
    Be the defender. This is the reply your mail server should never give:

    ```bash
    printf 'VRFY svc_backup\r\nQUIT\r\n' | nc -w 3 10.77.0.40 25 | sed -n 2p | cut -c1-40
    ```

    Write the reply a hardened server would give to both a real and a made-up name, and say why they must be identical.

!!! recap "Recap: section 10"
    - SNMP: turn it off or change the community strings; SNMPv3; block 161.
    - LDAP: SSL or STARTTLS; no anonymous binds; lockout; canary accounts.
    - NFS: tight `/etc/exports`; `root_squash`; NFSv4 with Kerberos; block 2049.
    - SMTP: disable VRFY, EXPN, RCPT TO probing and open relay; SPF, DKIM, DMARC.
    - SMB: block 139 and 445 on exposed hosts; `RestrictNullSessAccess` = 1; SMBv3. DNS: restrict zone transfers and recursion.

## 11. Lab walk-through {D}

Run this in course lab L01. The generic skin (Kestrel Freight) and the healthcare skin (Aarogya Demo Hospital, `aarogya-demo.lab`) behave identically; swap the domain and the user names. Work from the attacker container. Allow about 60 minutes including notes.

```bash
# 1. Which enumerable services exist?
nmap -p 21,25,53,80,111,139,389,445,2049 --open 10.77.0.10,20,30,40

# 2. DNS: ask for the whole zone
dig axfr kestrel-freight.lab @10.77.0.10

# 3. FTP: read the banner, then list what a guest can see
printf 'QUIT\r\n' | nc -w 3 10.77.0.30 21
curl -s ftp://10.77.0.30/pub/
curl -s ftp://10.77.0.30/pub/onboarding.txt

# 4. SMTP: read the banner, then confirm the accounts you have learned of
nc 10.77.0.40 25
#    type:  HELO x      VRFY nobody      VRFY <a staff login>      VRFY <the service account>      QUIT

# 5. The quiet host: banner-grab the port your Module 3 scan found
nc 10.77.0.45 <its port>
```

Answer these in your log as you go:

1. For each of steps 2 to 5, which row of the port table in section 1 are you using?
2. Step 4: which reply codes did you get for a valid and an invalid name? Try `EXPN` too. What does the server say?
3. Build the table every report needs: host, port, service, version, and what it revealed.
4. For each leak, copy the matching countermeasure from section 10.

Module 5 takes the versions in that table and asks which are vulnerable.

## Quiz

Twelve questions. The options are shuffled every time you load the page.

```quiz
Q: Which port does the NetBIOS name service use?
- TCP 139
- * UDP 137
- UDP 161
- TCP 445
WHY: Name service is UDP 137, datagram service UDP 138, session service TCP 139. SMB direct is 445.
TAG: M

Q: In a NetBIOS name table, what does the code `<20>` indicate?
- The domain master browser
- The messenger service
- * The server service: the host is sharing files
- The host name only
WHY: 20 is the server service. 00 is the host or domain name, 03 the messenger service, 1B the domain master browser.
TAG: M

Q: You know a Windows host's IP address but not its name. Which command shows its NetBIOS name table?
- `nbtstat -a 10.0.0.5`
- * `nbtstat -A 10.0.0.5`
- `nbtstat -c`
- `nbtstat -n`
WHY: Capital -A takes an IP address; small -a takes a name. -c shows the cache and -n the local names.
TAG: M

Q: What are the default SNMP community strings?
- admin and password
- read and write
- * public (read) and private (read/write)
- manager and agent
WHY: The read community string defaults to public and the read/write string to private. Leaving them unchanged is the classic SNMP weakness.
TAG: M

Q: In SNMP, what is an OID?
- The password for write access
- * The numeric name of a managed object, tracing its path from the root of the MIB tree
- The address of the management station
- An unprompted alert from an agent
WHY: The MIB is a tree of objects and each has an object identifier. The unprompted alert is a trap.
TAG: M

Q: An LDAP client connects to which component, on which default port?
- A domain controller on TCP 3268
- * A Directory System Agent on TCP 389
- A management station on UDP 161
- A portmapper on TCP 111
WHY: LDAP sessions start with a connection to a Directory System Agent, normally on TCP 389. 3268 is the Global Catalog.
TAG: M

Q: Which command lists the directories an NFS server exports?
- `rpcinfo -p <target>`
- * `showmount -e <target>`
- `ntptrace <target>`
- `net view \\<target>`
WHY: showmount -e lists exports. rpcinfo -p lists RPC services and their ports; net view is for Windows shares.
TAG: M

Q: Which SMTP command reveals the members of a mailing list?
- VRFY
- * EXPN
- RCPT TO
- HELO
WHY: EXPN expands an alias or list into its delivery addresses. VRFY validates one user; RCPT TO names a recipient.
TAG: M

Q: A mail server answers `250` to `VRFY rkapoor` and `550` to `VRFY xyzzy`. What has it revealed?
- That it is an open relay
- * That rkapoor is a valid account and xyzzy is not
- Its software version
- Nothing useful
WHY: Different replies for valid and invalid users let an attacker confirm user names. Hardened servers answer the same way to both.
TAG: U

Q: With `dig @server example.com A +norecurse`, what does an answer in the reply indicate?
- The zone allows transfers
- DNSSEC is enabled
- * The record was in the server's cache, so someone using it looked the name up recently
- The server is authoritative for every domain
WHY: With recursion off the server may answer only from what it already holds. That is non-recursive cache snooping.
TAG: M

Q: Which record type does DNSSEC zone walking follow, and what was introduced to stop it?
- PTR records; split DNS
- * NSEC records; NSEC3, which hashes the names
- MX records; SPF
- SOA records; zone transfers
WHY: NSEC records name the next entry in the zone, so they can be followed end to end. NSEC3 replaces names with hashes.
TAG: M

Q: A hospital printer answers SNMP queries with the community string "public". What is the best fix?
- Move the printer to a different floor
- Block ICMP echo requests
- * Disable SNMP on it, or change the community string and move to SNMPv3
- Enable VRFY on the mail server
WHY: Remove the service if it is not needed; otherwise change the default string and use SNMPv3, which authenticates and encrypts.
TAG: U
```

## Exam cheat sheet

Only the MEMORISE items from this chapter, collected automatically. If a fact is not here, you need to understand or recognise it, not recite it.

[[cheatsheet]]

## Coverage check against the official Module 4

Each sub-topic of the official module and where this chapter covers it. The section-by-section verification report is kept with the handbook source as `verification/ceh/m04-enumeration.md`. No official text is reproduced.

| Official sub-topic | Covered in | Status |
| --- | --- | --- |
| What is enumeration; information collected | 1 | OK, exam/practice note on authorisation |
| Techniques for enumeration | 1 | OK |
| Services and ports to enumerate | 1 | OK |
| NetBIOS enumeration; name list; nbtstat | 2 | OK, name and switch tables from Microsoft's documentation (official tables are images) |
| NetBIOS enumeration tools; PsTools; Net View; with AI | 2, 9 | OK, update on SMBv1 and NetBIOS in current Windows |
| SNMP enumeration; working of SNMP; MIB | 3 | OK, exam/practice note on port 162 |
| SnmpWalk; Nmap SNMP scripts; SNMP tools; with AI | 3, 9 | OK, exam/practice note on changing values |
| LDAP enumeration: manual (Python), automated (Nmap), ldapsearch, tools | 4 | OK, exam/practice note on `-h` |
| NTP enumeration: commands and tools | 5 | OK, switch tables reduced; exam/practice note on ntpdc |
| NFS enumeration: rpcinfo, showmount, RPCScan, SuperEnum | 5 | OK |
| SMTP enumeration: VRFY, EXPN, RCPT TO; Nmap; Metasploit; tools; with AI | 6, 9 | OK, exam/practice note on RSET and port 465 |
| DNS enumeration using zone transfer (dig, nslookup, DNSRecon) | 7 | OK |
| DNS cache snooping: non-recursive and recursive; with AI | 7, 9 | OK |
| DNSSEC zone walking and tools | 7 | OK |
| DNS enumeration using OWASP Amass and Nmap; with AI | 7, 9 | OK, exam/practice note on Amass |
| IPsec enumeration; ike-scan; with AI | 8, 9 | OK |
| VoIP enumeration; Svmap | 8 | OK, exam/practice note on ports |
| RPC enumeration | 8 | OK, update on `nmap -sR` |
| Unix/Linux user enumeration | 8 | OK |
| SMB enumeration; with AI | 8, 9 | OK |
| Custom script to automate network enumeration with AI | 9 | OK, exam/practice note |
| Countermeasures: SNMP, LDAP, NFS, SMTP, SMB, DNS | 10 | OK, reduced to the key measures |
| Module summary | Recaps and cheat sheet | OK |

---
title: Module 6 - System Hacking
book: Ethical Hacking Study Handbook
module: 6
kicker: Ethical hacking track · Module 6 of 20
home: index.html
lab: 140
difficulty: Intermediate
status: Review draft
verified: 19 Nov 2026: CEH v13 courseware and Lab Manual Module 06, TryHackMe and HTB Academy practice material, Microsoft, NIST, Apple, hashcat.net, the NetExec, BloodHound, PowerSploit and Impacket repositories, l0phtcrack.gitlab.io, dban.org
footer: Unofficial, independent study material. Not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Written in our own words from public standards and tool documentation. Use these techniques only on systems you own or are authorised in writing to test.
---

# System Hacking

[[meta]]

## What this chapter is about

Modules 2 to 5 collected information: which machines exist, which doors are open, which accounts and weaknesses they have. This chapter is what an attacker does with that information on one machine and then on the network around it. The courseware splits the work into four phases, and the whole module hangs on them: get in, get more rights, stay in, and hide the visit.

!!! story "An everyday picture"
    Picture a burglar and an office block. First they get through one door: a stolen key, a lock that was never fitted properly, or a staff member who lets them in. That is **gaining access**. Inside, a visitor's badge is not enough, so they find the caretaker's master key: **escalating privileges**. They wedge a fire door so they can return next week, and hide their tools above a ceiling tile: **maintaining access**. Last, they wipe the visitor book and the camera recording: **clearing logs**. A penetration tester walks the same four steps, with permission, so that the owner learns which door, which key, which wedge and which camera failed.

It is the longest module so far, and the exam treats it as vocabulary plus order: four phases, four families of password attack, eight steps of a buffer overflow, about thirty named ways to raise privileges, the kinds of keylogger, rootkit and steganography, and eight ways to cover tracks.

!!! before "Before you start"
    This chapter assumes seven ideas. The one-line version is enough to carry on.

    - **Hash.** A fixed-length fingerprint calculated from data. It cannot be run backwards, so systems store the hash of a password, not the password.
    - **Privilege.** What an account is allowed to do. An **administrator** (Windows) or **root** (Linux) can do almost anything; a standard user cannot.
    - **Process and memory.** A running program and the working space it uses. Passwords and keys pass through memory while a program runs.
    - **Registry.** The Windows database of settings, including what starts at boot.
    - **Domain and domain controller.** A domain is a group of Windows computers and users managed centrally by **Active Directory (AD)**; the domain controller (DC) is the server that checks every logon.
    - **Shell.** A text window that runs commands on a computer. A "remote shell" is that window on someone else's machine.
    - **Log.** The record a system keeps of who did what and when.

    Modules 3 to 5 help. Module 7 (malware) is the companion to sections 12 and 13.

!!! why "Why this matters to you"
    - **Exam candidate.** Expect "which attack is this?" questions on password attacks and privilege escalation, ordered lists (the four phases, the buffer overflow steps, the exploitation steps), port numbers for name-resolution poisoning and remote management, and tool-to-purpose matching.
    - **Defending a network.** Every technique here has a countermeasure, and most of them are settings: turn off old name-resolution protocols, randomise local administrator passwords, limit where administrators log on, send logs somewhere the intruder cannot reach.
    - **Working with sensitive data.** One reused password or one shared local administrator account is how a single infected desktop becomes a whole-hospital, whole-school or whole-firm incident. Sections 4, 6 and 11 explain the chain.

### How the tags work

[[legend]]

Facts tagged MEMORISE are collected automatically into the [cheat sheet](#exam-cheat-sheet) at the end.

**How to use this chapter.** Sections 1 to 6 are passwords and credentials; 7 to 9 are exploitation; 10 and 11 are privilege escalation; 12 to 15 are staying in; 16 is covering tracks. If time is short, read 1, 3, 4, 8, 10, 13 and 16. This chapter has no lab of our own. Each "Practise it" box names the official EC-Council lab, the TryHackMe rooms and the HTB Academy modules that cover the skill. Commands shown are **examples that were not run** for this chapter.

!!! stop "Where these notes stop, and where to read on"
    **What is held back.** This chapter explains every technique in the module, names its tools and gives its defence. It does **not** print working attack command lines: remote-shell one-liners, payload-building commands, credential-dumping and ticket-forging commands, or exploit code. Those were left out on purpose when the sources were read, so they are not in our notes either.

    **Where to read them in full.** Each affected section ends with a box like this one, naming the exact part of the EC-Council e-book, the Lab Manual task, the TryHackMe room and the HTB Academy section that shows the commands, to be used inside those lab environments.

| After this chapter you can | Section |
| --- | --- |
| Name the four phases of system hacking and the goal of each | 1 |
| Explain how Windows stores and checks passwords: SAM, NTLM and Kerberos | 2 |
| Classify any password attack into one of four families | 3 |
| Explain pass-the-hash, name-resolution poisoning, Kerberoasting and relaying | 4 |
| Describe rainbow tables, salting and the main cracking tools | 5 |
| List the defences against password attacks | 6 |
| Give the seven steps of exploiting a vulnerability and the Metasploit module types | 7 |
| Give the eight steps of a Windows buffer overflow and the defences | 8 |
| Say what BloodHound, PowerView and Seatbelt are used for | 9 |
| Tell horizontal from vertical escalation and match techniques to names | 10 |
| Explain pivoting, relaying, DCSync and the defences against escalation | 11 |
| Classify keyloggers and spyware | 12 |
| Classify rootkits and explain NTFS alternate data streams | 13 |
| Classify steganography and steganalysis methods | 14 |
| Name host and domain persistence techniques | 15 |
| List the eight ways attackers cover their tracks and the defences | 16 |

## 1. The four phases of system hacking {M}

The courseware's hacking methodology, introduced in Module 1, reaches its hands-on part here. Footprinting, scanning, enumeration and vulnerability analysis are finished; four phases remain.

```diagram m06-phases
The four phases of system hacking and what each one is for.
```

### The phases and their goals {M: System hacking phases, in order: gaining access (password cracking, vulnerability exploitation), escalating privileges, maintaining access (executing applications, hiding files, persistence), clearing logs}

| Phase | Goal | Main techniques in the courseware |
| --- | --- | --- |
| 1. Gaining access | Get past the logon or the software's defences | Password cracking, exploiting vulnerabilities, buffer overflows |
| 2. Escalating privileges | Turn a low-rights account into an administrator's | Misconfigurations, unpatched flaws, stolen tokens |
| 3. Maintaining access | Keep control and collect data | Executing applications (keyloggers, spyware, backdoors), hiding files (rootkits, data streams, steganography), persistence |
| 4. Clearing logs | Remove the evidence | Disabling auditing, clearing and editing logs, hiding artefacts |

The courseware's own section title for the last phase is "Clearing Logs"; its summary and older editions call it "covering tracks". Treat the two as the same phase.

!!! remember "Remember"
    **G-E-M-C: Get in, Elevate, Maintain, Clear.** Hiding files belongs to *maintaining access*, not to clearing logs. That placement is a common question.

!!! trap "Exam traps"
    - **Executing applications** is part of maintaining access. The courseware calls it "owning" the system.
    - **Enumeration is not system hacking.** It is the step before; this module starts once a target account or weakness is known.

!!! try "Practise it"
    **Official ECC lab:** the Module 06 Lab Manual is organised by these four phases: Lab 1 gain access, Lab 2 escalate privileges, Lab 3 maintain access and hide, Lab 4 clear logs, then an Active Directory lab and an AI lab. **TryHackMe:** Blue (free) walks one Windows machine through all four in miniature. **HTB Academy:** none specific to this section.

    On paper: for the burglar story at the top of the chapter, write the phase name beside each sentence.

!!! recap "Recap: section 1"
    - Four phases: gaining access, escalating privileges, maintaining access, clearing logs.
    - Gaining access means cracking passwords or exploiting a weakness.
    - Maintaining access includes executing applications and hiding files.
    - "Clearing logs" and "covering tracks" name the same phase.
    - Everything before this module was information gathering.

## 2. How Windows stores and checks passwords {M}

To attack a password it helps to know where it lives and how it is checked. The courseware names three mechanisms: the SAM database, NTLM and Kerberos.

### The SAM database {M: SAM file: %SystemRoot%\system32\config\SAM, mounted in the registry at HKLM\SAM; locked while Windows runs. Domain accounts live in NTDS.dit on the domain controller}

The **Security Accounts Manager (SAM)** is the file where a Windows computer keeps its local user names and password hashes. On a domain controller the same job is done by the Active Directory database. Windows keeps the SAM locked while it is running, so it cannot simply be copied; attackers read the copy on disk from another operating system, or pull the hashes out of memory with administrator rights.

Two kinds of hash appear in the courseware. The **LM hash** is the old LAN Manager format: the password is upper-cased, cut into two seven-character halves and each half is processed separately, which makes it quick to break. It has been switched off by default since Windows Vista, and a password longer than fourteen characters never gets one. The **NT hash** (often called the NTLM hash) replaced it and is what modern Windows stores.

!!! update "Updated: October 2017"
    **What changed.** The courseware lists "enable SYSKEY" as a defence and describes SYSKEY as extra encryption for the SAM. Microsoft removed the `syskey.exe` tool from Windows 10 version 1709 and Windows Server 2016 version 1709 in **October 2017**; Windows no longer prompts for a SYSKEY password, and Microsoft recommends BitLocker drive encryption instead. Checked on support.microsoft.com, 19 November 2026.

    **The exam still expects:** SYSKEY as the feature that protects the SAM database, first shipped with Windows NT 4.0.

### NTLM: challenge and response

**NTLM** (NT LAN Manager) proves that a user knows a password without sending it. The server sends a random number, the **challenge** (the courseware calls it a 16-byte nonce); the client encrypts it with the password hash; whoever holds the stored hash repeats the calculation and compares. There are three versions of the response: LM, NTLMv1 and NTLMv2, each stronger than the last.

```diagram m06-ntlm
NTLM in a domain: the password never crosses the network, but the hash is all an attacker needs.
```

The weakness is in that last sentence of the caption. Because the hash is the only secret used, anyone who steals the hash can answer the challenge. Section 4 builds on this.

!!! update "Updated: June 2024"
    **What changed.** Microsoft added every version of NTLM (LAN Manager, NTLMv1 and NTLMv2) to its list of deprecated Windows features in **June 2024**: no further development, and removal planned in a future release. NTLMv1 is already gone from Windows 11 version 24H2 and Windows Server 2025. Checked on learn.microsoft.com (page updated 11 November 2026).

    **The exam still expects:** NTLM as one of the three Microsoft authentication mechanisms, with Kerberos as the default for domains.

### Kerberos: tickets {M: Kerberos: KDC = Authentication Server (AS) + Ticket Granting Server (TGS). AS issues the TGT; TGS issues service tickets. Port 88. Default for Windows domains since Windows 2000}

**Kerberos** replaces repeated password checks with **tickets**. A trusted third party, the **Key Distribution Center (KDC)** on the domain controller, has two parts. The **Authentication Server (AS)** checks the user once and hands back a **Ticket Granting Ticket (TGT)**. The **Ticket Granting Server (TGS)** swaps that TGT for a **service ticket** each time the user wants a file share, a database or a printer. The service reads the ticket; it never talks to the KDC itself.

```diagram m06-kerberos
Kerberos in three exchanges: one logon, then a ticket for each service.
```

Kerberos gives single sign-on, mutual authentication (each side proves itself) and protection against replay through time stamps. It listens on port 88.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware calls the service ticket a "TGS" in places and an "ST" in others, and says Kerberoasting cracks the TGS while AS-REP roasting cracks the TGT.

    **In practice:** the TGS is the *server* that issues tickets; what it issues is a service ticket. TryHackMe and HTB Academy use the same loose shorthand, so read "TGS" in a question as "service ticket" unless it clearly means the server.

!!! try "Practise it"
    **Official ECC lab:** none for this section. **TryHackMe:** Active Directory Basics (Premium), tasks on Kerberos and NetNTLM authentication. **HTB Academy:** Introduction to Active Directory (Tier 0), sections "Kerberos, DNS, LDAP, MSRPC" and "NTLM Authentication"; Password Attacks (Tier 0), section "Windows Authentication Process".

    Example, not run. On your own Windows machine, list the Kerberos tickets your session holds:

    ```bash
    klist
    ```

!!! recap "Recap: section 2"
    - Local password hashes live in the SAM file; domain hashes live on the domain controller.
    - LM hashes are old, split in two halves and weak; NT hashes replaced them.
    - NTLM is challenge and response; the hash alone is enough to answer.
    - Kerberos uses a KDC made of an AS (gives the TGT) and a TGS (gives service tickets).
    - SYSKEY is the exam's SAM protection, though Microsoft removed it in 2017.

## 3. Password attacks: the four families {M}

**Password cracking** means recovering a password from stored or transmitted data. Testers do it to show that weak passwords exist; administrators do it to recover lost ones. The courseware sorts every technique into four families, and "which family?" is the standard exam question.

```diagram m06-pwtypes
The four families of password attack, with the techniques the courseware puts in each.
```

### The four families {M: Password attack families: non-electronic (shoulder surfing, social engineering, dumpster diving); active online (guessing, dictionary, brute force, spraying, mask, hash injection, LLMNR/NBT-NS poisoning, Kerberos cracking, NTLM relay); passive online (wire sniffing, man-in-the-middle, replay); offline (rainbow tables, distributed network attack)}

| Family | The attacker… | Techniques |
| --- | --- | --- |
| **Non-electronic** | needs no technical skill | Shoulder surfing, social engineering, dumpster diving |
| **Active online** | talks to the target system | Guessing, dictionary, brute force, spraying, mask, hash injection, name-resolution poisoning, Trojans and keyloggers, internal monologue, Markov chain, Kerberos password cracking, NTLM relay |
| **Passive online** | only listens | Wire sniffing, man-in-the-middle, replay |
| **Offline** | works on a stolen copy of the hashes | Rainbow tables, distributed network attack |

### Guessing strategies

These names describe *how candidate passwords are chosen*. Learn each with its one-line meaning.

| Attack | Meaning |
| --- | --- |
| **Dictionary** | Try every word in a list. Fast; fails against passphrases and random strings |
| **Brute force** | Try every possible combination. Always succeeds in the end; on average after half the possibilities |
| **Rule-based** | Used when something about the password is known, such as "two digits at the end" |
| **Hybrid** | Dictionary words with numbers or symbols added: `system1` |
| **Syllable** | Dictionary and brute force combined, for passwords that are not real words |
| **Mask** | Brute force limited to a known pattern, such as three letters then three digits |
| **Password spraying** | One or two common passwords tried against *many accounts*, staying under the lockout limit |
| **Password guessing** | A person tries likely passwords by hand; high failure rate |
| **Default passwords** | The maker's password was never changed; published lists exist |
| **Combinator** | Join words from two lists: 100 words and 70 words give 7,000 candidates |
| **Fingerprint** | Break a passphrase into single- and multi-character pieces and recombine them |
| **PRINCE** | One list; chain one to several words together into longer candidates |
| **Toggle-case** | Try every upper- and lower-case version of each word |
| **Markov chain** | Split leaked passwords into two- and three-character fragments and build likely new ones from the statistics |

Spraying matters because it avoids the defence aimed at brute force. Ten wrong guesses on one account lock it; one wrong guess on each of ten thousand accounts locks nothing. The courseware lists the ports commonly sprayed: SSH 22, Telnet 23, FTP 21, Kerberos 88, SMB 445 and Microsoft SQL Server 1433.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware's "GPU-based attack" is malware that abuses a browser's graphics interface to *watch* what a user types: a side-channel attack that steals passwords as they are entered.

    **In practice:** when testers say "GPU cracking" they mean something else entirely: using graphics cards to try billions of hashes a second offline (section 5). If a question describes spying through the graphics processor, the courseware's term is the answer.

Three more terms appear in the practice material and in everyday work, **outside the courseware**: **credential stuffing** (trying user name and password pairs leaked from another site, because people reuse them), **reverse brute force** (one password against a list of user names, the idea behind spraying) and **distributed brute force** (many machines sharing the work).

!!! remember "Remember"
    **Spraying goes wide; brute force goes deep.** Many accounts, one password, against one account, many passwords.

!!! trap "Exam traps"
    - **Dictionary or hybrid.** If the question mentions adding digits or symbols to words, it is hybrid.
    - **Rule-based or mask.** Both use known facts. Mask is the courseware's term when a *pattern of character types* limits a brute-force run.
    - **Rainbow table is offline.** It needs the stolen hashes; it never touches the live system.
    - **Hash injection is active online**, even though no password is ever cracked.

!!! try "Practise it"
    **Official ECC lab:** none dedicated; password cracking appears inside Lab 1 Task 1 and the Active Directory lab. **TryHackMe:** Password Cracking (Premium, published May 2026); Introduction to Wordlists (Premium, published May 2026); Hydra (free). **HTB Academy:** Login Brute Forcing (Tier II, free to unlock), sections "Introduction" to "Hybrid Attacks"; Password Attacks (Tier 0), sections "Introduction to Password Cracking" and "Spraying, Stuffing, and Defaults".

    On paper: a six-character password uses only lower-case letters. How many possibilities are there, and how many does adding two more characters give? (26 multiplied by itself six times is about 300 million; eight times is about 200 billion.)

!!! recap "Recap: section 3"
    - Four families: non-electronic, active online, passive online, offline.
    - Dictionary tries a list; brute force tries everything; hybrid adds digits and symbols to words.
    - Spraying tries one password on many accounts to avoid lockout.
    - Combinator, fingerprint, PRINCE, toggle-case and Markov chain are ways of building candidates.
    - The courseware's "GPU-based attack" is a side channel, not fast cracking.

## 4. Stealing and replaying credentials on a Windows network {M}

The attacks in this section never guess a password. They capture something that *stands in* for the password, a hash or a ticket, and either reuse it directly or take it away to crack. All of them are "active online" in the courseware's table.

### Hash injection, or pass-the-hash

Section 2 showed that NTLM uses only the hash. In a **pass-the-hash** attack the intruder, already an administrator on one machine, copies the hashes held in that machine's memory and presents one of them to another server as if it were a logon. No cracking is needed. The prize is the hash of a domain administrator who logged on to the compromised machine earlier.

The courseware lists four places hashes come from: cached logon hashes, the SAM file, a captured challenge and response, and the memory of the `lsass.exe` process (the Windows service that handles logons).

### Poisoning name resolution {M: LLMNR UDP 5355; NBT-NS UDP 137. When DNS fails, Windows asks the local network; an attacker answers and captures an NTLMv2 hash. Tool: Responder}

When a Windows machine cannot find a name through DNS, it falls back to asking every machine nearby, using **LLMNR** (Link-Local Multicast Name Resolution, UDP port 5355) and **NBT-NS** (NetBIOS Name Service, UDP port 137). Anyone on the network can answer. The attacker's tool replies "that is me", the victim tries to log on to it, and the attacker records the NTLMv2 challenge and response for offline cracking. A mistyped share name is enough to trigger it.

```diagram m06-llmnr
LLMNR and NBT-NS poisoning: a typing mistake hands a crackable hash to a listener.
```

The tool named in the courseware and used in the official lab is **Responder**. The practice material adds **WPAD** (the protocol browsers use to find a proxy automatically) as a third thing Responder can answer for; that is outside the courseware.

### NTLM relay

Instead of cracking the captured response, the attacker can pass it straight on to a second server while it is still fresh, and be logged on there as the victim. This is an **NTLM relay** attack. It works only where the second server does not insist on **SMB signing** (a check that each message really comes from the party that logged on), which is why enforcing signing is the main defence.

### Internal monologue

Reading `lsass.exe` memory is noisy and modern protections block it. The **internal monologue** attack avoids it: from a compromised account the tool asks Windows itself to produce an old-style NetNTLMv1 response to a challenge the attacker chose, after quietly lowering three NTLM settings, and then restores the settings. The weak response is cracked with rainbow tables. The exam point is the reason it exists: it gets hashes **without touching LSASS**.

### Cracking Kerberos: two roasting attacks {M: Kerberoasting: any domain user requests a service ticket for an account with an SPN; ticket is encrypted with the service account's hash; crack offline. AS-REP roasting: accounts with pre-authentication disabled; no password needed to request; crack the reply offline}

```diagram m06-roast
Kerberoasting and AS-REP roasting side by side: both end in offline cracking.
```

| | Kerberoasting | AS-REP roasting |
| --- | --- | --- |
| Target accounts | **Service accounts**: any account with a Service Principal Name (SPN) | Users with **"Do not require Kerberos preauthentication"** ticked |
| What the attacker needs | Any ordinary domain account | Only a list of user names |
| What is captured | A service ticket, part of it encrypted with the service account's hash | The AS reply, part of it encrypted with the user's hash |
| Then | Crack offline | Crack offline |
| Courseware shorthand | "Cracks the TGS" | "Cracks the TGT" |

!!! update "Updated: April 2026"
    **What changed.** Kerberoasting has been practical because service tickets were often encrypted with the old RC4 cipher, whose key is simply the NT hash. Microsoft changed the default in three steps during 2026: audit events from January, domain controllers issuing **AES-only tickets by default from the April 2026 security update**, and the rollback option removed in July 2026. RC4 now works only where an administrator has set it deliberately. Checked on Microsoft's Tech Community and message-centre pages, 19 November 2026.

    **The exam still expects:** Kerberoasting described as cracking RC4-encrypted service tickets. A weak service-account password is still crackable under AES, only more slowly.

!!! exam "Exam answer / In practice"
    **Exam answer:** the Lab Manual's Active Directory lab says Kerberoasting extracts "TGT hashes" and describes the hashcat mode it uses, 13100, as an "AS-REQ pre-auth" type.

    **In practice:** Kerberoasting extracts **service tickets**, and hashcat mode **13100** is the service-ticket (TGS-REP) type; AS-REP roasting is mode **18200**. TryHackMe's Attacking Kerberos room and HTB Academy's Hashcat module both confirm this. Mode numbers are not in the courseware text and are unlikely to be examined.

### Pass-the-ticket, silver and golden tickets

Tickets can be stolen and replayed just as hashes can: that is **pass-the-ticket**. Two forged tickets have names worth learning now; section 15 returns to them.

- A **silver ticket** is a forged *service ticket* for one service, made with that service account's hash.
- A **golden ticket** is a forged *TGT*, made with the hash of the special **KRBTGT** account, and is accepted for any user and any service in the domain.

!!! update "Updated: September 2023"
    **What changed.** The courseware and the official lab use **CrackMapExec** for spraying a password across a network. Its maintainer retired in **September 2023** and the remaining contributors continued the project under a new name, **NetExec** (command `nxc`). HTB Academy's Password Attacks module already teaches NetExec. Checked on the NetExec repository, 19 November 2026.

    **The exam still expects:** CrackMapExec by its old name.

!!! trap "Exam traps"
    - **Pass-the-hash needs no cracking.** If the question says the password was never recovered, think hash injection.
    - **LLMNR is 5355, NBT-NS is 137, both UDP.** Kerberos is 88.
    - **Golden is the TGT and KRBTGT; silver is one service.**
    - **Relay or poisoning.** Poisoning captures; relay forwards the capture to another server.

!!! stop "Where these notes stop: capturing and replaying credentials"
    **What is held back.** The commands that run the poisoner, relay a logon, read hashes from memory, request roastable tickets and pass a hash or ticket.

    **Where to read them in full.** **ECC e-book:** Gaining Access › Cracking Passwords, the pages on hash injection, LLMNR/NBT-NS poisoning, internal monologue, Kerberos cracking, pass-the-ticket and NTLM relay. **ECC Lab Manual:** Lab 1 Task 1 (Responder); the Active Directory lab, Tasks 2, 3 and 7. **TryHackMe:** Breaching Active Directory, the tasks on NTLM-authenticated services and authentication relays; Attacking Kerberos, the Rubeus and roasting tasks; Lateral Movement and Pivoting, the task on alternate authentication material; Credentials Harvesting. **HTB Academy:** Password Attacks, sections "Attacking SAM, SYSTEM, and SECURITY", "Attacking LSASS", "Pass the Hash (PtH)", "Pass the Ticket (PtT) from Windows" and "from Linux"; Active Directory Enumeration & Attacks, sections "LLMNR/NBT-NS Poisoning" and "Kerberoasting" (that module was read by its outline only).

!!! try "Practise it"
    **Official ECC lab:** Module 06, Lab 1 Task 1, "Perform Active Online Attack to Crack the System's Password using Responder"; the Active Directory lab (AS-REP roasting, password spraying, Kerberoasting). **TryHackMe:** Breaching Active Directory and Lateral Movement and Pivoting (network rooms that need a VPN connection); Attacking Kerberos and Credentials Harvesting (Premium); Attacktive Directory (free). **HTB Academy:** Password Attacks (Tier 0).

    On paper: for each of pass-the-hash, poisoning, relay, Kerberoasting and AS-REP roasting, write what the attacker must already have and what they end up with.

!!! recap "Recap: section 4"
    - Pass-the-hash reuses a stolen hash; nothing is cracked.
    - LLMNR (UDP 5355) and NBT-NS (UDP 137) poisoning captures NTLMv2 responses; Responder is the tool.
    - NTLM relay forwards a captured logon to another server; SMB signing stops it.
    - Kerberoasting targets service accounts; AS-REP roasting targets accounts without pre-authentication.
    - A golden ticket is a forged TGT from the KRBTGT hash; a silver ticket is for one service.

## 5. Offline cracking, salting and the tools {M}

Once hashes are in the attacker's hands, the target system is out of the picture. Speed now depends on the kind of hash and the hardware.

### Rainbow tables and salting {M: Rainbow table: precomputed hashes, a time-memory trade-off; offline. Salt: random value added to each password before hashing, so identical passwords give different hashes and precomputed tables fail}

A **rainbow table** is a very large precomputed list linking possible passwords to their hashes. Building it takes a long time once; using it is nearly instant. The courseware calls this a time-memory trade-off and names the `rtgen` program from RainbowCrack as the table generator.

```diagram m06-salt
Why a salt defeats a precomputed table: the same password no longer gives the same hash.
```

**Salting** defeats the table. A random value, the salt, is added to each password before hashing and stored beside the hash. Two users with the same password now have different hashes, and a table built without the salt matches nothing. The salt is not a secret; its job is to make precomputation useless. Windows LM and NT hashes are **not** salted, which is why they are the classic rainbow-table targets.

A **distributed network attack (DNA)** spreads cracking across many machines: a manager hands out portions of the key space and clients work on them with spare processor time.

### Tools the courseware names

| Purpose | Tools |
| --- | --- |
| Extract hashes | pwdump7, Mimikatz, DSInternals |
| Crack hashes | L0phtCrack, hashcat, John the Ripper, RainbowCrack |
| Guess against live services | THC-Hydra, Patator, Metasploit |
| Identify a hash type | hashID |
| Recover passwords for forensics | Elcomsoft Distributed Password Recovery, Passware Kit Forensic, PCUnlocker |
| Default password lists | cirt.net, routerpasswords.com and similar sites |

!!! update "Updated: October 2021"
    **What changed.** The courseware presents **L0phtCrack** as a current password auditing product. Its owners stopped selling it on 1 July 2021 and released it as open source on **17 October 2021**; version 7.2.0 from that date is the last release. Checked on l0phtcrack.gitlab.io, 19 November 2026.

    **The exam still expects:** L0phtCrack as a tool that audits passwords with dictionary, hybrid, rainbow-table and brute-force attacks.

### Hashcat masks {M: Hashcat mask charsets: ?l lower, ?u upper, ?d digit, ?s symbol, ?a all of those, ?h hex lower, ?H hex upper, ?b any byte. -m hash type, -a attack mode (0 wordlist, 3 mask)}

Hashcat describes a pattern with one placeholder per character. The courseware prints the set, and it is easy to examine.

| Placeholder | Stands for |
| --- | --- |
| `?l` | a lower-case letter |
| `?u` | an upper-case letter |
| `?d` | a digit |
| `?s` | a symbol |
| `?a` | any of the four above |
| `?h` / `?H` | a hexadecimal digit, lower or upper case |
| `?b` | any byte value |

So `?l?l?l?d?d?d` means three lower-case letters followed by three digits. The option `-m` selects the hash type and `-a` the attack mode: 0 for a wordlist, 3 for a mask.

!!! cpent "CPENT depth: what working crackers know beyond the courseware"
    None of this is in the CEH text. It comes from HTB Academy's Password Attacks and Cracking Passwords with Hashcat modules and TryHackMe's Password Cracking room.

    - **The hash type decides the time.** On the same hardware a fast hash such as MD5 or NT is tried millions of times a second; a deliberately slow one such as **bcrypt** or **Argon2** only thousands. Windows cached domain logons (the DCC2 format) crack about 800 times more slowly than NT hashes and cannot be passed.
    - **Identify first.** A 32-character hexadecimal string could be MD5 or NT; where it came from settles it. Modern Linux marks the algorithm at the start of the hash: `$6$` is SHA-512 and `$y$` is **yescrypt**, now the default on Debian and others.
    - **John the Ripper has three modes:** single (guesses from the user's own name and details), wordlist, and incremental (brute force guided by statistics). Helper programs with names ending in `2john` turn a protected ZIP, PDF, Office file or SSH key into a crackable hash.
    - **Rules beat bigger lists.** A small targeted list (the company name, the season, the year) with a rule set usually beats a huge generic one.
    - **Hashcat moves on.** The practice modules were written for version 6; hashcat.net showed version 8.0.0, released 25 October 2026, when checked on 19 November 2026.

!!! try "Practise it"
    **Official ECC lab:** Lab 1 Task 1 cracks a captured hash with John the Ripper; the Active Directory lab cracks with John and hashcat. **TryHackMe:** John the Ripper: The Basics (Premium); Password Cracking (Premium). **HTB Academy:** Cracking Passwords with Hashcat (Tier II, free to unlock); Password Attacks, sections "Introduction to John The Ripper", "Introduction to Hashcat" and "Writing Custom Wordlists and Rules".

    Examples, not run. Safe on your own machine: make a hash of a made-up word and see what a tool thinks it is.

    ```bash
    echo -n 'Winter2026' | sha256sum     # a fingerprint of a made-up password
    hashid '5f4dcc3b5aa765d61d8327deb882cf99'   # ask what kind of hash a string looks like
    ```

!!! recap "Recap: section 5"
    - A rainbow table trades storage for time and works offline.
    - A salt makes every hash unique, so precomputed tables fail.
    - LM and NT hashes are unsalted.
    - Hashcat mask placeholders: `?l ?u ?d ?s ?a ?h ?H ?b`.
    - L0phtCrack, hashcat, John the Ripper and RainbowCrack crack; pwdump7 and Mimikatz extract.

## 6. Defending against password attacks {U}

The courseware gives a long list of countermeasures. Grouped, they come to five ideas.

| Idea | What the courseware lists |
| --- | --- |
| Make passwords hard to guess | Eight to twelve characters or more with mixed character types; no dictionary words or personal details; no reuse; change default passwords |
| Store and send them safely | Never in clear text; salt and hash with bcrypt, Argon2 or PBKDF2; no clear-text protocols; encrypt the password database |
| Limit guessing | Account lockout after failed attempts; CAPTCHA and multi-factor authentication; rename the administrator account; restrict by location |
| Watch for attacks | Audit passwords; monitor logs for failed logons; check for leaked passwords; intrusion detection |
| Retire old mechanisms | Disable LM and, where possible, NTLM; enable SYSKEY; set a BIOS password |

!!! update "Updated: July 2025"
    **What changed.** The courseware says to "set the password change policy to 30 days". The US standards body NIST published **SP 800-63B revision 4** as final in **July 2025**. It says verifiers *shall not* require periodic password changes and *shall* force a change only when there is evidence of compromise; it asks for a minimum of eight characters, recommends fifteen, forbids composition rules and requires new passwords to be checked against a list of known-bad ones. HTB Academy's Password Attacks module teaches the newer view. Checked on pages.nist.gov, 19 November 2026.

    **The exam still expects:** regular password changes (the courseware's figure is 30 days) and mixed character types as good practice.

### Stopping name-resolution poisoning {M: Disable LLMNR: Group Policy › Computer Configuration › Administrative Templates › Network › DNS Client › "Turn off multicast name resolution" = Enabled. Disable NBT-NS: adapter › TCP/IPv4 › Advanced › WINS › "Disable NetBIOS over TCP/IP"}

Both protocols can simply be turned off, and the courseware gives the exact path for each. It adds: enforce SMB signing, watch UDP ports 5355 and 137, and watch for new services being installed (Windows event IDs 4697 and 7045). Detection tools named: Vindicate, Respounder and got-responded.

### Defending SMB

The courseware's advice is to disable SMB version 1, patch, segment the network, lock out repeated failures and give accounts the least privilege they need.

!!! exam "Exam answer / In practice"
    **Exam answer:** one line in the courseware groups "SMBv2" with SMBv1 as an old, vulnerable version to switch off.

    **In practice:** SMBv1 is the version to remove; SMBv2 and SMBv3 are what current Windows uses, and switching them off breaks file sharing. Treat the SMBv2 mention as a slip.

!!! hospital "Worked example: one typing mistake on a ward"
    A nurse on a ward workstation mistypes the name of the shared drive that holds the duty rota. Nothing seems to happen; she retypes it and carries on.

    1. **What happened underneath.** DNS did not know the mistyped name, so the workstation asked the ward network through LLMNR. A laptop that an intruder had plugged into a spare wall socket answered, and recorded her logon response (section 4).
    2. **Why it mattered.** Her password was the hospital name and the year. It cracked offline within the hour (section 5).
    3. **How it grew.** Her account could reach the nursing shares. On one of them sat a spreadsheet of equipment logins. One of those worked on a server where an administrator had logged on (sections 4 and 10).
    4. **What would have stopped it.** LLMNR and NBT-NS switched off by Group Policy; network sockets that refuse unknown devices; a password checked against a banned list; a second factor; administrators who never log on to ordinary servers.
    5. **What to ask afterwards.** Not "who mistyped?" but "why did a typing mistake leak a credential?"

    The same chain fits a school staff room, a law firm's reception desk or a factory office: any place with shared drives, wall sockets and people in a hurry.

!!! try "Practise it"
    **Official ECC lab:** none for this section. **TryHackMe:** Breaching Active Directory, the mitigations task. **HTB Academy:** Password Attacks, sections "Password Policies" and "Password Managers"; Introduction to Active Directory, section "Security in Active Directory".

    On paper: write a five-line password policy for a small clinic that follows the 2025 NIST guidance, then mark which lines the exam's answer would disagree with.

!!! recap "Recap: section 6"
    - Strong, unique, salted, never in clear text, with lockout and a second factor.
    - The exam expects periodic changes (30 days) and SYSKEY; current guidance has dropped both.
    - LLMNR is disabled through the DNS Client policy; NBT-NS through the adapter's WINS tab.
    - SMB signing stops relays; SMBv1 should be off.
    - Event IDs 4697 and 7045 record a new service being installed.

## 7. Exploiting vulnerabilities, and the Metasploit Framework {M}

The second way in is a flaw in software rather than a weak password. An **exploit** is code that uses a flaw; a **payload** is the code the attacker wants to run once the flaw has been used.

### The seven steps {M: Vulnerability exploitation steps: 1 identify the vulnerability, 2 determine the risk, 3 determine the capability, 4 develop the exploit, 5 select the delivery method (local or remote), 6 generate and deliver the payload, 7 gain remote access}

```diagram m06-exploit
The seven steps of exploiting a vulnerability, as the courseware orders them.
```

The courseware names four places to look up known exploits: **Exploit-DB**, **VulDB**, **OSV** (osv.dev, for open-source packages) and **MITRE CVE** (cve.org). It also names Packet Storm, whose old address now redirects to packetstorm.news (seen live on 19 November 2026). A **proof of concept** is exploit code published to show that a flaw is real; if it appears before a fix exists, attackers use it as a **zero-day**.

**WES-NG** (Windows Exploit Suggester, Next Generation) compares the list of updates installed on a Windows machine, taken from the output of the `systeminfo` command, with the known flaws and reports which are unpatched.

### Metasploit module types {M: Metasploit modules: exploit, payload (singles, stagers, stages), auxiliary (scanners, fuzzers, DoS), NOPs, encoders, evasion, post}

The **Metasploit Framework** is a toolkit that stores exploits and payloads as interchangeable parts called **modules**.

| Module type | What it is for |
| --- | --- |
| **Exploit** | Uses one specific flaw to deliver a payload |
| **Payload** | What runs on the target afterwards |
| **Auxiliary** | Anything that is not an exploit: scanners, fuzzers, denial-of-service tests |
| **NOPs** | Padding instructions that do nothing, used to keep a payload's size and position steady |
| **Encoders** | Rewrite a payload so that it avoids certain bytes or simple signatures |
| **Evasion** | Build files intended to slip past antivirus |
| **Post** | Run after access is gained: gather information, collect credentials, set up routes |

Payloads come in three kinds. A **single** is complete in itself. A **stager** is tiny: it only opens a connection back. A **stage** is the larger part the stager then downloads, such as **Meterpreter**, an in-memory agent with its own commands. The courseware's five steps for using an exploit module are: configure the exploit, check its options, select a target, select a payload, launch.

!!! exam "Exam answer / In practice"
    **Exam answer:** three payload kinds (singles, stagers, stages); an example auxiliary module that begins `class Metasploit3`.

    **In practice:** current Metasploit also lists a fourth payload folder, **adapters**, which wrap a single payload in another format (TryHackMe's Metasploit: Introduction room shows it). In a payload's name, an underscore means a single and a slash means stager plus stage. Modules have been written as `class MetasploitModule` for years; `Metasploit3` is the old form. Meterpreter traffic has been encrypted end to end since Metasploit 6 (August 2020), and the old Mimikatz extension was replaced by one called Kiwi.

### Bind and reverse connections

A remote shell needs one side to listen and the other to connect. In a **bind** shell the target listens and the attacker connects in, which a firewall usually blocks. In a **reverse** shell the attacker listens and the target connects out, which firewalls often allow because it looks like ordinary outbound traffic. Module 7 used the same idea for Trojans.

### AI-assisted exploitation

The courseware names two research tools: **Nebula**, which turns plain-language requests into tool commands, and **DeepExploit**, which uses machine learning to choose and launch Metasploit exploits. The official AI lab uses **ShellGPT** to write commands for payloads, a login-guessing run and a steganography tool.

!!! coasp "COASP link: when an assistant writes the commands"
    This is where the CEH syllabus meets the COASP one, from the operator's side.

    - **The model does not know your scope.** An assistant will write a command for any address it is given. The written authorisation is the tester's job, not the tool's.
    - **Generated commands are untested commands.** Read each one before running it, exactly as you would a script from a stranger.
    - **Prompts and outputs are data that leaves the room.** Target names, addresses and captured hashes typed into a hosted assistant have been disclosed to a third party. Client contracts often forbid that.

!!! stop "Where these notes stop: shells and payloads"
    **What is held back.** The one-line commands that open bind and reverse shells, the commands that build payload files, listener set-up, and shell stabilisation tricks.

    **Where to read them in full.** **ECC e-book:** Gaining Access › Vulnerability Exploitation, the Metasploit pages. **ECC Lab Manual:** Lab 1 Task 2, "Gain Access to a Remote System using Reverse Shell Generator"; Lab 2 and Lab 3 Task 2 for payload files; the AI lab. **TryHackMe:** What the Shell? (Premium), tasks 4 to 11; Metasploit: Exploitation (Premium), the msfvenom task; Metasploit: Meterpreter (Premium). **HTB Academy:** Shells & Payloads (Tier 0), sections "Bind Shells", "Reverse Shells", "Crafting Payloads with MSFvenom", "Infiltrating Windows", "Infiltrating Unix/Linux" and "Spawning Interactive Shells" (the first ten of its seventeen sections were read; the rest by title); Using the Metasploit Framework (Tier 0), sections "Payloads" and "Introduction to MSFVenom".

!!! try "Practise it"
    **Official ECC lab:** Lab 1 Task 2 (reverse shell generator). **TryHackMe:** Metasploit: Introduction (free), then Metasploit: Exploitation and Metasploit: Meterpreter (Premium); Blue (free), the classic MS17-010 "EternalBlue" exercise. **HTB Academy:** Using the Metasploit Framework (Tier 0).

    Example, not run. On a Windows machine you own, this is the input WES-NG works from:

    ```bash
    systeminfo > systeminfo.txt
    ```

!!! recap "Recap: section 7"
    - Seven steps: identify, risk, capability, develop, delivery method, payload, remote access.
    - Exploit sites: Exploit-DB, VulDB, OSV, MITRE CVE.
    - Metasploit modules: exploit, payload, auxiliary, NOPs, encoders, evasion, post.
    - Payloads: singles, stagers, stages. Meterpreter is a stage.
    - Bind: the target listens. Reverse: the target connects out.

## 8. Buffer overflows {M}

A **buffer** is a fixed-size block of memory set aside for some data. A **buffer overflow** happens when a program copies in more data than the block can hold and the extra spills over whatever sits next to it. If the attacker controls the extra, they can change what the program does next.

Programs are vulnerable when they do not check lengths: older languages such as C leave the check to the programmer, and functions that copy until they meet an end marker will copy as much as they are given.

### Stack and heap {M: Stack: LIFO, static memory; registers EBP (base of stack frame), ESP (top of stack), EIP (next instruction to run). Heap: dynamic memory, malloc(). Overwriting the saved return address gives control of EIP}

| | Stack | Heap |
| --- | --- | --- |
| Used for | Local variables and return addresses of functions | Memory requested while the program runs |
| Order | Last in, first out (PUSH and POP) | No fixed order; requested with `malloc()` and released with `free()` |
| An overflow overwrites | The saved return address | Pointers and bookkeeping data of neighbouring blocks |
| Exploiting it | Predictable | Less consistent |

Three processor registers matter. **EBP** points to the base of the current function's part of the stack, **ESP** to its top, and **EIP** holds the address of the next instruction to run.

```diagram m06-stack
A stack overflow: input longer than the buffer overwrites the saved return address.
```

When a function finishes, the processor loads the saved return address into EIP. Overwrite that address and the attacker chooses where execution goes.

### The eight steps of a Windows buffer overflow {M: Windows buffer overflow steps: 1 spiking, 2 fuzzing, 3 identify the offset, 4 overwrite the EIP, 5 identify bad characters, 6 identify the right module, 7 generate shellcode, 8 gain root access}

```diagram m06-bof
The eight steps of a Windows buffer overflow, from finding the weak command to running code.
```

| Step | Meaning |
| --- | --- |
| 1. **Spiking** | Send odd input to each command the program accepts to find one that crashes |
| 2. **Fuzzing** | Send that command steadily longer input to find roughly how many bytes cause the crash |
| 3. **Identify the offset** | Send a non-repeating pattern and read which part landed in EIP: that gives the exact position |
| 4. **Overwrite the EIP** | Confirm control by placing a chosen value at that position |
| 5. **Identify bad characters** | Find byte values the program alters or stops at, so the final code avoids them |
| 6. **Identify the right module** | Find a loaded library without memory protections that contains a "jump to the stack" instruction |
| 7. **Generate shellcode** | Produce the payload, avoiding the bad characters |
| 8. **Gain root access** | Send it all and receive a shell |

The official lab practises this on a deliberately weak program (vulnserver) inside a debugger (Immunity Debugger, with the mona add-on).

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware calls EIP "read-only" and its worked example crashes the program at about 2,300 bytes, with the offset found at 2,003.

    **In practice:** "read-only" means a program cannot write to EIP directly; overflowing the return address is exactly how its value gets changed. The Lab Manual's own numbers differ from the e-book (it reports the crash at about 10,200 bytes in one place and 5,100 in another); only the *method* is examinable, not the byte counts.

### Getting round the protections

| Term | Meaning |
| --- | --- |
| **DEP** (Data Execution Prevention) | Marks data areas such as the stack as non-executable |
| **ASLR** (Address Space Layout Randomization) | Loads programs and libraries at different addresses each run |
| **ROP** (return-oriented programming) | Reuses short pieces of existing code, each ending in a return, instead of injecting new code; gets round DEP and code signing |
| **Heap spraying** | Fills the heap with many copies of the payload so that a wild jump is likely to land on one |
| **JIT spraying** | Makes a script engine's just-in-time compiler emit predictable code; aimed at both ASLR and DEP |
| **Exploit chaining** | Uses several weaknesses in sequence, each one enabling the next |

### Detecting and preventing overflows

Detection tools named: OllyDbg, Veracode, Flawfinder, Kiuwan, Splint and Valgrind. Defences: validate input length; use safer functions (`strncpy`, `strncat`, `snprintf`); compile with stack canaries and bounds checking; enable DEP, ASLR and SEHOP; use the processor's NX bit; prefer languages that check bounds; review code with static and dynamic analysis.

!!! remember "Remember"
    **"Some Fools Insist On Bad Manners, Shouting Rudely":** Spiking, Fuzzing, Identify offset, Overwrite EIP, Bad characters, Module, Shellcode, Root.

!!! trap "Exam traps"
    - **Spiking comes before fuzzing.** Spiking finds *which* command is weak; fuzzing finds *how many* bytes.
    - **DEP stops execution; ASLR hides addresses.** ROP answers DEP; spraying answers ASLR.
    - **EIP, not ESP,** decides what runs next.

!!! stop "Where these notes stop: the overflow exercise"
    **What is held back.** The spike templates, the fuzzing and exploit scripts, the pattern and shellcode commands, and the debugger commands.

    **Where to read them in full.** **ECC e-book:** Gaining Access › Vulnerability Exploitation, "Windows Buffer Overflow Exploitation". **ECC Lab Manual:** Lab 1 Task 3, "Perform Buffer Overflow Attack to Gain Access to a Remote System". **TryHackMe:** none on the practice map for this topic. **HTB Academy:** Stack-Based Buffer Overflows on Windows x86 (Tier 0), the sections on fuzzing parameters, controlling EIP, bad characters, the return instruction and jumping to shellcode; Stack-Based Buffer Overflows on Linux x86 (Tier 0), the sections from taking control of EIP to the return address. Both modules were read by outline only.

!!! try "Practise it"
    **Official ECC lab:** Lab 1 Task 3 (vulnserver and Immunity Debugger). **TryHackMe:** none on the practice map. **HTB Academy:** the two Stack-Based Buffer Overflows modules (Tier 0; last updated 2020 and 2021).

    On paper: put these in order and say what each finds: bad characters, offset, fuzzing, spiking, module.

!!! recap "Recap: section 8"
    - An overflow writes past a buffer; on the stack it reaches the saved return address.
    - EBP is the base, ESP the top, EIP the next instruction.
    - Eight steps: spiking, fuzzing, offset, overwrite EIP, bad characters, module, shellcode, root.
    - DEP makes the stack non-executable; ASLR randomises addresses; ROP and spraying are the bypasses.
    - Defences: check lengths, safer functions, canaries, DEP and ASLR.

## 9. Mapping Active Directory after getting in {R}

With one domain account, an intruder can read most of the directory: every user, group, computer and policy. The courseware places this "post-AD enumeration" inside the exploitation section and names three tool families. Recognise each and what it shows.

| Tool | What it does |
| --- | --- |
| **BloodHound** | Collects directory data and draws it as a graph, showing the chains of group memberships and rights that lead from an ordinary account to a domain administrator |
| **PowerView** | A PowerShell script whose commands list domain objects |
| **GhostPack** | A collection of C# tools: **Seatbelt** (host security checks), SharpUp, SharpRoast, SharpDump, SafetyKatz, SharpWMI |

The courseware spends ten tables on PowerView command names. The pattern is enough: the name says what is listed.

| PowerView command family | Lists |
| --- | --- |
| `Get-NetDomain`, `Get-DomainSID`, `Get-DomainPolicy`, `Get-NetDomainController` | The domain, its identifier, its password policy and its controllers |
| `Get-NetUser`, `Get-NetLoggedon`, `Get-NetSession` | Users, who is logged on, open sessions |
| `Get-NetComputer` | Computers, with filters for operating system |
| `Get-NetGroup`, `Get-NetGroupMember`, `Get-NetLocalGroup` | Groups and their members |
| `Invoke-ShareFinder`, `Get-NetShare`, `Invoke-FileFinder` | Shared folders and interesting files |
| `Get-NetGPO`, `Get-NetOU` | Group Policy objects and organisational units |
| `Get-ObjectAcl`, `Invoke-ACLScanner` | Access control lists: who has rights over what |
| `Get-NetForest`, `Get-NetForestDomain` | Forests and trusts between domains |

A **forest** contains trees, and a tree contains domains. In a **one-way trust**, users of the trusted domain can reach resources in the trusting domain; a two-way trust works in both directions.

!!! exam "Exam answer / In practice (as checked in November 2026)"
    **Exam answer:** BloodHound is a desktop application built on Electron and Linkurious with a Neo4j database, which uses graph theory to reveal attack paths in Active Directory.

    **In practice:** that version is now "BloodHound Legacy"; its makers mark it deprecated and no longer maintained. The current **BloodHound Community Edition** is a web application with a browser interface, a PostgreSQL database and a Neo4j graph database; its collectors are still SharpHound and AzureHound. TryHackMe's Post-Exploitation Basics room also still teaches the legacy version. The makers' pages give no month for the change (2023). Checked on the SpecterOps repositories.

!!! update "Updated: January 2021"
    **What changed.** PowerView belongs to the **PowerSploit** collection, which its owners archived on **21 January 2021** with the note that the project is no longer supported. It still runs, and the official lab still uses it, but antivirus flags it on sight and newer forks renamed many commands from `Get-Net…` to `Get-Domain…`. Checked on the PowerSploit repository, 19 November 2026; the renaming was not checked.

    **The exam still expects:** the `Get-Net…` names in the courseware tables.

Outside the courseware, HTB Academy's Introduction to Active Directory supplies the structure these tools walk over, and a working tester is expected to know it: five special domain controller roles (called FSMO roles), three group scopes (domain local, global, universal), the order in which Group Policy applies (local, site, domain, organisational unit), and the special **KRBTGT** account that signs every ticket.

!!! try "Practise it"
    **Official ECC lab:** the Active Directory lab, Task 4, "Perform Post-Enumeration using PowerView". **TryHackMe:** Active Directory Basics (Premium); Post-Exploitation Basics (free). **HTB Academy:** Introduction to Active Directory (Tier 0, read in full); Active Directory Enumeration & Attacks (Tier II, free to unlock, outline only).

    On paper: draw three groups nested inside each other and a user in the innermost. Which rights does the user inherit, and how would a graph make that obvious?

!!! recap "Recap: section 9"
    - Any domain user can read most of Active Directory.
    - BloodHound graphs the paths from ordinary accounts to administrators.
    - PowerView commands are named for what they list: users, groups, computers, shares, policies, trusts.
    - Seatbelt, from GhostPack, runs security checks on a host.
    - A forest holds trees; a tree holds domains; trusts can be one-way or two-way.

## 10. Escalating privileges {M}

The first account an intruder gets is usually an ordinary one. **Privilege escalation** is the second phase: using a design flaw, a programming error or a careless setting to gain rights the account was never given.

### Horizontal and vertical {M: Privilege escalation: horizontal = take over another user at the same level; vertical = gain higher rights (administrator, root, SYSTEM)}

- **Horizontal** escalation takes over another account at the *same* level: one online-banking customer reading another customer's account.
- **Vertical** escalation gains a *higher* level: a standard user becoming an administrator.

### The techniques, by name

The courseware lists about thirty. The exam describes one and asks for its name, so learn each with its one-line meaning.

**Windows: libraries and programs that load the wrong thing**

| Technique | Meaning |
| --- | --- |
| **DLL hijacking** | A program asks for a library without giving its full path; Windows searches the program's own folder first, so a malicious library planted there is loaded instead |
| **Unquoted service path** | A service's path contains spaces and no quotation marks; Windows tries each partial path, so a program planted at one of them runs with the service's rights |
| **Service object permissions** | A user is allowed to reconfigure a service and points it at their own program |
| **Path interception** | General name for the three above: search-order hijacking, unquoted paths and a misconfigured PATH variable |
| **File system permission weakness** | A service's program file is writable by ordinary users and is replaced |
| **Unattended installs** | Set-up answer files (`Unattend.xml`) left on disk still contain an administrator password |
| **Modifiable registry autoruns** | A start-up entry points to a program an ordinary user can replace |
| **MSI abuse** | A Windows Installer "repair" runs as SYSTEM and can be made to run the attacker's custom action |
| **Application shimming** | The compatibility layer for old programs is used to redirect or inject code |
| **COM hijacking** | A per-user registry entry for a component is read before the system-wide one, so the user's version loads |

**Windows: tokens, identities and built-in features**

| Technique | Meaning |
| --- | --- |
| **Named pipe impersonation** | A service that a privileged client connects to can act with that client's identity; the basis of Metasploit's `getsystem` |
| **Access token manipulation** | Copying or forging the token that records a logged-on user's identity |
| **Parent PID spoofing** | Starting a process so that it appears to be the child of a trusted system process |
| **UAC bypass** | Running elevated without the User Account Control prompt, typically by planting a per-user registry entry that a trusted auto-elevating program reads (the lab uses the `fodhelper` and Event Viewer variants) |
| **Accessibility features** | Replacing a program reachable from the logon screen, such as Sticky Keys (`sethc.exe`), with a command prompt |
| **SID-History injection** | Adding an administrator's identifier to an account's migration-history attribute |
| **Scheduled tasks** | Creating or altering a task that runs with higher rights |
| **Boot or logon scripts** | Scripts that run automatically at start-up or logon |
| **NoFilter** | Abuse of the Windows Filtering Platform on Windows 11 to duplicate a SYSTEM token |

**Linux and macOS**

| Technique | Meaning |
| --- | --- |
| **SUID and SGID abuse** | A program marked to run as its owner (often root) offers a way to run other commands |
| **Sudo rights** | The `sudoers` file lets a user run some program as root, and that program can be turned to other uses |
| **Cron jobs** | A scheduled job run by root uses a script an ordinary user can edit |
| **Kernel exploits** | An unpatched flaw in the operating system core |
| **"." in PATH** | The current folder is searched for commands, so a planted file named like a common command runs |
| **NFS misconfiguration** | A network file share (port 2049) lets a remote user plant files that run with high rights |
| **ptrace injection** | Using the debugging interface to write code into a running process |
| **Dylib hijacking** (macOS) | The macOS equivalent of DLL hijacking |
| **Launch daemons and plist modification** (macOS) | Altering the files that tell macOS what to start |
| **Setuid, web shells** | Listed without detail: a privileged program flag, and a script planted on a web server |

**Hardware**

| Technique | Meaning |
| --- | --- |
| **Spectre** | Abuses speculative execution and branch prediction to read memory a program should not see |
| **Meltdown** | Lets an ordinary program read kernel memory through the processor's out-of-order execution |

Tools named: BeRoot, pwncat, PowerSploit, Traitor, PEASS-ng (WinPEAS and LinPEAS), FullPowers, and Linux Privilege Checker.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware shows the NFS attack only as a sequence of screenshots: find the share, mount it, copy a shell onto it, log in.

    **In practice:** the setting that makes it work has a name, **`no_root_squash`**. Normally a file server treats a remote root user as nobody; with that option it trusts them as root. TryHackMe's Linux Privilege Escalation room teaches it by name.

!!! exam "Exam answer / In practice (as checked in November 2026)"
    **Exam answer:** `at` and `schtasks` are the Windows scheduling tools; login hooks and Startup Items are macOS start-up points.

    **In practice:** Microsoft's page for `at` (updated 21 October 2026) says the command has been deprecated since Windows 8 and Windows Server 2012 in favour of `schtasks`, and is removed in current preview builds of the next Windows release. Apple's developer documentation, last updated in 2016, calls login hooks "a deprecated technology" and points to `launchd` instead. Checked on learn.microsoft.com and developer.apple.com.

!!! cpent "CPENT depth: escalation paths the courseware leaves out"
    These come from TryHackMe's Linux and Windows Privilege Escalation rooms and the outline of the two HTB Academy privilege escalation modules. A working tester is expected to know them.

    - **Linux capabilities.** Root's powers can be granted to a program one at a time. A search for SUID files does not find them; a separate check does.
    - **`LD_PRELOAD`.** If `sudo` is set to keep this environment variable, a user can make a root program load their own library first.
    - **GTFOBins.** A public catalogue of ordinary Unix programs and the ways each can be misused when it runs with extra rights.
    - **Dangerous Windows privileges.** An account holding **SeImpersonate** (most service accounts), **SeBackup** or **SeTakeOwnership** can usually reach SYSTEM. The tools that abuse SeImpersonate are known as the "potato" family.
    - **Where Windows passwords are left lying.** PowerShell's command history file, saved credentials listed by `cmdkey`, web application configuration files.
    - **Enumeration scripts.** WinPEAS and LinPEAS (in the courseware), plus PrivescCheck and Metasploit's local exploit suggester.

!!! remember "Remember"
    **Horizontal is sideways to a peer; vertical is up to the boss.**

!!! trap "Exam traps"
    - **DLL hijacking or unquoted path.** A missing *library path* is DLL hijacking; a missing *quotation mark* around a service path is the other.
    - **Sticky Keys appears twice:** as privilege escalation (accessibility features) and as persistence (section 15).
    - **Spectre and Meltdown are processor flaws,** not operating system bugs.

!!! stop "Where these notes stop: escalation commands"
    **What is held back.** The enumeration one-liners, the UAC-bypass module steps, and the commands that plant files or reconfigure services.

    **Where to read them in full.** **ECC e-book:** Escalating Privileges, the whole section; its Tables 6.12 to 6.14. **ECC Lab Manual:** Lab 2 Task 1, "Escalate Privileges by Bypassing UAC and Exploiting Sticky Keys"; the Active Directory lab, Task 6. **TryHackMe:** Linux Privilege Escalation (free), tasks on kernel exploits, sudo, SUID, capabilities, cron, PATH and NFS; Windows Privilege Escalation (Premium), tasks on harvesting passwords, quick wins, service misconfigurations and dangerous privileges. **HTB Academy:** Linux Privilege Escalation and Windows Privilege Escalation (both Tier II, free to unlock; read by outline only).

!!! try "Practise it"
    **Official ECC lab:** Lab 2 Task 1. **TryHackMe:** Linux Privilege Escalation (free); Windows Privilege Escalation (Premium). **HTB Academy:** Linux Privilege Escalation (28 sections) and Windows Privilege Escalation (33 sections).

    Examples, not run. Two harmless checks an administrator uses to audit their own machines:

    ```bash
    whoami /priv                              # Windows: which privileges does this session hold?
    find / -perm -u=s -type f 2>/dev/null     # Linux: list programs that run as their owner
    ```

!!! recap "Recap: section 10"
    - Horizontal: another account at the same level. Vertical: a higher level.
    - Windows favourites: DLL hijacking, unquoted service paths, weak service permissions, UAC bypass, named pipe impersonation.
    - Linux favourites: SUID programs, sudo rights, cron jobs, kernel exploits, NFS.
    - Spectre and Meltdown read memory through processor behaviour.
    - Tools: BeRoot, PEASS-ng, pwncat, Traitor, PowerSploit.

## 11. Moving through the network, and defending against escalation {U}

### Pivoting and relaying {M: Pivoting: use a compromised host to attack other systems it can reach. Relaying: reach resources through the compromised host so requests appear to come from it}

A compromised machine usually sits on networks the attacker cannot reach directly. The courseware separates two uses of it.

| | Pivoting | Relaying |
| --- | --- | --- |
| Purpose | **Attack** other systems from the compromised host | **Access** resources on other systems through it |
| Steps in the courseware | Find live hosts; add a route through the session; scan ports; exploit | Set up port-forwarding rules; open the forwarded port locally |

The courseware does both with Meterpreter's routing and port-forwarding commands. The practice material adds other tunnels, all outside the courseware: SSH port forwarding, SOCKS proxies with proxychains, and the tools chisel and sshuttle.

### Escalation in a domain

| Technique | Meaning |
| --- | --- |
| **DCSync** | An account holding the directory's *replication* rights asks a domain controller to send password data, as another controller would. The right names begin "Replicating Directory Changes" |
| **Group Policy modification** | Editing a policy object so that every machine it applies to runs a task or grants a right |
| **Domain trust modification** | Changing the trust between domains to open a path |
| **AD CS abuse** | A badly designed certificate template lets an ordinary user request a certificate in an administrator's name (the courseware's example is the case known as ESC1) |

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware's DCSync defences include using "network surveillance tools such as Sean Metcalf and StealthDEFEND", and its certificate-abuse screenshot is captioned with the tool name "Certify" although the commands shown are for Certipy.

    **In practice:** Sean Metcalf is a well-known Active Directory security researcher, not a product. Certify (Windows) and Certipy (Python) are two different tools for the same job. Neither slip is likely to be examined.

### Defending against privilege escalation

The courseware's list, grouped:

| Idea | Measures |
| --- | --- |
| Least privilege | Run services as unprivileged accounts; separate administrator accounts; restrict interactive logon; remove unused accounts; time-limited and just-in-time rights |
| Hardening | Patch the kernel and applications; UAC set to "Always notify"; write-protect program folders and search paths; use full paths in code; block unneeded scheduling tools |
| Verification | Multi-factor authentication; code signing; application allow-listing; file integrity monitoring; audit access control lists |
| For `sudo` | Require the password every time; log its use |
| For DCSync | Track who holds replication rights; audit directory permissions |
| For DLL and dylib hijacking | Tools: Dependency Walker, DLL Hijack Audit Kit, DLLSpy, Dylib Hijack Scanner |
| For Spectre and Meltdown | Operating system, firmware and BIOS updates. Detection tools: InSpectre, Spectre & Meltdown Checker |

The practice material adds three defences that matter more than any in the list above for Windows networks, all outside the courseware: **LAPS**, which gives every machine a different, rotating local administrator password; **tiered administration**, meaning domain administrators log on only to domain controllers; and **group Managed Service Accounts**, whose long random passwords make Kerberoasting pointless.

!!! update "Updated: April 2023"
    **What changed.** The courseware mentions LAPS only as the name of one Seatbelt check. Microsoft built **Windows LAPS** into Windows itself with the updates of **11 April 2023**; the older add-on, "Microsoft LAPS", is deprecated from Windows 11 version 23H2 and its installer is blocked on newer versions. Checked on learn.microsoft.com (page updated 16 September 2026).

    **The exam still expects:** nothing specific on LAPS; know that shared local administrator passwords are what pass-the-hash feeds on.

!!! stop "Where these notes stop: pivoting and domain escalation"
    **What is held back.** Routing and port-forwarding commands, the replication request, certificate requests and policy edits.

    **Where to read them in full.** **ECC e-book:** Escalating Privileges, "Pivoting and Relaying", "Modifying Domain Policy", "DCSync Attack" and "Abusing Active Directory Certificate Services". **ECC Lab Manual:** no task covers these. **TryHackMe:** Lateral Movement and Pivoting, the port-forwarding task; Credentials Harvesting, the domain controller task; Attacktive Directory (free). **HTB Academy:** Pivoting, Tunneling, and Port Forwarding (Tier II; outline only); Active Directory Enumeration & Attacks, the DCSync and ACL sections (outline only); Password Attacks, section "Pass the Certificate" (read in full).

!!! try "Practise it"
    **Official ECC lab:** none for pivoting or DCSync. **TryHackMe:** Lateral Movement and Pivoting (network room). **HTB Academy:** Pivoting, Tunneling, and Port Forwarding (18 sections).

    On paper: a web server sits in a public zone and can reach a database server that the internet cannot. Draw the two machines and mark where a pivot and where a relay would run.

!!! recap "Recap: section 11"
    - Pivoting attacks onward from a compromised host; relaying reaches resources through it.
    - DCSync abuses replication rights to obtain password data from a domain controller.
    - Certificate-template and Group Policy mistakes can hand out domain-wide rights.
    - Defences: least privilege, patching, UAC at its strictest, allow-listing, audited permissions.
    - LAPS, tiered administration and managed service accounts are the practical fixes.

## 12. Maintaining access: running programs, keyloggers and spyware {M}

With high privileges the intruder "owns" the machine and starts running their own programs on it. The courseware calls this **executing applications** and lists what gets run: backdoors, password crackers, keyloggers and spyware.

### Running programs remotely {M: Remote execution: WMI over DCOM port 135; WinRM 5985 (HTTP) and 5986 (HTTPS); also service execution and exploitation for client execution. Tools: PsExec, Dameware}

| Technique | Meaning |
| --- | --- |
| **Exploitation for client execution** | A flaw in a browser, an office program or a document reader runs the attacker's code |
| **Service execution** | Creating or starting a Windows service through the Service Control Manager |
| **WMI** | Windows Management Instrumentation, reached over DCOM on port 135 |
| **WinRM** | Windows Remote Management, on port 5985 (HTTP) or 5986 (HTTPS) |

Tools named: Dameware Remote Support, PsExec, Pupy, PDQ Deploy, ManageEngine Endpoint Central. The courseware's heading above that list reads "privilege escalation tools"; they are remote administration tools.

!!! update "Updated: August 2026"
    **What changed.** Many of the courseware's command tables use **WMIC**, the old command-line front end to WMI. Microsoft deprecated it years ago and removed it from Windows 11 versions 24H2 and 25H2 with the **August 2026** update, and from version 26H1 in September; it can no longer be added back. WMI itself remains, used through PowerShell. Checked on support.microsoft.com (change log dated 29 September 2026).

    **The exam still expects:** `wmic` commands as a way to query and run things on local and remote Windows machines.

### Keyloggers {M: Keyloggers: hardware (PC/BIOS embedded, keylogger keyboard, external: PS/2 and USB, acoustic/CAM, Bluetooth, Wi-Fi) and software (application, kernel/rootkit/device driver, hypervisor-based, form-grabbing, JavaScript-based, memory-injection-based)}

A **keylogger** records what is typed. Many also capture screenshots, window titles, visited addresses and the clipboard.

| Kind | Types |
| --- | --- |
| **Hardware** | Embedded in the PC or its BIOS; a keyboard with a logger built in; **external** devices: PS/2 and USB plugs, acoustic or camera-based capture, Bluetooth, Wi-Fi |
| **Software** | Application; kernel, rootkit or device-driver; hypervisor-based; form-grabbing (reads web forms as they are submitted); JavaScript-based (a script in the page); memory-injection-based (alters the browser in memory) |

Hardware makers named: KeyGrabber, KeyCarbon, KeyGhost, KEYKatcher. Software named: Spyrix Personal Monitor (used in the official lab), REFOG, All In One Keylogger; for macOS, Hoverwatch and FlexiSPY. Metasploit's Meterpreter has its own keystroke capture.

### Spyware

**Spyware** watches a user and reports back without their knowledge. It arrives by piggybacking on other software, through a drive-by download, or by pretending to be anti-spyware. The courseware lists eleven types by what they watch: **desktop, email, internet, child-monitoring, screen-capturing, USB, audio, video, print, telephone or cellphone, and GPS** spyware. Tools named include Spytech SpyAgent and Spyrix; for phones, mSpy and FlexiSPY.

### Defences

| Against | Measures and tools |
| --- | --- |
| Keyloggers | Anti-keylogger software; an on-screen keyboard; a password manager that fills forms; one-time passwords and multi-factor authentication; host intrusion detection. Tools: Zemana AntiLogger, GuardedID, KeyScrambler, SpyShelter |
| Hardware keyloggers | Restrict physical access; inspect cables and ports; lock or disable unused USB ports |
| Spyware | Keep browser security settings high; an outbound firewall; do not work as an administrator; distrust "your computer is infected" pop-ups. Tools: SUPERAntiSpyware, Kaspersky, Malwarebytes, Avast |

!!! update "Updated: June 2024"
    **What changed.** The courseware recommends Kaspersky Total Security. On **20 June 2024** the US Department of Commerce prohibited Kaspersky from selling its software to US customers, and updates to US users stopped on 29 September 2024. The product is still sold elsewhere. Seen on the bis.gov press release through a search result, 19 November 2026; the page itself would not load.

    **The exam still expects:** Kaspersky as an anti-spyware and anti-rootkit vendor (its TDSSKiller appears in section 13).

!!! trap "Exam traps"
    - **Form-grabbing** captures data from a web form before it is encrypted and sent; it does not record every key.
    - **Acoustic and camera-based** loggers are *hardware*, external type.
    - **WinRM is 5985 and 5986; WMI over DCOM is 135.**

!!! try "Practise it"
    **Official ECC lab:** Lab 3 Task 1, "User System Monitoring and Surveillance using Spyrix". **TryHackMe:** Metasploit: Meterpreter (Premium); Lateral Movement and Pivoting, the tasks on spawning processes remotely and on WMI. **HTB Academy:** Password Attacks, section "Network Services" (WinRM, SSH, RDP and SMB).

    On paper: list everything connected between your keyboard and your computer. Where could a device be added without you noticing?

!!! recap "Recap: section 12"
    - Executing applications is part of maintaining access.
    - Remote execution: service execution, WMI (port 135), WinRM (5985 and 5986), client-side exploitation.
    - Keyloggers are hardware or software; six software types.
    - Eleven types of spyware, named for what they watch.
    - Defences: anti-keyloggers, on-screen keyboards, a second factor, physical checks.

## 13. Hiding files: rootkits and NTFS data streams {M}

The courseware gives three ways to hide files: rootkits, NTFS alternate data streams, and steganography (section 14).

### Rootkits

A **rootkit** is software that hides the intruder's presence and keeps privileged access. It does so by replacing or intercepting parts of the operating system, so that the tools an administrator would use to look for it give false answers. A typical kit bundles a backdoor, packet sniffers, log-wiping tools and sometimes programs for denial-of-service attacks.

### Types of rootkit {M: Rootkit types: hypervisor-level (Ring -1), hardware/firmware, kernel-level (Ring 0), boot-loader-level (bootkit), application/user-mode (Ring 3), library-level}

```diagram m06-rings
Where each type of rootkit sits, from the hardware up to ordinary applications.
```

| Type | Where it lives |
| --- | --- |
| **Hypervisor-level** | Beneath the operating system, which it turns into a guest virtual machine; uses the processor's virtualisation features. Called Ring -1 |
| **Hardware / firmware** | In device or platform firmware, which is not checked for integrity; survives reinstalling the operating system |
| **Kernel-level** | Inside the operating system core as a driver or loadable module. Ring 0 |
| **Boot-loader-level** | Replaces the boot loader, so it starts before the operating system. Also called a bootkit |
| **Application-level / user-mode** | Replaces ordinary program files or alters their behaviour. Ring 3 |
| **Library-level** | Alters system libraries so that the calls programs make return hidden results |

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware text says there are "six" types of rootkit.

    **In practice:** it then lists seven, adding **memory rootkits**, which live only in RAM and vanish at reboot. If a question asks how many, six is the stated number; if it describes a rootkit that leaves nothing on disk, "memory rootkit" is the term.

### How rootkits work, and examples

Three mechanisms are named. **System hooking** redirects a system call to the rootkit's own code. **Inline function hooking** overwrites the first bytes of a function in a core library. **Direct kernel object manipulation (DKOM)** edits the kernel's own lists, for instance unlinking a process so that it no longer appears.

Examples in the courseware: **FudModule** (used by the Lazarus group; exploited a Windows driver to reach the kernel and switch off security products), **Fire Chili** (delivered through the Log4Shell flaw), CopperStealer, Syslogk, Reptile and CosmicStrand (a firmware rootkit).

### Detecting rootkits {M: Rootkit detection methods: integrity-based, signature-based, heuristic/behaviour-based, runtime execution path profiling, cross-view-based, alternative trusted medium, memory dump analysis, virtualization-based}

| Method | Idea |
| --- | --- |
| **Integrity-based** | Compare current files and memory with a trusted baseline (Tripwire, AIDE) |
| **Signature-based** | Look for known rootkit fingerprints |
| **Heuristic / behaviour-based** | Look for deviations from normal behaviour |
| **Runtime execution path profiling** | Compare how many instructions a routine takes before and after; a hook adds steps |
| **Cross-view-based** | Ask the same question two ways, through the normal interface and by reading the raw data, and look for differences |
| **Alternative trusted medium** | Boot from clean media and inspect the disk from outside; the most reliable |
| **Memory dump analysis** | Capture RAM and examine it offline |
| **Virtualization-based** | Inspect the machine from the hypervisor |

Anti-rootkit tools named: GMER, Trellix Stinger, Kaspersky TDSSKiller, Malwarebytes Anti-Rootkit, Avast, AVG. Defences: reinstall from trusted media, verify checksums, enable Secure Boot, write-protect the BIOS, apply least privilege and allow-listing.

### NTFS alternate data streams {M: NTFS ADS: extra named stream attached to a file, written as file.ext:streamname; file size shown does not change; lost when copied to FAT. Detect with Sysinternals Streams, LADS, Stream Armor}

On the NTFS file system, a file can carry extra, named blocks of data called **alternate data streams (ADS)**. The ordinary contents are the unnamed stream; others are addressed as `filename:streamname`. Windows Explorer and a plain directory listing show only the main stream's size, so a stream of any size, even a program, can ride inside a small text file unnoticed. Only the file's modification time changes.

```diagram m06-ads
One file, two streams: the listing shows the size of the first only.
```

Streams exist only on NTFS: copying the file to a FAT-formatted drive strips them, which the courseware lists as a way to remove them. Detection tools named: Sysinternals **Streams**, **LADS**, Stream Armor, Stream Detector, ADS Scanner, AlternateStreamView and GMER. The courseware does not mention it, but Windows' own `dir /r` also lists them.

!!! trap "Exam traps"
    - **Kernel-level is Ring 0; hypervisor-level is below it; application-level is Ring 3.**
    - **Cross-view** compares two views of the same system; **integrity-based** compares now with a stored baseline.
    - **ADS does not change the visible file size.** It changes the modification time.

!!! try "Practise it"
    **Official ECC lab:** none. No task in the Module 06 Lab Manual covers rootkits or data streams. **TryHackMe:** none on the practice map. **HTB Academy:** none on the practice map.

    Examples, not run. Safe on an NTFS drive you own: attach a short note to a text file as a second stream, then list and read it.

    ```bash
    echo hidden note > notes.txt:extra.txt
    dir /r notes.txt
    more < notes.txt:extra.txt
    ```

!!! recap "Recap: section 13"
    - A rootkit hides the intruder by altering the operating system's own answers.
    - Types by depth: hypervisor, firmware, kernel, boot loader, library, application; the text adds memory.
    - Mechanisms: system hooking, inline function hooking, DKOM.
    - Eight detection methods; booting from trusted media is the most reliable.
    - An NTFS data stream hides data inside a file without changing its visible size.

## 14. Steganography and steganalysis {M}

**Steganography** hides the *existence* of a message by placing it inside something ordinary: a picture, a sound file, a document. Encryption makes a message unreadable; steganography makes it unnoticed. Attackers use it to carry stolen data out, or tools and instructions in, past inspection.

### Classification {M: Steganography: technical (invisible ink, microdots, computer-based) and linguistic (semagrams: visual, text; open codes: jargon codes, covered ciphers: null cipher, grille cipher). Computer-based techniques: substitution, transform domain, spread spectrum, statistical, distortion, cover generation}

```diagram m06-stego
The courseware's classification of steganography.
```

- **Technical steganography** uses physical or computing methods: invisible ink, **microdots** (a page shrunk to a dot about a millimetre across), and computer-based methods.
- **Linguistic steganography** hides the message in language itself. **Semagrams** use signs or symbols: *visual* (an arrangement of objects) or *text* (changes in font or spacing). **Open codes** hide meaning in an innocent-looking text: *jargon codes* (agreed words with secret meanings) and *covered ciphers*, which are **null ciphers** (the message is, say, the first letter of each word) and **grille ciphers** (a template with holes reveals the right letters).

Six **computer-based techniques**: **substitution** (replace unimportant bits of the cover), **transform domain** (hide in the mathematical transform of an image or sound), **spread spectrum**, **statistical**, **distortion** (the receiver compares with the original), and **cover generation** (create a cover specially to hold the message).

### What can be a cover

The courseware lists twelve media: image, document, folder, video, audio, white space, web, spam or email, natural text, hidden operating system, C++ source code, and compressed data.

| Medium | How | Tools named |
| --- | --- | --- |
| **Image** | **Least significant bit (LSB) insertion**: change the last bit of each colour value. **Masking and filtering**: alter brightness, like a watermark; survives compression. **Algorithms and transformation**: hide in the coefficients of a mathematical transform (DCT, wavelet) | OpenStego, StegOnline, Coagula, CryptaPix |
| **White space** | Spaces and tabs at line ends | Snow |
| **Document** | Hidden data in document structure | StegoStick, StegJ, SNOW |
| **Video** | In the picture transform of frames; large capacity | OmniHide Pro, OpenPuff |
| **Audio** | **Echo data hiding, spread spectrum, LSB coding, tone insertion, phase encoding**; or frequencies above about 20,000 Hz that people cannot hear | DeepSound, MP3Stego |
| **Folder** | Files hidden and encrypted inside a folder | GiliSoft File Lock Pro, Folder Lock |
| **Spam / email** | Message encoded as text that looks like junk mail | Spam Mimic |

The LSB method works because the last bit barely changes a colour. Three pixels, each with red, green and blue values, give nine bits to play with: enough to hide one eight-bit letter with no visible difference.

### Steganalysis {M: Steganalysis attacks: stego-only, known-stego, known-message, known-cover, chosen-message, chosen-stego, chi-square, distinguishing statistical, blind classifier}

**Steganalysis** is the reverse: detecting that a message is hidden and, if possible, recovering or destroying it. It is hard because a suspect file may hold nothing, the hidden data may be encrypted, and ordinary noise looks similar.

| Attack | The analyst has… |
| --- | --- |
| **Stego-only** | Only the suspect object |
| **Known-stego** | The algorithm, the original cover and the suspect object |
| **Known-message** | The hidden message and the suspect object |
| **Known-cover** | The original cover and the suspect object, to compare |
| **Chosen-message** | A tool that makes stego objects from messages of the analyst's choosing |
| **Chosen-stego** | The suspect object and the tool or algorithm that made it |
| **Chi-square** | A statistical test on the distribution of values |
| **Distinguishing statistical** | Statistics that separate the method used |
| **Blind classifier** | A detector trained on clean samples |

Detection tools named: **zsteg** (PNG and BMP), StegoVeritas, Stegextract, StegoHunt, Steganography Studio, Virtual Steganographic Laboratory.

!!! remember "Remember"
    **Cryptography hides the meaning; steganography hides the message.** A null cipher's message is in the *first letters*; a grille cipher needs a *template*.

!!! trap "Exam traps"
    - **Semagram or open code.** Semagrams use signs, symbols or layout; open codes use ordinary-looking words.
    - **Masking survives compression; LSB does not** survive lossy editing well.
    - **Known-cover** means the analyst has the *original* file to compare against.
    - **Snow is white space,** not images.

!!! try "Practise it"
    **Official ECC lab:** the AI lab's last prompts hide and recover a text file in a JPEG with steghide; no other task covers steganography. **TryHackMe:** none on the practice map. **HTB Academy:** none on the practice map.

    On paper: the letter H is 01001000 in binary. Take three pixels with any nine colour values, write each value in binary, and change only the last bit of the first eight to carry H. How many values actually changed?

!!! recap "Recap: section 14"
    - Steganography hides that a message exists.
    - Technical (ink, microdots, computer-based) and linguistic (semagrams, open codes).
    - Six computer-based techniques, starting with substitution and transform domain.
    - Image methods: LSB insertion, masking and filtering, algorithms and transformation.
    - Steganalysis has nine named attacks, from stego-only to blind classifier.

## 15. Persistence: on one machine and across a domain {R}

**Persistence** means surviving a reboot, a password change or a patch. The courseware covers host tricks first and then what it calls **domain dominance**.

### On one Windows machine

| Technique | Meaning |
| --- | --- |
| **Sticky Keys** | The accessibility program started by pressing Shift five times at the logon screen is swapped for a command prompt, which then opens as SYSTEM before anyone logs on |
| **Registry Run keys** | An entry under a `…\CurrentVersion\Run` key starts a program at every logon. The official lab notes that an entry's data is limited to 260 characters |
| **Startup folder** | A program or shortcut placed in a Startup folder runs at logon |
| **WMI event subscription** | Three linked WMI objects, an event filter, an event consumer and a binding between them, run a command whenever a chosen event occurs |

### Domain dominance {M: Domain dominance techniques: remote code execution, abusing DPAPI, malicious replication (DCSync), skeleton key, golden ticket, silver ticket}

| Technique | Meaning |
| --- | --- |
| **Remote code execution** | Running commands on the domain controller with administrator rights |
| **Abusing DPAPI** | The Data Protection API encrypts users' stored secrets; the domain controller holds a backup key that can unlock all of them |
| **Malicious replication** | DCSync (section 11) aimed at the KRBTGT account |
| **Skeleton key** | A patch applied in the domain controller's memory that makes one master password work for every account, alongside the real ones; lost at reboot |
| **Golden ticket** | A forged TGT made from the KRBTGT hash: any user, any service, for as long as the forger chooses |
| **Silver ticket** | A forged service ticket made from one service account's hash; the domain controller is never contacted |

Two more are described alongside. **AdminSDHolder** is a template whose permissions Windows copies onto all protected administrator groups at intervals; an attacker who adds themselves to the template is re-granted rights automatically. **Overpass-the-hash** uses a stolen NT hash or Kerberos key to request a genuine TGT, turning a hash into tickets.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware says the AdminSDHolder permissions are re-applied "every 60 minutes" in one place, then shows a registry change it describes as "3 minutes" using the value 300.

    **In practice:** Microsoft's documentation gives the default as **60 minutes**, run on the domain controller holding the PDC emulator role, and the registry value is in *seconds* with an allowed range of 60 to 7,200. So 300 means five minutes, not three. Learn 60 minutes. Checked on learn.microsoft.com (page updated 12 May 2025).

### Commands for looking around

The courseware ends this part with fourteen tables of "post-exploitation" commands for Linux and Windows. They are ordinary administration commands: list hidden files, scheduled tasks, services, users, shares, routes, firewall state and installed software. Recognise what a command is for; the exact switches are rarely examined.

!!! exam "Exam answer / In practice (as checked in November 2026)"
    **Exam answer:** the tables use `netsh firewall show state` and `netsh firewall show config` to read the Windows firewall.

    **In practice:** Microsoft's guidance (page updated 12 February 2026) is to use the newer `netsh advfirewall firewall` commands and warns that the old `netsh firewall` context may be removed in a future version. The same tables lean on `wmic`, which is now gone from Windows 11 (section 12).

### Defences against persistence

The courseware's list: reset the **KRBTGT password twice** after any suspected compromise (twice, because the previous password is also accepted); monitor ticket requests and replication; restrict domain administrators from ordinary machines; keep firmware current; collect logs centrally.

!!! cpent "CPENT depth: persistence the courseware leaves out"
    From TryHackMe's Windows Local Persistence and Credentials Harvesting rooms.

    - **Quiet group membership.** Adding an account to Backup Operators and Remote Management Users gives nearly administrator-level reach without appearing in the Administrators group.
    - **RID hijacking.** Changing the identifier stored for a normal local account so that Windows treats it as the built-in Administrator.
    - **Hidden scheduled tasks, file-association hijacks and Winlogon values.** Further start-up points beyond Run keys.
    - **Protecting LSASS.** Running the logon service as a protected process, and Credential Guard, which keeps secrets in an isolated virtual environment, are the modern answers to credential theft from memory.

!!! stop "Where these notes stop: persistence and domain dominance"
    **What is held back.** The commands that add start-up entries, the WMI subscription scripts, and every ticket-forging, skeleton-key and DPAPI command.

    **Where to read them in full.** **ECC e-book:** Maintaining Access › Establishing Persistence, the pages on domain dominance, AdminSDHolder, WMI event subscription and overpass-the-hash; Tables 6.13 to 6.25. **ECC Lab Manual:** Lab 2 Task 1 (Sticky Keys); Lab 3 Task 2, "Maintain Persistence by Modifying Registry Run Keys". **TryHackMe:** Windows Local Persistence (Premium), all tasks; Attacking Kerberos (Premium), the golden and silver ticket and skeleton key tasks; Post-Exploitation Basics (free). **HTB Academy:** Password Attacks, sections "Attacking Windows Credential Manager" and "Attacking Active Directory and NTDS.dit"; Active Directory Enumeration & Attacks (outline only).

!!! try "Practise it"
    **Official ECC lab:** Lab 3 Task 2 (registry Run keys). **TryHackMe:** Windows Local Persistence (Premium). **HTB Academy:** none dedicated to persistence on the practice map.

    Example, not run. On your own Windows machine, see what already starts at logon for all users:

    ```bash
    reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
    ```

!!! recap "Recap: section 15"
    - Host persistence: Sticky Keys, Run keys, Startup folder, WMI event subscription.
    - Six domain dominance techniques, ending with golden and silver tickets.
    - A skeleton key lives in the domain controller's memory and adds a master password.
    - AdminSDHolder permissions are re-applied every 60 minutes.
    - After a compromise, the KRBTGT password is reset twice.

## 16. Clearing logs and covering tracks {M}

The last phase removes the evidence. An intruder who plans to stay removes only the entries that reveal them, because an empty log is itself a warning. Investigators detect tampering by comparing cryptographic hashes of logs and files with earlier copies.

### The eight techniques {M: Covering tracks techniques: disabling auditing, clearing logs, manipulating logs, covering tracks on the network, covering tracks on the OS, deleting files, disabling Windows functionality, hiding artifacts}

```diagram m06-tracks
The eight ways of covering tracks named in the courseware.
```

### Auditing and logs on Windows {M: Windows: auditpol reads and sets audit policy; wevtutil el lists logs, wevtutil cl <log> clears one; Clear-EventLog (PowerShell); Meterpreter clearev; cipher /w:<folder> overwrites free space with 0x00, 0xFF, then random data}

| Tool | What it does |
| --- | --- |
| `auditpol` | Shows and changes which kinds of event are recorded. An intruder switches categories off on arrival and back on when leaving |
| `wevtutil el` / `wevtutil cl <log>` | Lists the event logs; clears the one named |
| `Clear-EventLog` | PowerShell command that empties a named log |
| Meterpreter `clearev` | Clears the Application, System and Security logs in one step |
| Event Viewer | The graphical way to do the same |
| `cipher /w:<folder>` | Overwrites the unused space on a drive three times, with zeros, then 0xFF, then random data, so that deleted files cannot be recovered |

!!! exam "Exam answer / In practice (as checked in November 2026)"
    **Exam answer:** the courseware names the Windows log files as `SECEVENT.EVT` (security), `SYSEVENT.EVT` (system) and `APPEVENT.EVT` (application).

    **In practice:** those are the Windows XP-era names. Microsoft's documentation says the newer Windows Event Log system replaced the old one in Windows Vista; current logs are `Security.evtx`, `System.evtx` and `Application.evtx`. Likewise, Microsoft documents `Clear-EventLog` only for Windows PowerShell 5.1 and says such commands work "only on classic event logs"; it is absent from PowerShell 7. Checked on learn.microsoft.com.

### Shell history on Linux {M: Bash history: stored in ~/.bash_history; export HISTSIZE=0 stops recording; history -c clears the current session's list; shred overwrites the file}

| Command | Effect |
| --- | --- |
| `export HISTSIZE=0` | Tells the shell to remember no commands from now on |
| `history -c` | Clears the list held in the current session |
| `history -w` | See the note below |
| `shred ~/.bash_history` | Overwrites the saved history file so it cannot be recovered |

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware and the Lab Manual both say `history -w` "deletes the history of the current shell".

    **In practice:** `-w` *writes* the session's current list to the history file. It appears to delete only when it is run just after `history -c`, because it then saves an empty list over the file. If the exam offers "delete history of the current shell" for `history -w`, that is the courseware's wording.

### Hiding on the network

| Technique | Idea |
| --- | --- |
| **Reverse HTTP shell** | The victim machine asks the attacker for instructions with ordinary-looking web requests |
| **Reverse ICMP tunnel** | Data travels inside ping packets, which firewalls often let out |
| **DNS tunnelling** | Data travels inside name lookups |
| **TCP parameters** | Data is hidden a character at a time in header fields: the IP identification field, the TCP acknowledgement number or the TCP initial sequence number |

### Hiding on the operating system

On Windows: data streams (section 13), changed file time stamps (the courseware names the Metasploit tool **timestomp** and a PowerShell property), and the hidden and system file attributes set with `attrib`. A user account can be hidden from the logon screen through a registry key. On Linux and macOS: file names beginning with a dot, and changed time stamps with `touch`.

### Switching off Windows features that record activity

The courseware lists: the **last access time stamp** (`fsutil`), **hibernation** (the `hiberfil.sys` file holds a copy of memory), the **paging file** (virtual memory), **system restore points**, the **thumbnail cache**, **Prefetch** (records which programs ran), and Windows **activity history**. For browsers it lists private browsing and clearing history, cookies, cache and saved passwords.

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware gives the recent-documents registry key under `HKEY_LOCAL_MACHINE`, shows `more < C:\SecretFile.txt` as the way to read a hidden stream, and gives `sudo killall -INFO mDNSResponder` to flush the macOS name cache.

    **In practice:** recent documents are per user, under `HKEY_CURRENT_USER`. A stream is read by naming it: `more < LegitFile.txt:SecretFile.txt`. On macOS the flushing signal is `-HUP`; `-INFO` only writes the cache contents to the log. These three were not checked on an owner's site for this chapter; they are general knowledge, noted in the table at the end.

### Anti-forensics and wiping tools

The courseware's wider list of **anti-forensics** techniques: deleting files, password protection, steganography, hiding data in file-system structures (bad-cluster records, slack space, hidden disk areas), **trail obfuscation** (false time stamps and headers, log cleaners), **artifact wiping**, overwriting data and metadata, **program packers**, minimising footprints (live systems, virtual machines) and anonymised access.

Track-covering tools named: CCleaner, DBAN, Privacy Eraser, Wipe, BleachBit.

!!! exam "Exam answer / In practice (as checked in November 2026)"
    **Exam answer:** DBAN is a tool for wiping drives.

    **In practice:** DBAN's own site, run by Blancco, says it gets no software updates, cannot detect or erase solid-state drives and gives no proof of erasure. On a modern machine with an SSD it is not a safe wiping method. The page carries no date. Checked on dban.org.

### Defending the logs

The courseware's list: turn logging on everywhere; send logs to a **separate, central log server**; make them **append-only or immutable**, encrypted and backed up to media that cannot be altered; restrict who can read and write them; keep old entries rather than overwriting; monitor file integrity; use a SIEM, intrusion detection and behaviour analytics; patch and close unused ports.

!!! remember "Remember"
    **A log the intruder can reach is a log the intruder can edit.** The one defence that defeats every technique in this section is a copy of the log on another machine.

!!! trap "Exam traps"
    - **`auditpol` changes what is recorded; `wevtutil` clears what was recorded.**
    - **`cipher /w` wipes free space,** not existing files.
    - **Disabling auditing comes first in the list,** before any clearing.
    - **timestomp changes time stamps;** it does not delete anything.

!!! try "Practise it"
    **Official ECC lab:** Lab 4, "Clear Logs to Hide the Evidence of Compromise": Task 1 on Windows (a batch script, `wevtutil` and `cipher`), Task 2 on Linux (bash history). **TryHackMe:** Metasploit: Meterpreter (Premium) lists `clearev` among the system commands; no room on the practice map is about log clearing. **HTB Academy:** none on the practice map.

    Examples, not run. Read-only commands that show what is being recorded on your own Windows machine:

    ```bash
    auditpol /get /category:*
    wevtutil el
    ```

!!! recap "Recap: section 16"
    - Eight techniques, from disabling auditing to hiding artifacts.
    - Windows: `auditpol`, `wevtutil`, `Clear-EventLog`, `clearev`, `cipher /w`.
    - Linux: `HISTSIZE=0`, `history -c`, `shred` the history file.
    - Network hiding: reverse HTTP, ICMP tunnels, DNS tunnels, TCP header fields.
    - The defence is a central, append-only copy of the logs.

## 17. Lab and practice route {D}

This module has no lab of our own. The official labs total about 140 minutes. Do the three sources in this order; the practice material is large (HTB Academy's own estimates for the listed modules add up to more than two weeks), so the table marks what to do first.

| Step | Where | What you do | Sections |
| --- | --- | --- | --- |
| 1 | **TryHackMe: Password Cracking** and **John the Ripper: The Basics** (Premium), or **HTB Academy: Password Attacks**, first six sections (Tier 0) | Hash types, wordlists, rules, masks | 3, 5 |
| 2 | **TryHackMe: Hydra** (free) or **HTB Academy: Login Brute Forcing** (Tier II, free to unlock) | Guessing against live services | 3 |
| 3 | **ECC Lab 1 Task 1**: Responder | Capture and crack one network logon | 4, 5 |
| 4 | **TryHackMe: Metasploit: Introduction** (free), then **HTB Academy: Using the Metasploit Framework** (Tier 0) | Modules, payloads, sessions | 7 |
| 5 | **ECC Lab 1 Task 2**: reverse shell generator; **TryHackMe: Blue** (free) | One exploit from scan to shell | 7 |
| 6 | **ECC Lab 1 Task 3**: buffer overflow on vulnserver | The eight steps, in a debugger | 8 |
| 7 | **TryHackMe: Linux Privilege Escalation** (free), then **Windows Privilege Escalation** (Premium) | Find and use one misconfiguration at a time | 10 |
| 8 | **ECC Lab 2**: bypass UAC and exploit Sticky Keys | Standard user to SYSTEM | 10, 15 |
| 9 | **ECC Lab 3**: Spyrix; registry Run keys | Monitoring and persistence | 12, 15 |
| 10 | **ECC Lab 4**: clear logs on Windows and Linux | `wevtutil`, `cipher`, bash history | 16 |
| 11 | **HTB Academy: Introduction to Active Directory** (Tier 0), then **TryHackMe: Active Directory Basics** (Premium) | Structure before attack | 2, 9 |
| 12 | **ECC Active Directory lab** (unnumbered, placed after Lab 4) | AS-REP roasting, spraying, PowerView, a database service, an unquoted path, Kerberoasting | 4, 9, 10 |
| 13 | **TryHackMe: Attacktive Directory** (free); **Breaching Active Directory**, **Lateral Movement and Pivoting** (network rooms); **Credentials Harvesting**, **Attacking Kerberos**, **Windows Local Persistence** (Premium); **Post-Exploitation Basics** (free) | The domain attack chain in pieces | 4, 11, 15 |
| 14 | **ECC AI lab** (also numbered "Lab 5") | ShellGPT writes the commands | 7, 14 |
| 15 | **HTB Academy**, for depth: Shells & Payloads; Cracking Passwords with Hashcat; Linux and Windows Privilege Escalation; Active Directory Enumeration & Attacks; Pivoting, Tunneling, and Port Forwarding; the two Stack-Based Buffer Overflows modules | Weeks of material; pick by weakness | 5, 7, 8, 10, 11 |

HTB Academy's **Kerberos Attacks** module is Tier III and was skipped. **What the Shell?** on TryHackMe is Premium.

Answer these in your log as you go:

1. In Lab 1 Task 1, which protocol did the victim fall back to, and which setting from section 6 would have prevented the capture?
2. For the buffer overflow, record the offset you found and the one byte value you had to avoid.
3. Which privilege escalation technique from section 10 did Lab 2 use, and which did the Active Directory lab use?
4. Name one tool in the official labs that has been renamed, archived or removed since the courseware was written, and what replaces it.

Module 7 follows the same intruder one step further: the malware they leave behind.

## Quiz

Twelve questions. The options are shuffled every time you load the page.

```quiz
Q: What is the correct order of the four system hacking phases?
- Escalating privileges, gaining access, clearing logs, maintaining access
- * Gaining access, escalating privileges, maintaining access, clearing logs
- Gaining access, maintaining access, escalating privileges, clearing logs
- Maintaining access, gaining access, escalating privileges, clearing logs
WHY: Get in, elevate, maintain, clear. Hiding files and executing applications belong to maintaining access.
TAG: M

Q: An attacker tries the single password `Welcome1` against four thousand user accounts, one attempt each. Which attack is this?
- Brute-force attack
- Rainbow table attack
- * Password spraying
- Hybrid attack
WHY: Spraying uses one or a few passwords across many accounts so that no single account reaches its lockout limit.
TAG: M

Q: Which pair of protocols and ports does a tool such as Responder poison when DNS fails to resolve a name?
- DNS on UDP 53 and DHCP on UDP 67
- * LLMNR on UDP 5355 and NBT-NS on UDP 137
- Kerberos on TCP 88 and LDAP on TCP 389
- WinRM on TCP 5985 and SMB on TCP 445
WHY: Windows falls back to LLMNR (5355) and NBT-NS (137), both UDP, and anyone on the local network can answer.
TAG: M

Q: Which accounts does AS-REP roasting target?
- Service accounts that have a Service Principal Name
- The KRBTGT account
- * User accounts with Kerberos pre-authentication disabled
- Local administrator accounts in the SAM file
WHY: Without pre-authentication, anyone can request the AS reply for that user and crack it offline. Service accounts with an SPN are the Kerberoasting target.
TAG: M

Q: Why does salting defeat a rainbow table?
- The salt is kept secret from the attacker
- The salt makes the hash longer than the table can store
- * The same password produces a different hash for each salt, so precomputed hashes do not match
- The salt encrypts the hash with the user's password
WHY: A salt is stored in the open; its job is to make precomputation useless, not to be secret.
TAG: U

Q: In the hashcat mask `?u?l?l?l?d?d`, what does the pattern describe?
- Six digits
- * One upper-case letter, three lower-case letters, then two digits
- One symbol, three letters, then two hexadecimal digits
- Any six printable characters
WHY: `?u` is upper case, `?l` lower case and `?d` a digit.
TAG: M

Q: In the courseware's eight steps of a Windows buffer overflow, which step comes immediately after fuzzing?
- Spiking
- Generating shellcode
- Identifying bad characters
- * Identifying the offset
WHY: Spiking, fuzzing, identify the offset, overwrite the EIP, bad characters, right module, shellcode, root access.
TAG: M

Q: A Windows service is installed at `C:\Program Files\Acme Tools\svc.exe` and its configured path has no quotation marks. A tester places a program at `C:\Program Files\Acme.exe` and it runs as SYSTEM at the next start. Which technique is this?
- DLL hijacking
- * Unquoted service path
- Named pipe impersonation
- Application shimming
WHY: Without quotation marks Windows tries each space-separated partial path in turn, so a planted program earlier in the path runs with the service's rights.
TAG: U

Q: Which type of rootkit turns the running operating system into a guest virtual machine and sits beneath it?
- Kernel-level rootkit
- Boot-loader-level rootkit
- * Hypervisor-level rootkit
- Library-level rootkit
WHY: A hypervisor-level rootkit uses the processor's virtualisation features to run below the operating system, sometimes called Ring -1.
TAG: M

Q: A message is hidden so that reading the first letter of every word of an innocent-looking paragraph spells it out. What is this called?
- A grille cipher
- A visual semagram
- * A null cipher
- A jargon code
WHY: A null cipher hides the message in chosen letters of ordinary text. A grille cipher needs a template with holes.
TAG: M

Q: A file `report.txt` on an NTFS drive shows a size of 2 KB, but a 4 MB program has been attached to it as an alternate data stream. What does a normal directory listing show?
- 4 MB, because the larger stream is reported
- * 2 KB, because only the main stream's size is shown
- Two separate files
- An error, because streams cannot hold programs
WHY: Alternate data streams do not change the visible size; only the modification time changes. Tools such as Streams or LADS reveal them.
TAG: U

Q: A clinic wants to be sure an intruder who becomes administrator on a workstation cannot erase the evidence. Which single measure helps most?
- A longer screen-lock timeout
- Clearing the event logs every night
- * Forwarding logs to a separate, append-only central log server
- Hiding the event log files with the hidden attribute
WHY: A copy held on another machine survives whatever is done to the local logs; every local technique in section 16 can be undone by an administrator on that machine.
TAG: U
```

## Exam cheat sheet

Only the MEMORISE items from this chapter, collected automatically. If a fact is not here, you need to understand or recognise it, not recite it.

[[cheatsheet]]

## Coverage check against the official Module 6

Each sub-topic of the official module and where this chapter covers it. The section-by-section verification report, with the comparison against TryHackMe and HTB Academy, is kept with the handbook source as `verification/ceh/m06-system-hacking.md`. No official text is reproduced.

| Official sub-topic | Covered in | Status |
| --- | --- | --- |
| Learning objectives; hacking methodology and its goals | Opening table, 1 | OK |
| Microsoft authentication: SAM, NTLM, Kerberos | 2 | OK, updates on SYSKEY and NTLM |
| Password cracking; types of password attack | 3 | OK |
| Non-electronic attacks | 3 | OK |
| Active online: dictionary, brute force, rule-based, hybrid, syllable, spraying, mask, guessing, default passwords | 3, 5 | OK, mask syntax in 5 |
| Active online: Trojans, spyware and keyloggers for passwords | 3, 12 | OK, one line in 3 |
| Hash injection (pass-the-hash) | 4 | OK, commands held back |
| LLMNR/NBT-NS poisoning; Responder | 4, 6 | OK, commands held back |
| Internal monologue attack | 4 | OK, reduced |
| Kerberos cracking: AS-REP roasting, Kerberoasting; pass-the-ticket | 4 | OK, update on RC4; exam/practice note on the lab's labels |
| NTLM relay | 4 | OK, commands held back |
| Combinator, fingerprint, PRINCE, toggle-case, Markov chain, GPU-based attacks | 3 | OK, exam/practice note on "GPU-based" |
| Passive online: wire sniffing, man-in-the-middle, replay | 3 | OK, names only |
| Offline: rainbow tables, distributed network attack | 5 | OK, `rtgen` named, syntax not given |
| Password recovery and cracking tools | 5 | OK, update on L0phtCrack |
| Password salting | 5 | OK |
| Defences against password cracking, LLMNR/NBT-NS poisoning and SMB attacks | 6 | OK, update on password expiry; exam/practice note on SMBv2 |
| Vulnerability exploitation steps; exploit sites; proof of concept | 7 | OK |
| WES-NG | 7 | OK |
| Metasploit Framework: modules, payload types | 7 | OK, individual example modules not listed |
| AI-powered exploitation tools | 7 | OK |
| Buffer overflow: types, stack and heap, registers | 8 | OK |
| Windows buffer overflow exploitation, eight steps | 8 | OK, scripts and commands held back |
| ROP, ASLR and DEP bypass, heap spraying, JIT spraying, exploit chaining | 8 | OK |
| Active Directory domain mapping: BloodHound, PowerView (Tables 6.1 to 6.10), GhostPack and Seatbelt (Table 6.11) | 9 | OK, command families not every command; Seatbelt groups not listed |
| Buffer overflow detection tools and defences | 8 | OK |
| Privilege escalation: types | 10 | OK |
| DLL and dylib hijacking; Spectre and Meltdown; named pipe impersonation; misconfigured services | 10 | OK |
| Pivoting and relaying | 11 | OK, commands held back |
| NFS misconfiguration; UAC bypass; boot or logon scripts; domain policy modification; DCSync; AD CS abuse | 10, 11 | OK, exam/practice note on NFS |
| Other techniques: tokens, parent PID spoofing, shimming, accessibility features, SID-History, COM hijacking, scheduled tasks (Table 6.12), launch daemons, plist, setuid, web shell, sudo, SUID/SGID, kernel exploits, PATH, ptrace, MSI, NoFilter | 10 | OK, one line each; crontab options not listed |
| Privilege escalation tools and defences | 10, 11 | OK, grouped |
| Executing applications; remote code execution techniques and tools | 12 | OK, update on WMIC |
| Keyloggers: types, hardware and software products | 12 | OK, lead products only |
| Spyware: types and tools | 12 | OK, eleven types named; products reduced |
| Defences against keyloggers and spyware; anti-keyloggers; anti-spyware | 12 | OK, update on Kaspersky |
| Rootkits: types, how they work, examples, detection, defences, anti-rootkits | 13 | OK, exam/practice note on the count; manual detection steps not given |
| NTFS data streams: creation, manipulation, defences, detectors | 13 | OK |
| Steganography: classification, techniques, media, tools | 14 | OK, tools reduced to lead examples; Snow options not given |
| Steganalysis: attacks, detection by file type, tools | 14 | OK, detection by file type reduced |
| Establishing persistence: Sticky Keys, autostart, domain dominance, AdminSDHolder, WMI event subscription, overpass-the-hash | 15 | OK, commands held back; exam/practice note on AdminSDHolder |
| Linux and Windows post-exploitation (Tables 6.13 to 6.25) | 15 | Reduced to one paragraph and an exam/practice note |
| Defences against persistence | 15 | OK |
| Clearing logs: techniques, auditpol, clearing and manipulating logs | 16 | OK, exam/practice notes on log names and `history -w` |
| Covering tracks on the network and the operating system; deleting files; disabling Windows functionality; hiding artifacts | 16 | OK, registry paths and menu routes not given |
| Anti-forensics techniques; track-covering tools; defences | 16 | OK, exam/practice note on DBAN |
| Lab Manual: Labs 1 to 4, the Active Directory lab, the AI lab | 4, 7, 8, 10, 12, 15, 16, 17 | OK, named in practice boxes; not run |

### Not read or not verified

Kept here so that a reviewer can see what is still open. Checked 19 November 2026.

| Item | Status | What would close it |
| --- | --- | --- |
| The 262 figures in the courseware | Not read: screenshots and diagrams | Look at the figures in the e-book |
| Working attack commands throughout the module | Deliberately not transcribed from any source; the "Where these notes stop" boxes list where each set is | Read the named pages inside the lab environments |
| HTB Academy: Shells & Payloads | First ten of seventeen sections read; no detailed notes kept; the rest by title | Read the module |
| HTB Academy: both Stack-Based Buffer Overflows modules; Linux and Windows Privilege Escalation; Active Directory Enumeration & Attacks; Pivoting, Tunneling, and Port Forwarding | Outline and overview only (139 sections), by the owner's decision of 19 November 2026 | Read the modules |
| HTB Academy: Kerberos Attacks | Skipped: Tier III | Needs cubes or a higher plan |
| HTB section titles quoted for the outline-only modules | Taken from the module outline in shortened form; exact wording may differ | Open each module's contents list |
| TryHackMe: terminal output in the Metasploit rooms and the last eight rooms | Teaching text read in full; long terminal output cut | Read the rooms while doing them |
| TryHackMe: whether Breaching Active Directory and Lateral Movement and Pivoting are free or Premium | Not recorded | Open each room page |
| BloodHound Community Edition release month (August 2023) | From memory; the owner's pages give "deprecated" and 2023 only | Check the SpecterOps release notes |
| NIST SP 800-63B-4 publication month (July 2025) | The rule's wording was read on pages.nist.gov; the month came from secondary pages | Check the NIST publication page |
| Kaspersky prohibition | Dates seen on the bis.gov press release through a search result; the page itself failed to load | Open the press release |
| NTLMv1 removed in Windows 11 24H2 and Server 2025 | From a secondary report of Microsoft's removed-features page | Open Microsoft's removed-features page |
| Kerberos RC4 change dates | From Microsoft's Tech Community blog and message-centre text seen through search results | Open the Microsoft support article |
| Recent-documents key location; reading a stream; macOS cache flush signal; `dir /r`; modern `.evtx` file names | General knowledge, not checked on an owner's site | Check learn.microsoft.com and support.apple.com |
| PowerView command renaming; `class MetasploitModule`; Metasploit adapters; RainbowCrack's supported Windows versions | Not checked on an owner's site | Check each project's repository |
| Steganalysis attack definitions; rootkit ring numbers | The courseware list is long-standing; our one-line meanings were written from the notes and general knowledge | Re-read the e-book pages |
| Cached-logon (DCC2) speed figure; yescrypt as a default | As stated in HTB Academy's Password Attacks module, not checked elsewhere | Check hashcat benchmarks and Debian release notes |
| Hospital worked example | Invented for teaching; not a real incident | Nothing |
| Source comparison table | Written after the chapter draft, from notes made during reading | Nothing; noted for accuracy |
| All commands and all six official labs | Not run | Run them only in the official labs or named rooms |

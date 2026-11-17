---
title: Module 1 - Introduction to Ethical Hacking
book: Ethical Hacking Study Handbook
module: 1
kicker: Ethical hacking track · Module 1 of 20
home: index.html
lab: 45
difficulty: Beginner
status: Review draft
verified: 18 Nov 2026: CEH v13 courseware Module 01, MITRE ATT&CK release notes
footer: Unofficial, independent study material. Not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Written in our own words from public standards and frameworks. Use these techniques only on systems you own or are authorised in writing to test.
---

# Introduction to Ethical Hacking

[[meta]]

## What this chapter is about

This chapter gives you the vocabulary and the map for everything that follows. It answers four questions. What are we protecting? Who attacks it, and how do they go about it? What is an ethical hacker allowed to do? And which laws and standards apply?

!!! story "An everyday picture"
    A bank hires a locksmith to try to break into its own vault at night. The locksmith uses the same picks and the same patience as a burglar. Three things make the work honest: a signed letter from the bank, an agreed list of what may be touched, and a report at the end that says exactly how the vault was opened and how to stop it happening again. Take away the letter and the same actions are a crime. That locksmith is an ethical hacker.

There are no commands to learn here. There are a lot of lists. The exam asks about them directly, so this chapter tells you which lists to learn by heart and gives you a way to remember each one.

!!! before "Before you start"
    This chapter assumes very little.

    - **Information system.** Computers, networks, software and the data they hold, taken together.
    - **Vulnerability.** A weakness that can be abused. A door with a broken lock is a vulnerability.
    - **Threat.** Something that could cause harm. A burglar in the neighbourhood is a threat.
    - **Malware.** Software written to do harm: viruses, ransomware and the like. Module 7 covers it.
    - **Log.** The diary a computer keeps of what happened on it and when.

    Everything else is defined where it first appears.

!!! why "Why this matters to you"
    - **Exam candidate.** This module is almost pure recall. Expect direct questions on the five security elements, attack classes, hacker types, the kill chain phases, threat intelligence types, incident handling steps and which law covers what.
    - **Defending a network.** The frameworks here (kill chain, MITRE ATT&CK, incident handling) are the language security teams use every day to describe an attack and decide where to stop it.
    - **Working with sensitive data.** If you handle patient, customer or student records, section 6 tells you which rules bind your organisation, and section 5 explains what "risk" means when someone asks you to assess it.

### How the tags work

[[legend]]

Facts tagged MEMORISE are collected automatically into the [cheat sheet](#exam-cheat-sheet) at the end.

**How to use this chapter.** Read one section at a sitting; there are six. Say each mnemonic aloud. Run the "Try it" boxes in lab L01 where they need one. Finish with the quiz.

| After this chapter you can | Section |
| --- | --- |
| Name the five elements of security and classify any attack | 1 |
| Tell the hacker classes apart and state what makes hacking ethical | 2 |
| Recognise the AI tools the syllabus names | 3 |
| Walk through the CEH framework, the kill chain, ATT&CK and the Diamond Model | 4 |
| Explain risk, threat intelligence, threat modelling and incident handling | 5 |
| Match a law or standard to what it protects | 6 |

## 1. Information security concepts {U}

**Information security** means keeping information, and the systems that store, process and send it, safe from unauthorised access, disclosure, alteration and destruction.

### The five elements {M: Five elements of information security: confidentiality, integrity, availability, authenticity, non-repudiation. Controls: encryption (C); checksums and access control (I); redundancy and anti-DDoS (A); biometrics, smart cards, certificates (authenticity); digital signatures (non-repudiation)}

```diagram m01-elements
The five elements. Every attack damages at least one of them.
```

| Element | Meaning | Typical control |
| --- | --- | --- |
| Confidentiality | Only authorised people can see the information | Data classification, encryption, proper disposal of equipment |
| Integrity | The information has not been improperly changed | Checksums, access control |
| Availability | Systems and data are there when authorised users need them | Redundant disks and clustered machines, antivirus, DDoS protection |
| Authenticity | A message, document or user is genuine | Biometrics, smart cards, digital certificates |
| Non-repudiation | The sender cannot deny sending; the receiver cannot deny receiving | Digital signatures |

!!! exam "Exam answer / In practice"
    **Exam answer:** information security has **five** elements.

    **In practice:** most textbooks and standards teach the three-part "CIA triad" and treat authenticity and non-repudiation as extensions. If a question says "elements of information security", count five.

!!! remember "Remember"
    **CIA + AN**: Confidentiality, Integrity, Availability, then Authenticity and Non-repudiation. "The CIA wants **A**nswers **N**ow."

### What an attack is made of {M: Attack = Motive (goal) + Method (TTP) + Vulnerability. TTP = tactics (overall strategy, start to finish), techniques (technical methods for intermediate results), procedures (the systematic sequence of actions)}

```diagram m01-attack
The attack equation. Remove any one of the three and there is no attack.
```

**Motives** include disrupting business, stealing or manipulating data, creating fear by hitting critical infrastructure, causing financial loss, spreading political or religious beliefs, serving a state's military aims, damaging reputation, revenge and ransom.

**TTPs** describe how an attacker works.

| Term | Meaning | Analogy: a burglar |
| --- | --- | --- |
| Tactics | The strategy for the whole attack, beginning to end | "Hit empty houses during the school run" |
| Techniques | The technical methods used to get intermediate results | Slipping a latch with a card |
| Procedures | The systematic, step-by-step sequence the actor follows | Watch for a week, enter by the back, leave in four minutes |

A **vulnerability** is a weakness in design or implementation that can be exploited. The courseware gives five reasons they exist: hardware or software misconfiguration; insecure or poor design of the network or application; inherent technology weaknesses; end-user carelessness; and intentional end-user acts, such as an ex-employee abusing access that was never removed. {R}

### Five classes of attack {M: Attack classes (IATF): passive (sniffing, footprinting, traffic analysis: no tampering); active (DoS, malware, spoofing, MITM, SQL injection: tampers or disrupts); close-in (physical proximity: shoulder surfing, dumpster diving); insider (trusted person: pod slurping, planting keyloggers); distribution (tampering with hardware or software at source or in transit)}

The classification comes from the Information Assurance Technical Framework (IATF).

| Class | What defines it | Examples |
| --- | --- | --- |
| Passive | Watches traffic; changes nothing. Very hard to detect | Footprinting, sniffing and eavesdropping, traffic analysis, decrypting weak encryption |
| Active | Tampers with data or disrupts service; detectable | Denial of service, malware, spoofing, replay, man-in-the-middle, session hijacking, SQL injection, privilege escalation |
| Close-in | Attacker is physically near the target | Social engineering: eavesdropping, shoulder surfing, dumpster diving |
| Insider | A trusted person with access misuses it | Theft of devices, data theft, pod slurping, planting keyloggers or backdoors |
| Distribution | Hardware or software is tampered with before installation | Changes at the factory or in transit; vendor backdoors |

!!! remember "Remember"
    **P-A-C-I-D**: Passive, Active, Close-in, Insider, Distribution. "A hacker's **PACID** test."

!!! trap "Exam traps"
    - Footprinting is listed as a **passive** attack, even though some footprinting touches the target.
    - Shoulder surfing and dumpster diving are **close-in**. The same eavesdropping by an employee is **insider**.
    - A backdoor fitted at the factory is a **distribution** attack, not an insider attack.

### Information warfare {R}

**Information warfare** is the use of information and communication technology to gain an advantage over an opponent. Martin Libicki's seven categories:

| Category | In one line |
| --- | --- |
| Command and control (C2) warfare {R} | Control over a compromised system or network |
| Intelligence-based warfare {R} | Designing, protecting and denying systems that gather knowledge of the battlespace |
| Electronic warfare {R} | Radio-electronic and cryptographic techniques that degrade communication |
| Psychological warfare {R} | Propaganda and terror to demoralise the adversary |
| Hacker warfare {R} | Shutting systems down, stealing data, false messaging |
| Economic warfare {R} | Blocking the flow of information to damage a business or nation |
| Cyberwarfare {R} | The broadest: information terrorism, semantic attacks, simulated warfare |

Each has a **defensive** side (protecting your own assets) and an **offensive** side (attacking the opponent's). {M: Information warfare is either defensive (protect your ICT assets) or offensive (attack the opponent's)}

!!! try "Try it"
    See integrity protection work. In the L01 attacker container, or any terminal:

    ```bash
    echo "pay 100 to Asha" > m.txt; sha256sum m.txt; echo "pay 900 to Asha" > m.txt; sha256sum m.txt
    ```

    One changed character gives a completely different checksum. That is how tampering is detected.

!!! recap "Recap: section 1"
    - Five elements: confidentiality, integrity, availability, authenticity, non-repudiation.
    - Attack = motive + method + vulnerability. TTP = tactics, techniques, procedures.
    - Five attack classes: passive, active, close-in, insider, distribution.
    - Vulnerabilities exist because of misconfiguration, poor design, weak technology, careless users and deliberate users.
    - Information warfare has seven Libicki categories and is defensive or offensive.

## 2. Hackers and ethical hacking {U}

**Hacking** means exploiting system vulnerabilities and compromising security controls to gain unauthorised or inappropriate access to system resources. A **hacker**, in the exam's sense, is someone who breaks in without authorisation.

### Hacker classes {M: Hacker classes: black hat (malicious; "cracker"); white hat (defensive, with permission); gray hat (both, at different times); script kiddie (unskilled, uses others' tools); hacktivist (political or social protest); state-sponsored (government-employed); cyber terrorist (fear, religious or political); suicide hacker (no fear of punishment); blue hat (contract tester before release); red hat (vigilante against black hats); green hat (eager learner); industrial spy; insider; criminal syndicate; organized hackers; hacker team}

| Class | Who they are | Driven by |
| --- | --- | --- |
| Script kiddies | Unskilled; run tools written by others; quantity over quality | Thrill, recognition |
| White hats | Use hacking skills defensively, **with the owner's permission** | Improving security |
| Black hats | Highly skilled; illegal or malicious purposes. Also called **crackers** | Money, data, harm |
| Gray hats | Work offensively and defensively at different times | Curiosity, recognition |
| Hacktivists | Break in as an act of protest; deface or disable websites | A political or social cause |
| State-sponsored hackers | Employed by a government to penetrate other nations' systems | Espionage, national aims |
| Cyber terrorists | Create fear through large-scale disruption | Religious or political beliefs |
| Corporate (industrial) spies | Steal trade secrets from competitors | Competitive advantage |
| Blue hats | Contract security professionals who test a system before release | Product security |
| Red hats | Attack black hats with aggressive methods; do not follow ethical rules | "Cyber justice" |
| Green hats | Newcomers keen to learn | Learning |
| Suicide hackers | Attack critical infrastructure and do not care about being caught | A "cause" |
| Hacker teams | Skilled groups with their own funding who research the latest technology | Research, capability |
| Insiders | Trusted employees with access: disgruntled, dismissed or undertrained | Grievance, gain |
| Criminal syndicates | Groups in organised, prolonged crime across jurisdictions | Money |
| Organized hackers | Hierarchical criminal groups that rent botnets and crimeware | Money, selling data |

!!! trap "Exam traps"
    - The one word that separates a white hat from everyone else is **permission**.
    - A gray hat who reports a flaw found without permission has still accessed the system without authorisation.
    - A **suicide hacker** is defined by not fearing punishment, not by skill or cause.

### What ethical hacking is {U}

**Ethical hacking** is using hacking tools, tricks and techniques to find exploitable weaknesses in a system, with the owner's permission, in order to fix them. Ethical hackers report everything they find to the owner.

An ethical hacker's assessment answers three questions. Each belongs to particular phases of an attack: {M: Ethical hacker's three questions: What can an attacker see? (reconnaissance, scanning). What can an intruder do with it? (gaining and maintaining access). Are the attempts being noticed? (reconnaissance, covering tracks)}

1. **What can an attacker see on the target?** Reconnaissance and scanning.
2. **What can an intruder do with that information?** Gaining access and maintaining access.
3. **Are the attacker's attempts being noticed?** Reconnaissance and covering tracks.

Organisations hire ethical hackers to prevent break-ins, uncover vulnerabilities, strengthen their security posture, protect customer data and raise security awareness.

!!! exam "Exam answer / In practice"
    **Exam answer:** the difference between an ethical hacker and a cracker is **consent**, and "ethical hacking is always legal".

    **In practice:** it is legal only while you stay inside a signed authorisation. Step outside the agreed scope, by one address or one hour, and you may have committed an offence. The paperwork is the protection.

### Scope, limits and rules {M: Ethical hacker's rules: get a signed contract giving permission before starting; sign and honour an NDA; stay within the agreed limits (for example, DoS only if agreed). Six audit steps: talk to the client; sign the NDA; organise the team and schedule; conduct the test; analyse and report; present findings}

An ethical hacker must:

- **Gain authorisation**: a signed contract giving permission to test, before any work begins.
- **Maintain confidentiality**: follow a non-disclosure agreement (NDA); disclose nothing to third parties.
- **Stay within the agreed limits**: for example, attempt denial of service only if the client agreed to it beforehand.

The framework for a security audit has six steps:

1. Talk to the client and discuss what the test must address.
2. Prepare and sign NDA documents.
3. Organise the team and prepare a schedule.
4. Conduct the test.
5. Analyse the results and prepare a report.
6. Present the findings to the client.

A group that performs a full-scale test covering network, physical and system intrusion is called a **tiger team**. {R}

The limitation: an ethical hacker can only help an organisation understand its security. It is up to the organisation to put the safeguards in place.

### Skills {R}

| Technical | Non-technical |
| --- | --- |
| In-depth knowledge of the major operating environments: Windows, Unix, Linux, Macintosh | Learns and adapts to new technology quickly |
| In-depth knowledge of networking concepts, hardware and software | Strong work ethic, problem solving and communication |
| Knowledge of security areas and how sophisticated attacks are launched | Committed to the organisation's security policies; aware of local standards and laws |

!!! cpent "CPENT depth: the paperwork professionals actually sign"
    The "signed contract" is usually three documents. A **statement of work** says what is being bought. **Rules of engagement** list in-scope addresses, forbidden actions, testing hours, emergency contacts and what to do if you find evidence of a real attacker. A **letter of authorisation** is what you show if someone calls the police. In L01 the student brief plays the role of the rules of engagement; read it as one.

!!! try "Try it"
    Open `labs/L01-recon-enumeration/student/brief-generic.md`. Find three things: what is in scope, what is forbidden, and what you must deliver. Those are rules of engagement.

!!! recap "Recap: section 2"
    - Black hats attack, white hats defend with permission, gray hats do both.
    - Know the rarer hats: blue (contract tester), red (vigilante), green (learner), and suicide hackers.
    - Three questions: what can they see, what can they do, is anyone noticing.
    - Three rules: signed authorisation, NDA, stay in scope.
    - Six audit steps, from talking to the client to presenting the report.

## 3. AI-driven ethical hacking {R}

**AI-driven ethical hacking** uses AI algorithms, machine-learning models and automation to speed up and extend an ethical hacker's work. The v13 syllabus adds it to every module.

**Four benefits**: efficiency, accuracy, scalability and cost-effectiveness. {M: AI-driven ethical hacking benefits: efficiency, accuracy, scalability, cost-effectiveness. AI complements ethical hackers; it does not replace them}

**Five application areas**: network security, application security, cloud security, IoT security and threat intelligence. {R}

**How it helps**: automating repetitive tasks; predictive analysis; advanced threat detection, including zero-days; better decision making; adaptive learning; better reporting; simulation and testing; scalability; continuous monitoring; adaptive defence. {R}

**The myth.** "AI will replace ethical hackers." It will not. AI needs humans to oversee it, check it and interpret results. Creativity, context and judgement stay with the human. {U}

### Tools the syllabus names {R}

| Tool | What the courseware says it does |
| --- | --- |
| ShellGPT {R} | Generates and completes shell commands, writes code snippets and documentation, answers questions in the terminal |
| AutoGPT {R} | Automates task execution and data processing |
| WormGPT {R} | Generates worm-like scripts and payloads |
| ChatGPT with DAN prompt {R} | Uses a "Do Anything Now" prompt to widen what the model will do |
| FreedomGPT {R} | Unrestricted access to AI; bypasses content filters |
| FraudGPT {R} | Described as detecting and preventing fraud |
| ChaosGPT {R} | Simulates chaotic and unpredictable behaviour |
| PoisonGPT {R} | Introduces a malicious model into a trusted AI system, to study model poisoning |

Others to recognise by name: HackerGPT, BurpGPT (adds AI to the Burp Suite web scanner), BugBountyGPT, PentestGPT, GPT White Hack, CybGPT, BugHunterGPT, Hacking APIs GPT, h4ckGPT, HackerNewsGPT, Ethical Hacker GPT and GP(en)T(ester).

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware presents every tool above as an aid for ethical hackers. Match the name to its description.

    **In practice:** WormGPT and FraudGPT were sold on criminal forums to write phishing emails and malware, and "DAN" is a jailbreak that breaks a provider's rules. Do not use them at work. Use an ordinary assistant, inside your authorisation, and verify what it produces.

!!! coasp "COASP link: when the AI is the target"
    This section treats AI as the hacker's tool. COASP turns it round. PoisonGPT in the table above is a preview: a tampered model placed where people trust it is a **distribution attack** from section 1, applied to AI. The kill chain and the ATT&CK matrix in section 4 also have an AI counterpart, **MITRE ATLAS**, which lists tactics such as poisoning training data and extracting a model. Learn the classic frameworks well here and ATLAS will read as a familiar map with new place names.

!!! try "Try it"
    Ask any AI assistant: "List the phases of the cyber kill chain with one defensive control for each." Check its answer against section 4. Note anything it got wrong; that habit is the skill.

!!! recap "Recap: section 3"
    - AI-driven ethical hacking automates and scales the work; four benefits: efficiency, accuracy, scalability, cost.
    - It applies to network, application, cloud and IoT security and to threat intelligence.
    - AI complements human ethical hackers and does not replace them.
    - Recognise ShellGPT, AutoGPT, WormGPT, DAN, FreedomGPT, FraudGPT, ChaosGPT, PoisonGPT.
    - In practice several of those are criminal tools or jailbreaks.

## 4. Hacking methodologies and frameworks {M}

Four models describe how attacks unfold. Each was built for a different job, and the exam asks you to tell them apart.

### The CEH ethical hacking framework {M: CEH hacking framework: 1 Reconnaissance (footprinting, scanning, enumeration); 2 Vulnerability scanning; 3 Gaining access (then escalating privileges); 4 Maintaining access; 5 Clearing tracks. Passive reconnaissance = no direct interaction; active = direct interaction}

```diagram m01-phases
EC-Council's own framework. An ethical hacker follows the same phases as an attacker; only the goal differs.
```

- **Reconnaissance** is the preparation. **Passive** reconnaissance never touches the target directly: public information, news, search engines. **Active** reconnaissance interacts with it: finding open ports, hosts and operating systems.
- **Scanning** probes the network using what reconnaissance found. **Enumeration** makes active connections and direct queries to list users, shares, routing tables and banners.
- **Vulnerability scanning** identifies, measures and classifies weaknesses.
- **Gaining access** is where the actual hacking happens: password cracking, exploiting flaws such as buffer overflows. Then **escalating privileges** from an ordinary account to administrator.
- **Maintaining access** keeps ownership: the attacker may even patch the hole to keep other hackers out.
- **Clearing tracks** removes the evidence, for example by wiping logs.

!!! exam "Exam answer / In practice"
    **Exam answer (v13):** the framework above, with scanning and enumeration inside reconnaissance and vulnerability scanning as its own phase.

    **In practice:** older CEH editions, and most study guides, list five phases as reconnaissance, **scanning**, gaining access, maintaining access, clearing tracks. If a question offers that older list and not the new one, it is the intended answer.

### The cyber kill chain {M: Cyber kill chain (Lockheed Martin), seven phases: reconnaissance, weaponization, delivery, exploitation, installation, command and control, actions on objectives. Weaponization = build the payload; delivery = send it; installation = backdoor for persistence}

Developed by **Lockheed Martin** from the military idea of a kill chain. It is part of **intelligence-driven defence**: break any link and the attack fails.

```diagram m01-killchain
The seven phases. Defenders ask: at which link could we have stopped this?
```

| Phase | What the adversary does |
| --- | --- |
| Reconnaissance | Gathers information: websites, social networks, Whois, DNS, scanning for open ports |
| Weaponization | Chooses or builds a malicious payload from an exploit and a backdoor; prepares a phishing campaign |
| Delivery | Transmits the weapon: email attachment, malicious link, USB drive, watering-hole website |
| Exploitation | Triggers the code, abusing a vulnerability to gain remote access |
| Installation | Installs more malware, such as a backdoor, to stay; hides it |
| Command and control | Opens a two-way channel to its own server, often hidden in web, email or DNS traffic |
| Actions on objectives | Achieves the goal: steals data, disrupts service, destroys capability |

!!! remember "Remember"
    **R-W-D-E-I-C-A**: "**R**obbers **W**ait, **D**eliver, **E**xploit, **I**nstall, **C**ommand, **A**ct."

!!! trap "Exam traps"
    - Building the booby-trapped document is **weaponization**. Emailing it is **delivery**.
    - The victim opening it and the code running is **exploitation**. The backdoor being written to disk is **installation**.

### Adversary behaviours and indicators of compromise {M: IoC types: atomic (IP address, email address), computed (hash, regular expression), behavioral (combination by logic). IoC categories: email, network (URLs, domains, IPs), host-based (filenames, hashes, registry keys, DLLs, mutex), behavioral (document running PowerShell)}

**Adversary behavioural identification** means spotting the common methods attackers use once inside. Recognise these nine: {R}

| Behaviour | What a defender checks |
| --- | --- |
| Internal reconnaissance | Unusual commands in batch scripts and PowerShell; packet captures |
| Use of PowerShell | PowerShell transcript logs, Windows event logs |
| Unspecified proxy activities | Many domains pointing at one host; domain data feeds |
| Use of the command-line interface | Logs of process IDs, oddly named processes, downloaded files |
| HTTP user agent | A tampered user-agent field |
| Command and control server | Outbound connection attempts, unwanted open ports |
| Use of DNS tunneling | Malicious DNS requests and payloads |
| Use of web shell | Server access and error logs, suspicious encoded strings |
| Data staging | Large file transfers, file integrity monitoring, event logs |

An **indicator of compromise (IoC)** is a clue, artefact or piece of forensic data that suggests an intrusion. IoCs are not intelligence by themselves; they are the data points intelligence is built from.

| IoC type | Meaning | Example |
| --- | --- | --- |
| Atomic | Cannot be broken into smaller parts | IP address, email address |
| Computed | Derived from incident data | Hash value, regular expression |
| Behavioural | Atomic and computed indicators combined by some logic | "Document launches PowerShell, then connects out" |

IoCs fall into four **categories**: email indicators, network indicators, host-based indicators and behavioural indicators.

Key IoCs worth recognising: unusual outbound traffic; unusual privileged-account activity; geographical anomalies; multiple login failures; increased database read volume; large HTML response sizes; many requests for the same file; mismatched port and application traffic; suspicious registry or system file changes; unusual DNS requests; unexpected patching; signs of DDoS; bundles of data in the wrong places; web traffic with superhuman behaviour. {R}

### MITRE ATT&CK {M: MITRE ATT&CK: knowledge base of adversary tactics and techniques from real-world observations. Exam matrices: Enterprise, Mobile, PRE-ATT&CK. 14 Enterprise tactics: reconnaissance, resource development, initial access, execution, persistence, privilege escalation, defense evasion, credential access, discovery, lateral movement, collection, command and control, exfiltration, impact}

**MITRE ATT&CK** is a globally accessible knowledge base of adversary tactics and techniques, built from real-world observations. Where the kill chain has seven broad links, ATT&CK for Enterprise has **14 tactics**, each with many techniques beneath it:

Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact.

!!! exam "Exam answer / In practice"
    **Exam answer:** ATT&CK comprises three collections: **Enterprise, Mobile and PRE-ATT&CK**.

    **In practice:** the courseware calls STIX and TAXII "organizations"; they are a format and a protocol for sharing threat data.

!!! update "Updated: October 2020, April 2026 and October 2026"
    **What changed.** MITRE retired PRE-ATT&CK in **October 2020** (ATT&CK v8) and replaced it with the first two Enterprise tactics, Reconnaissance and Resource Development. The matrices are now **Enterprise, Mobile and ICS**. In **April 2026** (v19) the Defense Evasion tactic was split into two, **Stealth** and **Defense Impairment**, so Enterprise now has **15 tactics**. The current release is v20, **October 2026**.

    **The exam still expects:** three collections named Enterprise, Mobile and PRE-ATT&CK, and **14** Enterprise tactics including Defense Evasion. Give the courseware's answer in the exam and use the current matrix at work.

### The Diamond Model of Intrusion Analysis {M: Diamond Model: four core features: adversary, capability, infrastructure, victim. Meta-features: timestamp, phase, result, direction, methodology, resource. Extended model adds socio-political (adversary-victim) and technology (infrastructure-capability) meta-features}

The Diamond Model describes a single intrusion **event** by four connected features. Analysts link events into activity threads to see how an attack unfolded.

```diagram m01-diamond
Every intrusion event has these four corners. Knowing any one helps you find the others.
```

| Feature | The question it answers |
| --- | --- |
| Adversary | **Who** was behind the attack? |
| Victim | **Where** was the attack performed: which person, organisation or asset? |
| Capability | **How** was it done: which malware, tool or technique? |
| Infrastructure | **What** did the adversary use to reach the victim: servers, domains, email accounts? |

Six **meta-features** add detail to an event: timestamp, phase, result, direction, methodology and resource. The **extended** model adds two more: the **socio-political** meta-feature (the relationship between adversary and victim, which is the motive) and the **technology** meta-feature (the relationship between infrastructure and capability).

!!! remember "Remember"
    Which framework for which job? **Kill chain**: the order of an attack. **ATT&CK**: a catalogue of techniques. **Diamond**: the four facts about one event. **CEH framework**: the phases you perform as the tester.

!!! try "Try it"
    Be the defender. In L01, from your own computer's terminal (not the attacker container), start the lab, make one request, and find it in the target's log:

    ```bash
    docker compose exec attacker curl -s http://10.77.0.20/ >/dev/null; docker compose logs --tail 3 h20
    ```

    The source address `10.77.0.100` in that log line is an **atomic, network** indicator.

!!! recap "Recap: section 4"
    - CEH framework: reconnaissance, vulnerability scanning, gaining access, maintaining access, clearing tracks.
    - Kill chain (Lockheed Martin): reconnaissance, weaponization, delivery, exploitation, installation, command and control, actions on objectives.
    - IoCs: atomic, computed, behavioural; categories email, network, host-based, behavioural.
    - ATT&CK: 14 Enterprise tactics; exam matrices Enterprise, Mobile, PRE-ATT&CK.
    - Diamond Model: adversary, capability, infrastructure, victim.

## 5. Information security controls {U}

Controls are what an organisation does to keep unwanted events from happening and to reduce the damage when they do.

### Information assurance and defence in depth {M: Information assurance: integrity, availability, confidentiality, authenticity of information in use, processing, storage, transmission. Defense-in-depth: several protection layers, so breaking one only reaches the next. Adaptive security strategy: protection, detection, responding, prediction}

**Information assurance (IA)** is the assurance that the integrity, availability, confidentiality and authenticity of information are protected while it is used, processed, stored and transmitted. It is achieved through physical, technical and administrative controls.

**Defence in depth** places several layers of protection around the information, on the military principle that a layered defence is harder to defeat than a single barrier. Breaking one layer only delivers the attacker to the next, and buys the defenders time.

```diagram m01-did
Defence in depth. An attacker must get through every layer to reach the data.
```

The **continual or adaptive security strategy** has four activities that run all the time: **protection** (policies, firewalls, physical security), **detection** (monitoring for abnormal activity), **responding** (investigating, containing, eradicating) and **prediction** (risk assessment, attack-surface analysis, threat intelligence).

### Risk {M: Risk = Threats x Vulnerabilities x Impact (also Threat x Vulnerability x Asset Value). Level of risk = Consequence x Likelihood. Risk levels: extreme or high (immediate measures), medium (act soon), low (preventive steps). Risk management phases: identification, assessment, treatment, tracking and review}

**Risk** is the degree of uncertainty or expectation that an adverse event will damage the system.

- **Risk = Threats × Vulnerabilities × Impact**
- **Level of risk = Consequence × Likelihood**

| Risk level | Consequence | Action |
| --- | --- | --- |
| Extreme or high | Serious or imminent danger | Immediate measures; impose controls to reduce the risk |
| Medium | Moderate danger | Not immediate, but act quickly |
| Low | Negligible danger | Take preventive steps |

A **risk matrix** plots likelihood against consequence so risks can be compared at a glance. Each organisation builds its own.

```diagram m01-risk
A three-by-three example. Real matrices are often five-by-five.
```

**Risk management** has four phases:

1. **Risk identification**: find the sources, causes and consequences of risks.
2. **Risk assessment**: estimate likelihood and impact; set priorities.
3. **Risk treatment**: select and apply controls, in order of severity.
4. **Risk tracking and review**: check that the controls work and stay appropriate.

!!! remember "Remember"
    Risk management: **I-A-T-T**: Identify, Assess, Treat, Track. "**I** **A**m **T**racking **T**hreats."

### Cyber threat intelligence {M: Threat intelligence types: strategic (executives, CISO; business risk, trends), tactical (SOC and security managers, architects; attacker TTPs), operational (IR heads, network defenders; specific threats), technical (SOC staff, IR teams; specific IoCs, shortest lifespan). Lifecycle: planning and direction; collection; processing and exploitation; analysis and production; dissemination and integration}

**Cyber threat intelligence (CTI)** is the collection and analysis of information about threats and adversaries, so that an organisation can prepare for, prevent and respond to attacks. It turns unknown threats into known ones.

```diagram m01-intel
Four types, defined by who reads them. The arrows run from the boardroom down to the firewall rule.
```

| Type | What it covers | Consumed by |
| --- | --- | --- |
| Strategic | High-level: financial impact, attack trends, threat landscape, attribution | Executives, IT management, the CISO |
| Tactical | The TTPs of threat actors | IT service and security operations managers, NOC staff, administrators, architects |
| Operational | Specific threats against the organisation; context on incidents | Security managers, heads of incident response, network defenders, forensics and fraud teams |
| Technical | Specific IoCs: IP addresses, domains, hashes, phishing headers. Shortest-lived | SOC staff and incident response teams |

The **threat intelligence lifecycle** has five phases:

1. **Planning and direction**: decide what intelligence is needed and form the team.
2. **Collection**: gather raw data from open sources (OSINT), human sources (HUMINT) and others.
3. **Processing and exploitation**: turn raw data into a usable format.
4. **Analysis and production**: turn information into intelligence that is objective, timely, accurate and actionable.
5. **Dissemination and integration**: deliver it to the consumers and take their feedback.

!!! remember "Remember"
    Types, top of the organisation to the bottom: **S-T-O-T**: Strategic, Tactical, Operational, Technical. Lifecycle: "**P**lease **C**ollect, **P**rocess, **A**nalyse, **D**eliver."

!!! trap "Exam traps"
    - **Tactical** intelligence is about TTPs. **Technical** intelligence is about individual indicators. The names are easy to swap.
    - A piece of malware used in an attack is tactical; the hash of that malware is technical.

### Threat modelling {M: Threat modeling, five steps: identify security objectives; application overview; decompose the application; identify threats; identify vulnerabilities}

**Threat modelling** is a risk assessment approach for an application: capture, organise and analyse everything that affects its security. Five steps:

1. **Identify security objectives**: what must be protected, and which compliance rules apply.
2. **Application overview**: components, roles, key usage scenarios, technologies, security mechanisms.
3. **Decompose the application**: trust boundaries, data flows, entry points and exit points.
4. **Identify threats** relevant to that context.
5. **Identify vulnerabilities** related to those threats.

### Incident management {M: IH&R nine steps: preparation; incident recording and assignment; incident triage; notification; containment; evidence gathering and forensic analysis; eradication; recovery; post-incident activities. Incident response is part of incident handling, which is part of incident management}

**Incident management** is the set of processes that identify, analyse, prioritise and resolve security incidents, restore normal service and prevent recurrence. Incident **response** is one function of incident **handling**, which is one service within incident **management**.

**Incident handling and response (IH&R)** has nine steps.

```diagram m01-ihr
The nine steps. Containment comes before evidence gathering; eradication comes before recovery.
```

!!! exam "Exam answer / In practice"
    **Exam answer:** nine IH&R steps, in the order shown.

    **In practice:** many teams learned the shorter four-phase NIST model: preparation; detection and analysis; containment, eradication and recovery; post-incident activity. The nine steps are the same work, sliced more finely.

!!! update "Updated: April 2025"
    **What changed.** NIST replaced that four-phase guide. SP 800-61 **Revision 3**, published **April 2025**, supersedes Revision 2 (2012) and organises incident response around the functions of the NIST Cybersecurity Framework 2.0 (Govern, Identify, Protect, Detect, Respond, Recover) instead of a separate life cycle.

    **The exam still expects:** EC-Council's own nine IH&R steps. NIST's model is not what the question is asking for.

!!! remember "Remember"
    "**P**lease **R**ecord, **T**riage, **N**otify; **C**ontain, gather **E**vidence, **E**radicate, **R**ecover, **P**ost-mortem."

### AI and machine learning in defence {R}

**Machine learning (ML)** is the branch of AI that lets systems learn without being explicitly programmed. Defenders use it to learn what "normal" looks like and report deviations.

| Type | Uses | Subcategories |
| --- | --- | --- |
| Supervised learning {M: Supervised learning: labelled data; classification and regression. Unsupervised learning: unlabelled data; clustering and dimensionality reduction} | **Labelled** training data | Classification (separate classes), regression (continuous values) |
| Unsupervised learning | **Unlabelled** training data | Clustering, dimensionality reduction |

AI and ML help with password protection and authentication, phishing detection, threat detection, vulnerability management, behavioural analytics, network security, AI-based antivirus, fraud detection, botnet detection, and combating AI-driven threats.

!!! hospital "Worked example: ransomware in a hospital laboratory"
    At 02:10 on a Sunday the laboratory information system of a 300-bed hospital stops accepting samples. Every result screen shows a ransom note. Walk it through this chapter.

    1. **Which elements are hit?** Availability first: results cannot be issued. Then confidentiality, if patient records were copied out before encryption. Then integrity: can the restored results be trusted?
    2. **Where in the kill chain was it stoppable?** Delivery was a phishing email to a technician three weeks earlier. Installation and command and control ran unnoticed. The ransom note is "actions on objectives", the last link.
    3. **Which IH&R step are you in?** Recording and triage, then notification to management. **Containment** means disconnecting the lab network from the wards, while analysers keep running on paper request forms. Evidence is collected before anything is wiped.
    4. **Which risk level?** Extreme: imminent danger to patients. Immediate measures.
    5. **Which rules apply?** In the United States, HIPAA's Security Rule and breach duties. In the European Union, GDPR. In India, the Information Technology Act and the Digital Personal Data Protection Act 2023, whose main duties take effect in stages to May 2027.

    Change "laboratory" to "warehouse dispatch system" and "patients" to "deliveries": the five answers have the same shape. Only the law in step 5 and the cost of downtime change.

!!! try "Try it"
    Take three findings you would expect in any small office: a default router password, an unpatched web server, a shared admin login. Place each on the risk matrix above by likelihood and consequence. Which one do you fix first, and why?

!!! recap "Recap: section 5"
    - Defence in depth layers controls; the adaptive strategy protects, detects, responds and predicts.
    - Risk = threats × vulnerabilities × impact. Risk management: identify, assess, treat, track.
    - Threat intelligence: strategic, tactical, operational, technical; five-phase lifecycle.
    - Threat modelling: objectives, overview, decompose, threats, vulnerabilities.
    - IH&R: nine steps from preparation to post-incident activities.

## 6. Laws and standards {M}

A **law** is enforced by a country. A **standard** is a document agreed by consensus and approved by a recognised body. The exam asks which one protects what.

### The ones to know {M}

| Law or standard {M} | What it protects or requires | Key facts |
| --- | --- | --- |
| PCI DSS | Cardholder data, for anyone who stores, processes or transmits it | A proprietary industry standard, not a law. Failure can mean fines or losing the right to process cards |
| ISO/IEC 27001:2022 | Requirements for an information security management system (ISMS) | The standard organisations are certified against |
| HIPAA | Individually identifiable health information in the United States | Privacy Rule, Security Rule, Enforcement Rule; National Provider Identifier is a 10-digit number |
| Sarbanes-Oxley (SOX), 2002 | Investors: accuracy and reliability of corporate disclosures | 11 titles |
| DMCA | Copyright; bans circumventing technological protection measures | 5 titles; implements two 1996 WIPO treaties |
| FISMA, 2002 | Information security of United States federal agencies | Agency-wide security programmes |
| GDPR | Personal data of people in the European Union, wherever the organisation is | In effect 25 May 2018; seven principles |
| Data Protection Act 2018 | Personal data in the United Kingdom | Replaced the 1998 Act; sets the Information Commissioner's powers |

### Details worth a second look {R}

**ISO/IEC family.** 27001 is the ISMS requirements. The others the courseware lists: **27701** (privacy information management, extends 27001), **27002** (best-practice controls), **27005** (risk management), **27018** (personal data in public clouds), **27032** (internet security), **27033-7** (network virtualisation security), **27036-3** (supply chain security), **27040** (storage security).

**HIPAA's Administrative Simplification rules.** Electronic transactions and code set standards; Privacy Rule (limits on use and disclosure; patients' rights to their records); Security Rule (administrative, physical and technical safeguards for electronic health information); employer identifier standard; National Provider Identifier standard; Enforcement Rule.

**SOX titles to recognise.** I: Public Company Accounting Oversight Board. II: auditor independence. III: corporate responsibility; senior executives personally certify financial reports. IV: enhanced financial disclosures and internal controls. VIII: corporate and criminal fraud accountability, with whistle-blower protection. IX: white-collar crime penalties.

**DMCA titles.** I: WIPO treaty implementation, including the anti-circumvention rule. II: online copyright infringement liability limitation, the "safe harbour" for service providers. III: computer maintenance or repair. IV: miscellaneous provisions. V: protection of certain original designs (vessel hulls).

**GDPR's seven principles.** Lawfulness, fairness and transparency; purpose limitation; data minimisation; accuracy; storage limitation; integrity and confidentiality; accountability. {M: GDPR seven principles: lawfulness, fairness and transparency; purpose limitation; data minimisation; accuracy; storage limitation; integrity and confidentiality; accountability}

### Cyber law by country {R}

| Country | Laws to recognise |
| --- | --- |
| United States | Computer Fraud and Abuse Act; Electronic Communications Privacy Act; Foreign Intelligence Surveillance Act; Privacy Act of 1974; Computer Security Act of 1987; Freedom of Information Act; CCPA and the California Privacy Rights Act |
| United Kingdom | Computer Misuse Act 1990; Investigatory Powers Act 2016; Network and Information Systems Regulations 2018 |
| India | Information Technology Act; Patents, Trade Marks and Copyright Acts |
| Australia | Cybercrime Act 2001 |
| Germany | Criminal code sections 202a (data espionage), 303a (alteration of data), 303b (computer sabotage) |
| Canada | Criminal Code section 342.1; PIPEDA |
| Singapore | Computer Misuse Act |
| Brazil | General Data Protection Law (LGPD) |
| Philippines | Republic Act No. 10175 |

!!! exam "Exam answer / In practice"
    **Exam answer:** the table above is what the courseware lists.

    **In practice:** the official text prints a heading as "27701:2022" where it describes 27001:2022. Learn 27001 as the ISMS standard and 27701 as the privacy standard.

!!! update "Updated: laws and standards that have moved on"
    Each line gives what changed and when. The exam still expects the courseware's version, shown in the tables above.

    | Topic | What changed | When | Exam still expects |
    | --- | --- | --- | --- |
    | PCI DSS | Version 4.0.1 is the only active version; v3.2.1 and v4.0 are retired | Published **June 2024**; sole version from **31 December 2024** | "PCI DSS" by purpose: protects cardholder data |
    | ISO/IEC 27701 | New edition is a stand-alone privacy management standard, no longer an add-on to 27001 | **October 2025** | 27701:2019, an extension of 27001 |
    | HIPAA Security Rule | A major strengthening was proposed. It is **not final**; the current rule still applies | Proposed **January 2025**; final action now targeted for **July 2027** | The existing Privacy, Security and Enforcement Rules |
    | UK data protection | The Data (Use and Access) Act 2025 amends, and does not replace, the UK GDPR and the Data Protection Act 2018 | Royal Assent **June 2025**, phased in over the following year | Data Protection Act 2018 |
    | India | The Digital Personal Data Protection Act 2023 is now being brought into force through the DPDP Rules 2025 | Rules notified **November 2025**; further stages **November 2026** and **May 2027** | Information Technology Act |

    Status checked 18 November 2026. Laws change; check the regulator's own site before relying on any row.

!!! remember "Remember"
    Match by what is protected. **Cards**: PCI DSS. **Health**: HIPAA. **Investors**: SOX. **Copyright**: DMCA. **US federal agencies**: FISMA. **EU personal data**: GDPR. **Management system**: ISO 27001.

!!! try "Try it"
    Pick the organisation you work or study in. Write one line for each: which data it holds, which row of the table above applies, and who inside it is accountable. If you cannot name the person, that is your first finding.

!!! recap "Recap: section 6"
    - PCI DSS protects cardholder data and is a standard, not a law.
    - ISO/IEC 27001 defines the ISMS; 27701 adds privacy; 27005 covers risk.
    - HIPAA: health information, Privacy and Security Rules. SOX: 11 titles, corporate disclosures. DMCA: 5 titles, anti-circumvention.
    - FISMA covers US federal agencies. GDPR took effect 25 May 2018 and has seven principles.
    - Know one headline law per country, such as the UK Computer Misuse Act 1990 and India's IT Act.

## 7. Lab walk-through {D}

There is nothing to break in this module. The practical skill is behaving like a professional before any testing starts. Use lab L01 in either skin. Allow 45 minutes.

```bash
# 1. Start the lab and open the attacker shell
cd labs/L01-recon-enumeration
docker compose up -d --build
docker compose exec attacker bash

# 2. Inside the attacker container: confirm where you are and what you may touch
hostname -I            # your own address
cat /etc/resolv.conf   # the lab's name server

# 3. Make one harmless, in-scope request
curl -s -D - -o /dev/null http://10.77.0.20/
exit

# 4. Back on your own computer: find your request in the target's log
docker compose logs --tail 5 h20

# 5. Stop the lab
docker compose down
```

Then write half a page in your log, answering:

1. **Authorisation.** From the student brief: what is in scope, what is forbidden, what is the deliverable?
2. **Framework.** Which phase of the CEH framework was step 3? Which kill-chain phase?
3. **Elements.** The response headers revealed a software version. Which of the five elements does that weaken, and how?
4. **Indicators.** Classify the log line from step 4 as an IoC: atomic, computed or behavioural, and which category?
5. **Risk.** Give "web server announces its exact version" a likelihood, a consequence and a risk level.

That half page is your first piece of professional documentation. Keep it; later modules add to it.

## Quiz

Twelve questions. The options are shuffled every time you load the page.

```quiz
Q: Which element of information security does a digital signature mainly provide?
- Availability
- Confidentiality
- * Non-repudiation
- Data minimisation
WHY: A digital signature stops the sender denying they sent the message. Encryption gives confidentiality.
TAG: M

Q: An attacker reads a manager's password over her shoulder in a cafe. Under the IATF classification this is which kind of attack?
- Passive
- * Close-in
- Insider
- Distribution
WHY: Close-in attacks depend on physical proximity. Shoulder surfing and dumpster diving are the standard examples.
TAG: M

Q: A hacker with strong skills attacks a power grid for a cause and does not care about going to prison. Which class?
- Script kiddie
- Gray hat
- * Suicide hacker
- Blue hat
WHY: Indifference to punishment is what defines a suicide hacker.
TAG: M

Q: What must an ethical hacker have before starting any test?
- A list of open ports
- * A signed document from the client giving permission
- An exploit for a known vulnerability
- Verbal approval from the help desk
WHY: Signed authorisation is the line between ethical hacking and a crime. An NDA and agreed limits follow.
TAG: M

Q: In the cyber kill chain, an attacker combines an exploit with a backdoor into a malicious document. Which phase is this?
- Delivery
- * Weaponization
- Installation
- Exploitation
WHY: Building the payload is weaponization. Sending it is delivery; the code running is exploitation.
TAG: M

Q: Which of these is a computed indicator of compromise?
- An IP address
- An email address
- * A file hash
- A domain name
WHY: Computed indicators are derived from incident data, such as hash values and regular expressions. Addresses are atomic.
TAG: M

Q: Which is NOT one of the four core features of the Diamond Model?
- Adversary
- Capability
- Infrastructure
- * Motive
WHY: The four are adversary, capability, infrastructure and victim. Motive appears in the extended model as the socio-political meta-feature.
TAG: M

Q: Threat intelligence describing the tactics, techniques and procedures of an attack group is which type?
- Strategic
- * Tactical
- Operational
- Technical
WHY: Tactical intelligence covers TTPs. Technical intelligence covers individual indicators such as hashes and IP addresses.
TAG: M

Q: In incident handling and response, which step comes directly after notification?
- Eradication
- Recovery
- * Containment
- Triage
WHY: The order is preparation, recording, triage, notification, containment, evidence gathering, eradication, recovery, post-incident.
TAG: M

Q: A US clinic emails unencrypted patient records to the wrong recipient. Which regulation is most directly engaged?
- SOX
- PCI DSS
- * HIPAA
- DMCA
WHY: HIPAA protects individually identifiable health information. PCI DSS is cards, SOX is corporate disclosures, DMCA is copyright.
TAG: M

Q: Why does defence in depth use several layers of control?
- To reduce the number of logs
- * So that defeating one layer only brings the attacker to the next
- Because a single control is always illegal
- To remove the need for monitoring
WHY: Layers slow the attacker and give defenders time to detect and respond.
TAG: U

Q: The courseware describes WormGPT as a helpful testing aid. What is the sound professional view?
- Use it on client systems to save time
- * Recognise the name for the exam, and do not use criminal-market tools at work
- It replaces the need for authorisation
- It is the same product as ShellGPT
WHY: Exam answers follow the courseware's descriptions. In practice WormGPT was sold to criminals; use ordinary tools inside your authorisation.
TAG: U
```

## Exam cheat sheet

Only the MEMORISE items from this chapter, collected automatically.

[[cheatsheet]]

## Coverage check against the official Module 1

Each sub-topic of the official module and where this chapter covers it. The section-by-section verification report is kept with the handbook source as `verification/ceh/m01-introduction-to-ethical-hacking.md`. No official text is reproduced.

| Official sub-topic | Covered in | Status |
| --- | --- | --- |
| Elements of information security | 1 | OK, exam/practice note on five vs three |
| Attacks: motives, goals, objectives; TTPs; vulnerability and its causes | 1 | OK |
| Classification of attacks | 1 | OK |
| Information warfare | 1 | OK |
| What is hacking; who is a hacker; hacker classes | 2 | OK |
| What is ethical hacking; why it is necessary; scope and limitations; skills | 2 | OK, exam/practice note on "always legal" |
| AI-driven ethical hacking: benefits, applications, how it helps, the myth | 3 | OK |
| ChatGPT-powered AI tools | 3 | OK, exam/practice note on criminal tools |
| CEH ethical hacking framework | 4 | OK, exam/practice note on older phase list |
| Cyber kill chain methodology | 4 | OK |
| TTPs; adversary behavioural identification; indicators of compromise and their categories | 1, 4 | OK |
| MITRE ATT&CK framework | 4 | OK, exam/practice note on PRE-ATT&CK |
| Diamond Model of Intrusion Analysis, including the extended model | 4 | OK |
| Information assurance; continual/adaptive security strategy; defence in depth | 5 | OK |
| Risk, risk level, risk matrix, risk management | 5 | OK |
| Cyber threat intelligence: types and lifecycle | 5 | OK |
| Threat modelling | 5 | OK |
| Incident management; incident handling and response | 5 | OK, exam/practice note on NIST model |
| Role of AI and ML in cyber security | 5 | OK |
| PCI DSS, ISO/IEC standards, HIPAA, SOX, DMCA, FISMA, GDPR, DPA 2018 | 6 | OK |
| Cyber law in different countries | 6 | OK, reduced to headline laws |
| Module summary | Recaps and cheat sheet | OK |

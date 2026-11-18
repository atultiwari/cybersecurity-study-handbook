"""Diagrams for CEH Module 7, Malware Threats. All original."""
from diagrams import diagram, ladder, pair, single, tree, bar


@diagram("m07-family")
def family():
    rows = [(0, "Malware: software written to harm, spy or take control"),
            (1, "Needs a host program and a person to run it"),
            (2, "Virus: copies itself into other files"),
            (2, "Trojan: harmful code hidden inside something that looks useful"),
            (1, "Spreads by itself across the network"),
            (2, "Worm: exploits a weakness, copies itself to the next machine"),
            (1, "Named for what it does once inside"),
            (2, "Ransomware, spyware, adware, keylogger, backdoor, rootkit, botnet client"),
            (1, "Leaves little or nothing on disk"),
            (2, "Fileless malware: runs in memory through tools already on the system")]
    return tree(rows, "The main families of malware, grouped by how they arrive and what they do", w=760, rh=34, ind=26)


@diagram("m07-apt")
def apt():
    return ladder([("1. Preparation", "Choose the target, research it, build or buy tools, test against detection."),
                   ("2. Initial intrusion", "Spear-phishing email or an exploited public server; malware calls out."),
                   ("3. Expansion", "Gather credentials, raise privileges, reach more systems."),
                   ("4. Persistence", "Custom malware and hiding places keep access for months."),
                   ("5. Search and exfiltration", "Find the data and take it out, often encrypted."),
                   ("6. Cleanup", "Remove evidence and restore file attributes to hide the visit.")],
                  "The six phases of the advanced persistent threat lifecycle", w=760, bw=210)


@diagram("m07-reverse")
def reverse():
    m = [(0, 0, "A firewall blocks connections coming in to the victim", "note"),
         (1, 0, "Blocked: attacker tries to connect in", "x"),
         (0, 1, "Allowed: the Trojan connects out, for example on port 80"),
         (1, 0, "Commands travel back down the connection the victim opened"),
         (0, 1, "Screens, keystrokes and files go to the attacker")]
    return single(("Victim", "Attacker"), m,
                  "A reverse-connecting remote access Trojan gets round an inbound firewall", gap=430)


@diagram("m07-infect")
def infect():
    return ladder([("1. Create", "Build a new Trojan with a construction kit, so no signature exists yet."),
                   ("2. Dropper or downloader", "Carrier that installs the Trojan (dropper) or fetches it (downloader)."),
                   ("3. Wrapper", "Bind the Trojan to a harmless-looking program."),
                   ("4. Crypter", "Encrypt it to hide from antivirus."),
                   ("5. Propagate", "Send it by email, covert channel, proxy, USB drive or exploit kit."),
                   ("6. Deploy", "The victim runs the carrier; the wrapped, encrypted Trojan lands."),
                   ("7. Damage routine", "The payload executes.")],
                  "The seven steps an attacker follows to infect a system with a Trojan", w=760, bw=220)


@diagram("m07-viruslife")
def viruslife():
    return ladder([("1. Design", "Written in a programming language or with a construction kit."),
                   ("2. Replication", "Copies itself within the target for a period, then spreads."),
                   ("3. Launch", "Activated when the user runs an infected program."),
                   ("4. Detection", "Identified as a threat to target systems."),
                   ("5. Incorporation", "Antivirus makers add a defence to their products."),
                   ("6. Execution of the damage routine", "Users update antivirus and remove the threat.")],
                  "The six stages of the virus lifecycle, from design to elimination", w=760, bw=270)


@diagram("m07-virusworm")
def virusworm():
    left = ("Virus", [(0, 0, "A person runs an infected file", "note"), (0, 1, "Code attaches to other files"),
                      (0, 0, "Spreads only when files are shared", "note")])
    right = ("Worm", [(0, 0, "No person needed", "note"), (0, 1, "Scans, exploits a weakness, copies itself"),
                      (1, 1, "The new copy repeats the cycle", "note")])
    return pair(left, right, lanes=("Infected host", "Next host"),
                label="A virus needs a person to run an infected file; a worm spreads across the network by itself")


@diagram("m07-fileless")
def fileless():
    return ladder([("1. Point of entry", "Memory exploit, malicious website, or phishing email with a booby-trapped document."),
                   ("2. Code execution", "Code injection or a script run through PowerShell, mshta or WScript."),
                   ("3. Persistence", "Script stored in the registry, WMI or Task Scheduler to survive a reboot."),
                   ("4. Achieving objectives", "Data theft, credential stealing, reconnaissance, spying.")],
                  "The four stages of a fileless malware attack", w=780, bw=200)


@diagram("m07-packed")
def packed():
    return bar([(2, "Unpacking stub", "runs first", "t"), (6, "Packed original program", "compressed or encrypted; unreadable on disk", "d")],
               "A packed executable: a small stub in front of the hidden original program", w=700,
               note="When run, the stub unpacks the original into memory and hands control to it.")


@diagram("m07-analysis")
def analysis():
    return ladder([("Prepare the testbed", "Isolated virtual machine, host-only network, snapshot, tools installed."),
                   ("Static analysis", "Do not run it. Hash, scan, strings, packer, PE details, dependencies, disassembly."),
                   ("Dynamic analysis", "Run it and watch. Baseline first, then ports, processes, registry, files, network.")],
                  "The malware analysis procedure: testbed, static analysis, dynamic analysis", w=780, bw=190)

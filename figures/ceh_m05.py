"""Diagrams for CEH Module 5, Vulnerability Analysis. All original."""
from diagrams import diagram, ladder, pair, tree, flow


@diagram("m05-where")
def where():
    return ladder([("Scanning", "Module 3. Which hosts are up and which ports are open?"),
                   ("Enumeration", "Module 4. What does each service say about itself: versions, users, shares?"),
                   ("Vulnerability analysis", "This module. Which of those versions and settings have a known weakness?"),
                   ("System hacking", "Module 6. Use one of those weaknesses to get in.")],
                  "Where vulnerability analysis sits between enumeration and system hacking", w=720, bw=190)


@diagram("m05-labels")
def labels():
    return ladder([("CWE", "The kind of mistake. Example: CWE-89, SQL injection, as a class of flaw."),
                   ("CVE", "One instance of it in one product. Example: CVE-2017-0144, a single SMB bug."),
                   ("CVSS", "How bad that instance is, as a score from 0.0 to 10.0 and a vector string."),
                   ("NVD", "The library that files the CVE with its CVSS score, CWE and affected products.")],
                  "Four labels for one flaw: CWE, CVE, CVSS and NVD", w=720, bw=110)


@diagram("m05-cvss")
def cvss():
    rows = [(0, "CVSS v4.0 score"),
            (1, "Base: what the flaw is, fixed over time and place"),
            (2, "Exploitability: Attack Vector, Complexity and Requirements; Privileges Required; User Interaction"),
            (2, "Impact: confidentiality, integrity, availability of the Vulnerable and Subsequent Systems"),
            (1, "Threat: what is happening now"),
            (2, "Exploit Maturity"),
            (1, "Environmental: what it means for one organisation"),
            (2, "Modified Base metrics plus confidentiality, integrity and availability requirements"),
            (1, "Supplemental: extra context, does not change the score"),
            (2, "Automatable, Recovery, Value Density, Vulnerability Response Effort, Provider Urgency, Safety")]
    return tree(rows, "The four metric groups of CVSS version 4.0 and the metrics in each", w=810, rh=34, ind=26)


@diagram("m05-lifecycle")
def lifecycle():
    n = {"a": (150, 40, 250, 44, "Pre-assessment\nIdentify assets, create a baseline", "t"),
         "b": (150, 130, 250, 44, "Vulnerability assessment\nScan, then analyse", "b"),
         "c": (150, 220, 250, 44, "Risk assessment\nRank what was found", "b"),
         "d": (150, 310, 250, 44, "Remediation\nPatch, fix or accept the risk", "b"),
         "e": (150, 400, 250, 44, "Verification\nRescan: did the fix work?", "b"),
         "f": (150, 490, 250, 44, "Monitoring\nWatch for the next weakness", "b"),
         "g": (500, 265, 190, 56, "Post-assessment:\nthese four steps", "d")}
    e = [("a", "b", "", "v"), ("b", "c", "", "v"), ("c", "d", "", "v"), ("d", "e", "", "v"), ("e", "f", "", "v"),
         ("f", "a", "", "M25 490H8V40H22"), ("g", "c", "", "M500 237V220H278"), ("g", "f", "", "M500 293V490H278")]
    return flow(n, e, 620, 525, "The vulnerability-management life cycle: pre-assessment, assessment and four post-assessment steps, repeated")


@diagram("m05-scanner")
def scanner():
    return ladder([("1. Locate nodes", "Find the live hosts in the target range (Module 3 host discovery)."),
                   ("2. Discover services and OS", "List open ports, the service on each and the operating system."),
                   ("3. Test for known flaws", "Compare what was found with a database of known vulnerabilities.")],
                  "The three steps every vulnerability scanner performs", w=720, bw=230)


@diagram("m05-activepassive")
def activepassive():
    left = ("Active scanning", [(0, 1, "Probe: crafted request to port 445"), (1, 0, "Reply reveals an unpatched service"),
                               (0, 0, "The target sees the scanner", "note")])
    right = ("Passive scanning", [(1, 1, "Target talks to others as usual", "note"), (1, 0, "Scanner only listens to that traffic"),
                                 (0, 0, "Versions inferred, nothing sent", "note")])
    return pair(left, right, lanes=("Scanner", "Target"), label="Active scanning sends probes to the target; passive scanning only observes its normal traffic")


@diagram("m05-report")
def report():
    rows = [(0, "Vulnerability assessment report"),
            (1, "Executive summary: scope, objectives, testing narrative, findings summary, remediation summary"),
            (1, "Assessment overview: methodology, scan information, target information, tools"),
            (1, "Findings: each host, its vulnerable services, CVE ID, CVSS score, impact, fix"),
            (1, "Risk assessment: findings ranked critical, high, moderate or low"),
            (1, "Recommendations: prioritised action plan, root cause, patches, lessons learned"),
            (1, "Appendices, conclusion, follow-up timeline, glossary")]
    return tree(rows, "The sections of a vulnerability assessment report", w=760, rh=36, ind=28)

"""Diagrams for CEH Module 4, Enumeration. All original."""
from diagrams import diagram, ladder, pair, single, tree, bar, svg, text


@diagram("m04-where")
def where():
    return ladder([("Footprinting", "Module 2. What is published about the organisation? Mostly without touching it."),
                   ("Scanning", "Module 3. Which hosts are up and which ports are open?"),
                   ("Enumeration", "This module. Log in to each open service and ask it to list what it knows."),
                   ("Vulnerability analysis", "Module 5. Which of those services, versions and accounts are weak?")],
                  "Where enumeration sits between scanning and vulnerability analysis", w=700, bw=180)


@diagram("m04-nbname")
def nbname():
    return bar([(15, "15 characters", "the device name, padded with spaces", "t"),
                (3, "16th", "service code", "d")],
               "A NetBIOS name is 16 characters: 15 for the name and one for the service type", w=660,
               note="Example: FILESRV01 plus code 20 means \"the file server service on FILESRV01\".")


@diagram("m04-snmp")
def snmp():
    m = [(0, 1, "GetRequest: what is the value of this object?"), (1, 0, "Response: the value"),
         (0, 1, "GetNextRequest: and the next object in the tree?"), (1, 0, "Response"),
         (0, 1, "SetRequest: change this value (needs the read/write string)"), (1, 0, "Response"),
         (0, 0, "Unprompted, when something happens:", "note"),
         (1, 0, "Trap: \"I have just rebooted\" (sent to port 162)")]
    return single(("SNMP manager", "SNMP agent"), m, "SNMP messages between a manager and an agent", gap=420)


@diagram("m04-mib")
def mib():
    rows = [(0, "iso (1)"), (1, "org (3)"), (2, "dod (6)"), (3, "internet (1)"),
            (4, "mgmt (2)"), (5, "mib-2 (1)"), (6, "system (1)"),
            (7, "sysDescr (1)   =   1.3.6.1.2.1.1.1"), (7, "sysContact (4)   =   1.3.6.1.2.1.1.4")]
    return tree(rows, "The MIB is a tree; an OID is the path of numbers from the root to one object", w=640, rh=34, ind=28)


@diagram("m04-ldap")
def ldap():
    rows = [(0, "dc=example,dc=com  (the root: its naming context)"),
            (1, "ou=People"),
            (2, "cn=Asha Verma  (sAMAccountName=averma, mail, department)"),
            (2, "cn=svc_backup  (a service account)"),
            (1, "ou=Groups"),
            (2, "cn=Domain Admins  (member=cn=...)"),
            (1, "ou=Servers"),
            (2, "cn=FILESRV01")]
    return tree(rows, "An LDAP directory is a tree of entries, each with attributes", w=660)


@diagram("m04-vrfy")
def vrfy():
    left = ("The account exists", [(0, 1, "VRFY svc_backup"), (1, 0, "250 svc_backup@... : confirmed")])
    right = ("No such account", [(0, 1, "VRFY nobody"), (1, 0, "550 user unknown")])
    return pair(left, right, lanes=("You", "Mail server"), label="An SMTP server answering VRFY differently for valid and invalid users")


@diagram("m04-snoop")
def snoop():
    left = ("Record is in the cache", [(0, 1, "A record for bank.example? (no recursion)"), (1, 0, "Answer from cache: someone here asked before")])
    right = ("Record is not in the cache", [(0, 1, "A record for bank.example? (no recursion)"), (1, 0, "No answer, only a referral")])
    return pair(left, right, lanes=("You", "DNS resolver"), label="Non-recursive DNS cache snooping: a cached record versus an uncached one")


@diagram("m04-nfs")
def nfs():
    return ladder([("rpcinfo -p <target>", "Ask the portmapper (port 111) which RPC services run, and on which ports."),
                   ("showmount -e <target>", "Ask the NFS server which directories it exports, and to whom."),
                   ("Mount the export", "Before version 4 the only credential is the client's IP address."),
                   ("Read what is there", "File names, owners and contents: the enumeration result.")],
                  "The steps of NFS enumeration", w=700, bw=200)

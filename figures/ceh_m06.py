"""Diagrams for CEH Module 6, System Hacking. All original."""
from diagrams import diagram, ladder, pair, single, tree, bar


@diagram("m06-phases")
def phases():
    return ladder([("1. Gaining access", "Crack a password or exploit a weakness to get a first foothold."),
                   ("2. Escalating privileges", "Turn an ordinary account into administrator, root or SYSTEM."),
                   ("3. Maintaining access", "Run programs, hide files, and make sure the way back in survives."),
                   ("4. Clearing logs", "Switch off auditing, remove or edit records, hide what was left.")],
                  "The four phases of system hacking, in order", w=780, bw=220)


@diagram("m06-ntlm")
def ntlm():
    m = [(0, 1, "1. Logon request: user name and domain"),
         (1, 0, "2. Challenge: a random number"),
         (0, 1, "3. Response: the challenge encrypted with the password hash"),
         (1, 2, "4. User name, challenge and response passed on"),
         (2, 2, "The controller repeats the sum with its stored hash", "note"),
         (2, 1, "5. Match or no match"),
         (1, 0, "6. Access granted or refused")]
    return single(("Client", "Server", "Domain controller"), m,
                  "NTLM challenge and response in a domain: only the hash is ever used", gap=270)


@diagram("m06-kerberos")
def kerberos():
    m = [(0, 1, "1. Request to the Authentication Server, proved with the user's key"),
         (1, 0, "2. Ticket Granting Ticket (TGT)"),
         (0, 1, "3. TGT presented to the Ticket Granting Server, naming a service"),
         (1, 0, "4. Service ticket"),
         (0, 2, "5. Service ticket presented to the service"),
         (2, 0, "6. Access; the service never contacts the KDC")]
    return single(("Client", "KDC (AS + TGS)", "Service"), m,
                  "Kerberos: one logon gives a TGT, and the TGT is exchanged for a ticket per service", gap=290)


@diagram("m06-pwtypes")
def pwtypes():
    rows = [(0, "Password attacks"),
            (1, "Non-electronic: no technical skill needed"),
            (2, "Shoulder surfing, social engineering, dumpster diving"),
            (1, "Active online: the attacker talks to the target"),
            (2, "Guessing, dictionary, brute force, spraying, mask, default passwords"),
            (2, "Hash injection, LLMNR/NBT-NS poisoning, Kerberos cracking, NTLM relay"),
            (1, "Passive online: the attacker only listens"),
            (2, "Wire sniffing, man-in-the-middle, replay"),
            (1, "Offline: the attacker works on stolen hashes"),
            (2, "Rainbow tables, distributed network attack")]
    return tree(rows, "The four families of password attack and the techniques in each", w=780, rh=34, ind=26)


@diagram("m06-llmnr")
def llmnr():
    m = [(0, 1, "1. Where is \\\\fileservr? (mistyped name)"),
         (1, 0, "2. DNS: no such name"),
         (0, 0, "3. Victim asks the whole local network: LLMNR UDP 5355, NBT-NS UDP 137", "note"),
         (2, 0, "4. Listener answers: that is me"),
         (0, 2, "5. Victim tries to log on: NTLMv2 challenge and response"),
         (2, 2, "6. The response is saved and cracked offline", "note")]
    return single(("Victim", "DNS server", "Attacker's listener"), m,
                  "LLMNR and NBT-NS poisoning: a failed name lookup ends with a captured logon response", gap=280)


@diagram("m06-roast")
def roast():
    left = ("Kerberoasting", [(0, 0, "Needs any ordinary domain account", "note"),
                              (0, 1, "Request a service ticket for an SPN"),
                              (1, 0, "Ticket, encrypted with the service account's hash"),
                              (0, 0, "Crack offline: service account password", "note")])
    right = ("AS-REP roasting", [(0, 0, "Needs only a user name", "note"),
                                 (0, 1, "Request logon for a no-pre-auth user"),
                                 (1, 0, "Reply, encrypted with that user's hash"),
                                 (0, 0, "Crack offline: that user's password", "note")])
    return pair(left, right, lanes=("Attacker", "KDC"),
                label="Kerberoasting targets service accounts; AS-REP roasting targets users without pre-authentication")


@diagram("m06-salt")
def salt():
    return bar([(3, "Without a salt", "hash(password): the same for every user; a table matches", "b"),
                (4, "With a salt", "hash(salt + password): different for every user; no table matches", "t")],
               "A salt is a random value stored beside the hash that makes precomputed tables useless", w=780,
               note="The salt is not secret. Its only job is to make each stored hash unique.")


@diagram("m06-exploit")
def exploit():
    return ladder([("1. Identify the vulnerability", "From scanning and vulnerability analysis in earlier modules."),
                   ("2. Determine the risk", "What would using it expose or break?"),
                   ("3. Determine the capability", "Can it be used, and what would it give?"),
                   ("4. Develop the exploit", "Write one, or find and adapt a published one."),
                   ("5. Select the delivery method", "Local, from an account on the machine, or remote, over the network."),
                   ("6. Generate and deliver the payload", "The code that runs once the flaw has been used."),
                   ("7. Gain remote access", "A session on the target.")],
                  "The seven steps of exploiting a vulnerability", w=780, bw=270)


@diagram("m06-stack")
def stack():
    return bar([(4, "Buffer", "space for the expected input", "b"),
                (2, "Saved EBP", "base of the caller's frame", "b"),
                (2, "Return address", "loaded into EIP on return", "d"),
                (3, "Rest of the stack", "where injected code may sit", "t")],
               "A stack frame: input longer than the buffer runs on over the saved return address", w=780,
               note="Input is written from left to right. Too much of it overwrites the return address, and so the EIP.")


@diagram("m06-bof")
def bof():
    return ladder([("1. Spiking", "Which command crashes the program?"),
                   ("2. Fuzzing", "Roughly how many bytes cause the crash?"),
                   ("3. Identify the offset", "Exactly which bytes land in the EIP?"),
                   ("4. Overwrite the EIP", "Prove control with a chosen value."),
                   ("5. Identify bad characters", "Which byte values must the final code avoid?"),
                   ("6. Identify the right module", "An unprotected library with a jump to the stack."),
                   ("7. Generate shellcode", "The payload, without the bad characters."),
                   ("8. Gain root access", "Send it and receive a shell.")],
                  "The eight steps of a Windows buffer overflow exploit", w=780, bw=250, rh=46)


@diagram("m06-rings")
def rings():
    rows = [(0, "Where a rootkit can live, from the top down"),
            (1, "Ring 3: applications"),
            (2, "Application-level (user-mode) and library-level rootkits"),
            (1, "Ring 0: the operating system kernel"),
            (2, "Kernel-level rootkits: drivers and loadable modules"),
            (1, "Before the operating system starts"),
            (2, "Boot-loader-level rootkits (bootkits)"),
            (1, "Ring -1: beneath the operating system"),
            (2, "Hypervisor-level rootkits"),
            (1, "The machine itself"),
            (2, "Hardware and firmware rootkits")]
    return tree(rows, "Rootkit types arranged by how deep in the system they sit", w=760, rh=34, ind=26)


@diagram("m06-ads")
def ads():
    return bar([(3, "report.txt", "main stream: 2 KB, shown in listings", "b"),
                (5, "report.txt:tool.exe", "alternate stream: 4 MB, not shown", "d")],
               "One NTFS file with a second, named data stream that a normal listing does not show", w=760,
               note="The visible size stays 2 KB. Only the modification time changes.")


@diagram("m06-stego")
def stego():
    rows = [(0, "Steganography"),
            (1, "Technical"),
            (2, "Invisible ink, microdots, computer-based methods"),
            (1, "Linguistic"),
            (2, "Semagrams: signs and symbols"),
            (3, "Visual semagrams; text semagrams"),
            (2, "Open codes: innocent-looking text"),
            (3, "Jargon codes"),
            (3, "Covered ciphers: null cipher, grille cipher")]
    return tree(rows, "Classification of steganography into technical and linguistic kinds", w=700, rh=34, ind=28)


@diagram("m06-tracks")
def tracks():
    rows = [(0, "Covering tracks"),
            (1, "1. Disabling auditing"),
            (1, "2. Clearing logs"),
            (1, "3. Manipulating logs"),
            (1, "4. Covering tracks on the network"),
            (1, "5. Covering tracks on the operating system"),
            (1, "6. Deleting files"),
            (1, "7. Disabling Windows functionality"),
            (1, "8. Hiding artifacts")]
    return tree(rows, "The eight techniques for covering tracks", w=620, rh=32, ind=28)

---
title: Module 2 - Footprinting and Reconnaissance
book: Ethical Hacking Study Handbook
module: 2
kicker: Ethical hacking track · Module 2 of 20
home: index.html
lab: 60
difficulty: Beginner
status: Review draft
verified: 18 Nov 2026: CEH v13 courseware Module 02, ICANN, Google Search Central, RFC 8482
footer: Unofficial, independent study material. Not affiliated with or endorsed by EC-Council. CEH, CPENT and COASP are trademarks of EC-Council. Written in our own words from public standards and tool documentation. Use these techniques only on systems you own or are authorised in writing to test.
---

# Footprinting and Reconnaissance

[[meta]]

## What this chapter is about

Footprinting is the homework you do before you touch anything. You start with the name of an organisation. You finish with a profile: its domain names, its internet addresses, the people who work there, the technology it runs, and the places where it has told the world more than it meant to.

!!! story "An everyday picture"
    A sales representative has a first meeting with a company next week. She reads its website and its annual report. She looks up the directors on a professional network, checks the news, and finds the office on a street-view map so she knows which door to use. The company has no idea any of this happened. That is **passive** footprinting. Then she phones reception and asks who looks after the IT contract. Now the company could notice her. That is **active** footprinting.

Attackers do exactly this, with different intentions. Ethical hackers do it first, with permission, so the organisation can see itself the way a stranger does and tidy up.

!!! before "Before you start"
    This chapter assumes five ideas. The one-line version is enough to carry on.

    - **Domain name.** The readable name of an organisation on the internet, such as `example.com`. A **subdomain** is a name inside it, such as `mail.example.com`.
    - **IP address.** The number that identifies a machine on a network, such as `10.77.0.20`.
    - **DNS.** The internet's phone book. It turns names into IP addresses. Section 6 teaches the parts you need.
    - **Search engine index.** The giant catalogue a search engine builds by visiting web pages with automated programs called crawlers.
    - **Metadata.** Data about data: the author name, software version and date stored inside a document or photo.

    You do not need Module 1. Where this chapter leans on it, it says so.

!!! why "Why this matters to you"
    - **Exam candidate.** Expect questions that describe a task and ask for the tool or the search operator, and questions on Whois, DNS record types and traceroute. The newer questions show an AI prompt and ask which command it produces.
    - **Defending a network.** Almost everything here uses information your organisation published itself. Running these steps against your own name is the cheapest security review you will ever do. Section 10 is written for you.
    - **Working with sensitive data.** If you work in a hospital, a bank or a school, staff pages, job adverts and shared documents describe your systems to strangers. This chapter shows what they can piece together, and why "it is only our public website" is not a defence.

### How the tags work

[[legend]]

Facts tagged MEMORISE are collected automatically into the [cheat sheet](#exam-cheat-sheet) at the end.

**How to use this chapter.** Read sections 1 and 2 first; the rest can be taken in any order. Run each "Try it" box in lab L01. The lab has no internet connection, so where a technique needs the internet the box says so and names a safe target: a domain you own, or `example.com`, which is reserved for examples. Finish with the lab walk-through and the quiz.

| After this chapter you can | Section |
| --- | --- |
| Tell passive from active footprinting and list what each collects | 1 |
| Write a search query with advanced operators and explain the Google Hacking Database | 2 |
| Match an online research service to the information it gives | 3 |
| Describe what social networks and email harvesting reveal | 4 |
| Read a Whois record and name the regional registries | 5 |
| Name the DNS record types and perform a zone transfer | 6 |
| Explain traceroute and read an email header | 7 |
| Recognise the footprinting tools, including the AI-assisted ones | 8, 9 |
| Recommend countermeasures | 10 |

## 1. Footprinting concepts {U}

**Footprinting** is collecting as much information as possible about a target organisation and its network before any attack or test begins. The result is a **blueprint** of the organisation's security profile. The courseware uses **reconnaissance** as another word for the same thing.

There is no single fixed method, because the information can be found in many ways. What matters is that the work is organised, so nothing is collected twice and nothing is missed.

```diagram m02-funnel
Footprinting narrows a name down, step by step, to things that can be tested.
```

### Passive and active {M: Footprinting types: passive = no direct interaction (OSINT, proprietary databases and paid services, intelligence shared by partners); active = direct interaction (DNS interrogation, social engineering, network and port scanning, user and service enumeration). Reconnaissance = footprinting (exam)}

```diagram m02-types
The two kinds of footprinting. The dividing line is whether the target could notice you.
```

| Type | How | Includes |
| --- | --- | --- |
| Passive footprinting | No direct interaction. You read what is already stored somewhere else | Open-source intelligence (**OSINT**), proprietary databases and paid services, intelligence shared by partner organisations or industry groups |
| Active footprinting | Direct interaction. The target may recognise what is happening | DNS interrogation, social engineering, network and port scanning, user and service enumeration |

Passive footprinting only finds what has been archived or published. Active footprinting finds more, needs more preparation, and may leave traces that alert the target.

!!! exam "Exam answer / In practice"
    **Exam answer:** reconnaissance and footprinting are the same thing, and it is the **first step** of ethical hacking. Port scanning and enumeration appear in the courseware's list of **active footprinting** activities.

    **In practice:** testers treat scanning (Module 3) and enumeration (Module 4) as separate phases that come after footprinting. Module 1's attack classes also list footprinting as a **passive** attack. If a question asks for the class of attack, answer passive; if it asks what active footprinting includes, the list above is the answer.

```diagram m02-choose
A working rule. Passive steps need care; active steps need permission.
```

### What footprinting collects {M: Footprinting collects three kinds of information: organization (employees, addresses, phone numbers, partners, web technologies, press releases, patents); network (domains and subdomains, network blocks, topology, reachable IP addresses, Whois and DNS records); system (web server OS, server locations, public email addresses, usernames and passwords)}

| Kind | Examples | Where it comes from |
| --- | --- | --- |
| Organisation information | Employee names, job titles and contact details; addresses and phone numbers; branches; partners; web technologies; news, press releases, legal documents, patents and trademarks | The organisation's own website, Whois |
| Network information | Domains and subdomains; network blocks; topology, trusted routers and firewalls; IP addresses of reachable systems; Whois and DNS records | Whois database analysis, traceroute |
| System information | Web server operating system; location of web servers; publicly available email addresses; usernames and passwords | Network, DNS, website and email footprinting |

### Objectives and threats {M: Six footprinting threats: social engineering; system and network attacks; information leakage; privacy loss; corporate espionage; business loss}

Footprinting has four **objectives**: {U}

1. Learn the **security posture**: where firewalls, proxies and other defences sit.
2. **Reduce the focus area** from "an organisation" to specific domain names, network blocks and individual IP addresses.
3. **Identify vulnerabilities** so the right exploits can be chosen.
4. Build an **information database** of weaknesses that points to the weakest link.

The courseware lists six **threats** that footprinting makes possible:

| Threat | In one line |
| --- | --- |
| Social engineering | Staff who do not know the caller's intent hand over information willingly |
| System and network attacks | Knowing the configuration and operating system leads straight to its known flaws |
| Information leakage | Sensitive information reaches an attacker, who uses or sells it |
| Privacy loss | Access gained with the help of footprinting exposes the organisation and its people |
| Corporate espionage | Competitors use what they learn to copy products and undercut prices |
| Business loss | Online shops, banks and finance firms lose money to the attacks that follow |

!!! remember "Remember"
    Three kinds of information: **O-N-S**, Organisation, Network, System: "**O**utsiders **N**otice **S**tuff". Six threats: "**S**ome **S**taff **I**nnocently **P**ost **C**ompany **B**usiness": Social engineering, System and network attacks, Information leakage, Privacy loss, Corporate espionage, Business loss.

!!! trap "Exam traps"
    - A **zone transfer**, a phone call to the help desk and a port scan are all **active**. Reading a cached page, an archive or a Whois record is **passive**.
    - "Reducing the focus area" is an objective. "Information leakage" is a threat. Questions swap the two lists.
    - OSINT means **open-source** intelligence: public sources. It does not mean open-source software.

!!! try "Try it"
    One request can yield system information. In the L01 attacker container:

    ```bash
    curl -s -D - -o /dev/null http://10.77.0.20/
    ```

    The `Server` and `X-Powered-By` lines name the web server software, its version and the language behind it. This touches the target, so it is active, and it is in scope here.

!!! recap "Recap: section 1"
    - Footprinting (reconnaissance) is the first step: collect information and build a blueprint of the target.
    - Passive: no direct interaction. Active: direct interaction that may be noticed.
    - It collects organisation, network and system information.
    - Objectives: learn the security posture, reduce the focus area, identify vulnerabilities, build an information database.
    - Six threats: social engineering, system and network attacks, information leakage, privacy loss, corporate espionage, business loss.

## 2. Footprinting through search engines {M}

A search engine has already visited the target's website, its forgotten test pages and the documents it left lying about. Asking the search engine is passive: the question goes to the search engine, not to the target.

### Advanced search operators {M: Google operators: `site:` one site or domain; `inurl:` / `allinurl:` words in the URL; `intitle:` / `allintitle:` words in the page title; `intext:` words in the body; `inanchor:` / `allinanchor:` words in link text; `filetype:` file extension; `cache:` Google's stored copy; `link:` pages linking to a URL; `related:` similar sites; `info:` details of a page; `before:` / `after:` date. Syntax `operator:term`, no space. The `all...` forms need every word}

**Google hacking**, also called **Google dorking**, means using a search engine's advanced operators to build precise queries that surface sensitive or hidden information. A single query of this kind is a **dork**. The syntax is `operator:search_term`, with no space after the colon.

| Operator | Restricts results to | Example |
| --- | --- | --- |
| `site:` | One site or domain | `site:example.com careers` |
| `inurl:` | Pages with the word in the URL | `inurl:admin site:example.com` |
| `allinurl:` | Pages with **all** the words in the URL | `allinurl:staff login` |
| `intitle:` | Pages with the word in the title | `intitle:"index of" backup` |
| `allintitle:` | Pages with **all** the words in the title | `allintitle:network diagram` |
| `intext:` | Pages with the word in the body text | `intext:"vpn configuration"` |
| `inanchor:` | Pages whose inbound link text has the word | `inanchor:intranet` |
| `allinanchor:` | Pages whose inbound link text has **all** the words | `allinanchor:staff portal login` |
| `filetype:` | Files with that extension | `site:example.com filetype:pdf` |
| `cache:` | Google's stored copy of a page | `cache:example.com` |
| `link:` | Pages that link to the given page | `link:example.com` |
| `related:` | Sites similar to the given one | `related:example.com` |
| `info:` | Information Google holds about a page | `info:example.com` |
| `location:` | News about a place | `location:udaipur flood` |
| `source:` | One publication in Google News | `ransomware source:"The Hindu"` |
| `phonebook:` | Phone listings for a person or business | (retired) |
| `before:` / `after:` | Results dated before or after a day | `breach after:2024-01-01` |

A minus sign excludes a word. The classic query for finding subdomains removes the main site: `site:example.com -inurl:www`. {D}

!!! exam "Exam answer / In practice"
    **Exam answer:** every operator in the table works as described, and there is no space between the operator and its term.

    **In practice:** several of them have been switched off (see the box below), and the courseware's own examples sometimes include a space, or write the `filetype:` example without the word `filetype`. Learn the meanings; do not expect them all to return results today.

!!! update "Updated: September 2024"
    **What changed.** Google has retired its cached pages. The "Cached" link left search results early in 2024, and in **September 2024** Google removed `cache:` from its operator documentation because the operator no longer works. Its current operator page documents only `site:`, `filetype:`, `src:` and `imagesize:`. Earlier retirements: `phonebook:` (**2010**), `link:` (**2017**) and `related:` (**2023**); `info:` has also gone. For an old copy of a page, use the Wayback Machine (section 3). Status checked 18 November 2026.

    **The exam still expects:** `cache:` shows Google's stored copy, `link:` finds pages linking to a site, `related:` finds similar sites and `info:` describes a page.

!!! remember "Remember"
    Read the operator as plain English. **in-url**, **in-title**, **in-text**, **in-anchor** say where to look. Put **all** in front and every word must be there. **site** fences the search into one domain; **filetype** picks the kind of file.

### What Google hacking finds {U}

With the right dork, a search engine will list things the owner never meant to publish: error messages that reveal software and file paths; files containing passwords; sensitive directories; login portals; firewall and intrusion-detection logs; security advisories and software versions; web application source code; control panels of unprotected internet-connected devices; and hidden intranet or VPN pages.

A typical people-and-intranet dork combines three operators: `intitle:intranet inurl:intranet +intext:"human resources"`. {R}

### The Google Hacking Database {M: GHDB (Google Hacking Database): the collection of Google dorks hosted on Exploit-DB. SearchSploit: command-line tool that searches a local, offline copy of Exploit-DB, useful on air-gapped networks}

The **Google Hacking Database (GHDB)** is a public collection of ready-made dorks. It is part of **Exploit-DB**, the exploit archive at exploit-db.com. Its fourteen categories are worth recognising: {R}

| | | |
| --- | --- | --- |
| Footholds | Files containing usernames | Sensitive directories |
| Web server detection | Vulnerable files | Vulnerable servers |
| Error messages | Files containing juicy info | Files containing passwords |
| Sensitive online shopping info | Network or vulnerability data | Pages containing login portals |
| Various online devices | Advisories and vulnerabilities | |

Attackers use the GHDB for reconnaissance, to exploit misconfigurations, to find systems running outdated software, to harvest credentials and to spot exposed services.

**SearchSploit** is a command-line tool that searches a local copy of Exploit-DB. Because the copy is on your own disk, it works on isolated networks with no internet access.

### VPN and FTP dorks {R}

The courseware prints two tables of dorks. You are not expected to recite them; recognise the pattern, which is always an operator from the table above plus a tell-tale string.

| Looking for | The dork contains | Finds |
| --- | --- | --- |
| VPN login portals {R} | `inurl:` with a vendor's login path, or `site:vpn.*.*/ intitle:"login"` | Remote-access login pages (Fortinet, Cisco ASA, Citrix, WatchGuard, Zyxel) |
| OpenVPN material {R} | `intitle:"index of" /etc/openvpn/`, or a search for files ending `.ovpn` | Configuration files, certificates and static keys |
| FTP servers {R} | `intitle:"index of" ftp`, `inurl:ftp` | Open file listings |
| FTP client leftovers {R} | `ws_ftp.ini`, `ws_ftp.log` | Stored FTP usernames, passwords and transfer logs |

### Other kinds of search engine {M: Search engine types: meta search engines (Startpage, MetaGer, eTools.ch) query other engines, hold no index of their own and hide the user's IP; FTP search engines (NAPALM FTP Indexer, FreewareWeb FTP File Search, Mamont, Globalfilesearch.com) find files on FTP servers; IoT search engines (Shodan, Censys, ZoomEye) find internet-connected devices with their IP, location and open ports}

| Kind | What it does | Names to know |
| --- | --- | --- |
| Advanced search, image search | Google's Advanced Search form builds operator queries for you. Advanced Image Search filters by size, colour, type and domain | Google Advanced Search |
| Reverse image search | Starts from a picture and finds where else it appears: the original source of a profile photo, for example | Google Image Search, TinEye, Yahoo, Bing, Pinterest |
| Video search and analysis | Finds video about the target, then reads its upload time, thumbnails and other hidden details | YouTube, Google Videos; YouTube Metadata, YouTube DataViewer, EZGif, VideoReverser.com |
| Meta search engine | Sends your query to several other search engines at once and merges the answers. Has **no index of its own** and hides your IP address | Startpage, MetaGer, eTools.ch |
| FTP search engine | Searches files stored on FTP servers | NAPALM FTP Indexer, FreewareWeb FTP File Search, Mamont, Globalfilesearch.com |
| IoT search engine | Indexes internet-connected **devices**, not pages: cameras, industrial control (SCADA) systems, routers | Shodan, Censys, ZoomEye |

**Shodan** deserves a second look. It scans the whole internet and records what each address answers with, so you can search for devices by city, country, hostname, operating system or IP address. The courseware uses it for VoIP and VPN footprinting and, in section 3, for identifying a target's operating system. {U}

!!! try "Try it"
    The lab has no internet, so look at the two things a search engine would have found. In the L01 attacker container:

    ```bash
    curl -s http://10.77.0.20/robots.txt ; curl -s http://10.77.0.20/backup/
    ```

    `robots.txt` asks search engines to stay out of one folder, which tells every reader the folder exists. The second command shows that folder's open file listing: exactly the page an `intitle:"index of"` dork is built to find. **With internet:** search `site:example.com filetype:pdf` for a domain you own.

!!! recap "Recap: section 2"
    - Google hacking (dorking) uses advanced operators to find sensitive pages. Syntax: `operator:term`.
    - `site:`, `inurl:`, `intitle:`, `intext:`, `inanchor:`, `filetype:`, `cache:`, `link:`, `related:`, `info:`; the `all...` forms need every word.
    - The GHDB is the dork collection on Exploit-DB; SearchSploit searches Exploit-DB offline.
    - Meta search engines have no index of their own. FTP search engines find files. IoT search engines find devices.
    - In practice `cache:`, `link:`, `related:` and `info:` no longer work; the exam still asks about them.

## 3. Footprinting through internet research services {R}

Beyond search engines there is a whole industry of websites that collect and resell public information. Each one answers a different question about the target. Most of this section is name recognition: match the service to the job.

### Domains, subdomains and old pages {M: Subdomain tools: Netcraft, DNSdumpster, Pentest-Tools Find Subdomains, Sublist3r (`sublist3r -d domain -o file`); dork `site:target.com -inurl:www`. Wayback Machine (archive.org) keeps old versions of web pages, including removed ones; Photon retrieves archived URLs (`--wayback`)}

A company's main website is built for the public. Its **subdomains** often are not: test sites, staff portals and forgotten projects sit there, usually less well protected. Finding them is the first technical job in footprinting.

| Tool | What it gives |
| --- | --- |
| Netcraft | Subdomains of a domain; site reports showing hosting and technology |
| DNSdumpster | Hosts related to a domain: subdomains, IP addresses, DNS servers |
| Pentest-Tools Find Subdomains | Subdomains with IP addresses, web server, technology and page titles |
| Sublist3r | Command-line subdomain enumeration: `sublist3r -d example.com -o subdomains.txt` |

The **Wayback Machine** at archive.org stores copies of web pages from the day it first visited them. Information the organisation has since removed (old staff lists, documents, even source code) may still be there. **Photon** is a crawler that can pull a site's archived addresses: `python photon.py -u <URL> -l 3 -t 200 --wayback`. {R}

!!! story "The idea"
    Deleting a page from your website is like taking a poster down from a noticeboard after a photographer has already been round. The board is clean. The photograph is not yours to delete.

### People, jobs and the dark web {M: Surface web = indexed by search engines; deep web = not indexed (behind logins and databases); dark web (darknet) = subset of the deep web reached only with special tools, allows anonymous use. Dark web tools: Tor Browser, ExoneraTor, OnionLand Search}

**People search services** (Spokeo is the featured one; also Intelius, pipl, BeenVerified, Whitepages, Instant Checkmate and PeekYou) return a person's addresses, phone numbers, email addresses, age, relatives, social profiles and court records. They mostly cover the United States. {R}

**Job sites** (Dice, LinkedIn, Glassdoor, Simply Hired) leak technology. An advert for a network administrator that asks for experience with a named firewall, hypervisor and database version is a free inventory of the target's systems. Staff CVs do the same in reverse. {U}

```diagram m02-webs
Three layers. The dark web is a small part of the deep web, not another name for it.
```

| Layer | What it is | Reached with |
| --- | --- | --- |
| Surface web | Pages that search engines have indexed | Any browser |
| Deep web | Pages search engines cannot index: anything behind a login, a form or a database | An ordinary browser and the right credentials |
| Dark web (darknet) | A subset of the deep web that lets people publish and browse anonymously | Special software such as Tor Browser |

On the dark web attackers look for what has already been stolen: card details, identity documents, medical records, account credentials. The courseware names **Tor Browser**, **ExoneraTor** and **OnionLand Search** as dark web tools, and shows searches refined by person, publication, court record, member directory, medical record and location.

!!! exam "Exam answer / In practice"
    **Exam answer:** the dark web is searched with tools such as Tor Browser, ExoneraTor and OnionLand Search, using operators such as `filetype:pdf site:onion confidential`. The courseware also describes Tor Browser as acting like a default VPN.

    **In practice:** Tor Browser is a browser, not a search engine and not a VPN. ExoneraTor, by the Tor Project's own description, only answers whether an IP address was a Tor relay on a given date. Google-style operators are honoured by few dark web search engines. Buying or downloading stolen data is a crime even for a tester; dark web checks are normally done through a contracted monitoring service.

### Competitive intelligence {M: Competitive intelligence = legally gathering and analysing information about competitors; direct approach (trade shows, social engineering of employees and customers) or indirect (online sources). Sites. When did it begin, how did it develop: EDGAR, D&B Hoovers, LexisNexis, Business Wire, Factiva. What are its plans: MarketWatch, The Wall Street Transcript, Euromonitor, Experian, The Search Monitor, USPTO. What do experts say: SEMRush, ABI/INFORM Global, SimilarWeb, SERanking}

**Competitive intelligence gathering** is identifying, collecting, analysing and using information about competitors from public sources. It is legal and non-interfering, which separates it from industrial espionage. An attacker uses the same sources to plan.

There are two approaches. The **direct** approach gathers from trade shows and by social engineering employees and customers. The **indirect** approach uses online resources: company websites and job adverts, press releases and annual reports, patents and trademarks, social media, customer reviews, financial filings and business databases.

| The question | Sites to recognise |
| --- | --- |
| When did the company begin? How did it develop? | **EDGAR** (company filings with the US Securities and Exchange Commission), **D&B Hoovers** (business records), **LexisNexis** (legal and public records), **Business Wire** (press releases), **Factiva** (global news database) |
| What are the company's plans? | **MarketWatch**, **The Wall Street Transcript** (interviews with executives and analysts), **Euromonitor** (market research), **Experian**, **The Search Monitor** (brand and advertising monitoring), **USPTO** (United States patents and trademarks) |
| What do experts say about the company? | **SEMRush** (keyword and advertising research), **ABI/INFORM Global** (business database), **SimilarWeb** (website traffic estimates), **SERanking** (competitor analysis) |

### Other research services {R}

| Service type | What an attacker learns | Names to know |
| --- | --- | --- |
| Operating system lookups | The operating system and software of public servers | Netcraft, Shodan, Censys |
| Maps and geography | Entrances, cameras, fences, nearby Wi-Fi; a basis for dumpster diving and tailgating | Google Earth, Google Maps, Wikimapia |
| Financial services | Share value, company profile, competitors, press releases | Google Finance, MSN Money, Yahoo Finance, Investing.com |
| Business profile sites | Location, contact details, departments, type of business | opencorporates, Crunchbase, corporationwiki |
| Alert services | Automatic notice whenever the target is mentioned | Google Alerts, X Alerts, Giga Alerts |
| Online reputation management (ORM) | What people are saying about the brand, in real time | Mention, ReviewPush, Reputology |
| Groups, forums and blogs | Staff discussing work: network details, names, email addresses | Google Groups, LinkedIn Groups |
| Public source-code repositories | Configuration files, private SSH and TLS keys, source code | GitHub, GitLab, SourceForge, Bitbucket; found with **Recon-ng** |

!!! update "Updated: services that have moved on"
    Each line gives what changed and when. The exam still expects the courseware's version.

    | Service | What changed | When | Exam still expects |
    | --- | --- | --- | --- |
    | Censys | Censys set the retirement of its original search site (Legacy Search) for this date and has switched off free access to it; searches now run on the Censys Platform with a new query language | **September 2026** | "Censys" as an IoT search engine and operating-system lookup |
    | USPTO | The trademark search system TESS was retired and replaced by a new Trademark Search. The patent databases PatFT and AppFT had already given way to Patent Public Search | **November 2023**; patents **September 2022** | "USPTO" as the source for patents and trademarks |
    | Google+ | The courseware's description of BuzzSumo still lists it. The consumer service closed | **April 2019** | Recognise BuzzSumo as a social content search tool |

    Status checked 18 November 2026. These services change often; look at the owner's site before you rely on one.

!!! try "Try it"
    Guess subdomains the way the online tools do. In the L01 attacker container (use `aarogya-demo.lab` in the healthcare skin):

    ```bash
    for w in $(cat /usr/share/wordlists/common-small.txt) mail ns1 www; do a=$(dig +short $w.kestrel-freight.lab @10.77.0.10); [ -n "$a" ] && echo "$w $a"; done
    ```

    Four names answer. Keep the list; section 6 shows a host that guessing cannot find. **With internet:** look up a domain you own on the Wayback Machine.

!!! recap "Recap: section 3"
    - Subdomains: Netcraft, DNSdumpster, Pentest-Tools, Sublist3r, or `site:target.com -inurl:www`.
    - archive.org keeps pages the owner has deleted; Photon retrieves the archived addresses.
    - Surface web is indexed; deep web is not; dark web is the anonymous subset reached with Tor Browser.
    - Competitive intelligence is legal; direct or indirect. Know which sites answer "began", "plans" and "expert opinion".
    - Job adverts, maps, alerts, reputation tools and code repositories all leak.

## 4. Footprinting through social networking sites {R}

This is not the same as social engineering. In **social engineering** the attacker tricks a person into giving information. In **footprinting through social networking sites** the attacker simply collects what people and organisations have posted. The first can use the second as its starting point.

### What is collected {U}

Sites such as Facebook, X (formerly Twitter), LinkedIn and Instagram let anyone search by name, employer, school or location. A profile gives a person's job title, employer, location, education, contacts and photographs. **LinkedIn** is the richest source about an organisation, because staff list their own roles, projects and the technology they work with.

### Harvesting names and email addresses {M: theHarvester: `-d` domain or company, `-l` limit on results, `-b` data source (for example `-b linkedin`, `-b baidu`), `-f` output file. Sherlock: searches many social networks for one username. Email Spider and theHarvester harvest email lists}

| Tool | What it does | Command to recognise |
| --- | --- | --- |
| **theHarvester** | Collects employee names, job titles and email addresses for a domain from public sources | `theHarvester -d example.com -l 200 -b baidu` |
| **Email Spider** {R} | Harvests email addresses for a domain from search engines | |
| **Sherlock** | Checks hundreds of social networks for one username and lists the profile addresses | `sherlock <username>` |
| **Social Searcher** {R} | Searches social networks in real time for a user's posts and profiles | |
| **BuzzSumo** {R} | Finds the most shared content for a topic, author or domain | |
| Google Trends, Hashatit, Ubersuggest {R} | Further tools for analysing a target's social media presence | |

In theHarvester, `-d` names the domain or company, `-l` limits the number of results and `-b` chooses the data source. `-b linkedin` lists employees; a search engine such as `-b baidu` finds email addresses. A harvested email list feeds two later attacks: social engineering and password guessing.

!!! exam "Exam answer / In practice"
    **Exam answer:** `theHarvester -d microsoft -l 200 -b linkedin` enumerates a company's employees on LinkedIn; `-b` names the source and `-l` the limit.

    **In practice:** as checked in November 2026, theHarvester's own source list no longer includes `linkedin`, `google` or `bing`; `baidu` is still there, alongside sources such as `crtsh` and `duckduckgo`. Run `theHarvester -h` and use what your version offers.

!!! trap "Exam traps"
    - Collecting posted information is **footprinting through social networking sites**. Sending a fake friend request to see restricted posts is **social engineering**.
    - **Sherlock** hunts a *username* across sites. **theHarvester** harvests *emails and names* for a *domain*.
    - In theHarvester, `-b` is the data source, not "brute force".

!!! try "Try it"
    Harvest an email list by hand. In the L01 attacker container:

    ```bash
    curl -s http://10.77.0.20/staff | grep -oE '[a-z]+@[a-z.-]+' | sort -u
    ```

    Five addresses, and from them the username pattern: first initial plus surname. That one line is what theHarvester automates across many sources.

!!! recap "Recap: section 4"
    - Social networking footprinting collects what is posted; social engineering tricks people.
    - LinkedIn reveals staff, roles and technology.
    - theHarvester: `-d` domain, `-l` limit, `-b` source, `-f` output file.
    - Sherlock finds one username across many networks; Social Searcher and BuzzSumo analyse social content.
    - An email list gives the username format for later attacks.

## 5. Whois footprinting {M}

Every domain name and every block of IP addresses is registered to someone. **Whois** is the query-and-response protocol for asking who. It listens on **TCP port 43**.

### What a Whois query returns {M: Whois: query and response protocol on TCP port 43. Returns domain name details, registrar, owner contact details, name servers, NetRange, creation, expiry and last-updated dates, domain status. Whois models: thick (complete data from all registrars), thin (only the name of the registrar's Whois server), decentralized (several independent entities hold complete data)}

A Whois record can show: domain name details; the registrar; the owner's contact details; the domain's name servers; the **NetRange** (the block of IP addresses); the dates the domain was created, last updated and will expire; and the domain's status.

An attacker uses this to map the organisation's network, to find its name servers for section 6, and to impersonate the people named in the record.

| Whois data model | What the central database stores |
| --- | --- |
| Thick Whois | The complete Whois information from all registrars |
| Thin Whois | Only the name of the registrar's Whois server, which holds the full details |
| Decentralized Whois | Complete information, managed by several independent entities |

The courseware adds the labels "distributed model" to thick and "centralized model" to thin. Other references do not use those labels consistently, so learn the definitions, not the labels.

### The five regional internet registries {M: Five RIRs: ARIN (North America), RIPE NCC (Europe, Middle East, Central Asia), APNIC (Asia Pacific), LACNIC (Latin America and Caribbean), AFRINIC (Africa). Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16}

| Registry | Full name | Region |
| --- | --- | --- |
| ARIN | American Registry for Internet Numbers | United States, Canada, parts of the Caribbean |
| RIPE NCC | Réseaux IP Européens Network Coordination Centre | Europe, the Middle East, Central Asia |
| APNIC | Asia Pacific Network Information Centre | Asia and the Pacific, including India |
| LACNIC | Latin American and Caribbean Network Information Centre | Latin America and the Caribbean |
| AFRINIC | African Network Information Centre | Africa |

```diagram m02-registries
Two hierarchies. A domain lookup goes down the first; an IP address lookup goes down the second.
```

!!! exam "Exam answer / In practice"
    **Exam answer:** the regional internet registries (RIRs) maintain the Whois databases, which hold the personal information of domain owners.

    **In practice:** RIRs register **numbers**: IP address blocks and autonomous system numbers. Domain **names** are registered through registries and registrars under ICANN's rules. Ask an RIR about an IP address; ask a registry or registrar about a domain. And since 2018 most personal contact details in domain records are redacted for privacy.

!!! update "Updated: January 2025 and August 2025"
    **What changed.** Whois is being replaced. From **28 January 2025** ICANN made the Registration Data Access Protocol (**RDAP**) the definitive source for registration data on generic top-level domains such as `.com` and `.org`, and ended the contractual duty to offer Whois for them. RDAP answers over HTTPS in a structured format. ICANN's Registration Data Policy, in effect from **21 August 2025**, sets which fields are published and which are redacted. Many registries still run Whois voluntarily, and country domains set their own rules. Status checked 18 November 2026.

    **The exam still expects:** Whois, a query and response protocol on TCP port 43, returning the fields listed above.

!!! remember "Remember"
    Five registries, five regions: **A**RIN America, **R**IPE Europe, **AP**NIC Asia Pacific, **LAC**NIC Latin America and the Caribbean, **AF**RINIC Africa. Whois is on port **43**: "**Who is** at door forty-three?"

### Tools and IP geolocation {R}

- **Whois lookup tools:** whois.domaintools.com; SmartWhois at tamos.com; Batch IP Converter (also handles non-English domain names and IPv6); WHOIS Domain Lookup; Active Whois.
- **IP geolocation tools:** IP2Location (featured), IP Location Finder, IP Address Geographical Location Finder. They estimate country, region, city, latitude and longitude, postal code, time zone, connection speed, internet provider and domain name from an IP address.

Geolocation is an estimate drawn from a database. It usually finds the right country and often the wrong street.

!!! try "Try it"
    The lab has no Whois server. Its DNS holds the nearest thing, the zone's start-of-authority record:

    ```bash
    dig +noall +answer kestrel-freight.lab SOA @10.77.0.10
    ```

    It names the primary name server, the responsible mailbox (`hostmaster.` stands for `hostmaster@`) and a serial number that reads as a date. **With internet:** run `whois example.com`, or use ICANN's lookup page at lookup.icann.org, on a domain you own.

!!! recap "Recap: section 5"
    - Whois: who registered a domain or address block. TCP port 43.
    - It returns registrar, owner contacts, name servers, NetRange, dates and status.
    - Thick stores everything; thin stores a pointer to the registrar; decentralized spreads it across entities.
    - Five RIRs: ARIN, RIPE NCC, APNIC, LACNIC, AFRINIC.
    - In practice RDAP has replaced Whois for generic domains and most personal details are redacted.

## 6. DNS footprinting {M}

The **Domain Name System (DNS)** maps names to addresses. An organisation's DNS data is called its **zone**. The zone is a list of the hosts the organisation considers important enough to name, so reading it is the fastest way to find key systems.

### Record types {M}

| Record {M} | What it holds |
| --- | --- |
| A | The IPv4 address of a host |
| AAAA | The IPv6 address of a host |
| MX | The domain's mail server |
| NS | The domain's name server |
| CNAME | An alias: another name for a host |
| SOA | Start of authority: which server is authoritative for the domain |
| SRV | Service records: where a named service runs |
| PTR | Maps an IP address back to a hostname (reverse lookup) |
| RP | The responsible person |
| HINFO | Host information: CPU type and operating system |
| TXT | Unstructured text |

!!! remember "Remember"
    **A** for **A**ddress, four **A**s for the longer IPv6 one. **M**ail e**X**changer. **N**ame **S**erver. **C**anonical **NAME** is an alias. **P**oin**T**e**R** points backwards, from number to name.

### Zone transfers and interrogation tools {M: Zone transfer (AXFR): copies an entire DNS zone in one request; if allowed to anyone it hands over every host name. DNS tools: SecurityTrails, Fierce, DNSChecker, zdns, DNSdumpster. `dnsrecon -d domain -t std` standard enumeration; `dnsrecon -r first-last` reverse lookup of a range. Reverse DNS finds the PTR record for an IP address}

A **zone transfer** is how a backup name server copies the whole zone from the primary. If the primary answers that request from anyone, an attacker gets every record in one reply, including hosts that are never linked from anywhere.

```diagram m02-axfr
Left: ordinary lookups reveal only the names you already know to ask for. Right: an open zone transfer reveals everything.
```

| Tool | What it does |
| --- | --- |
| **SecurityTrails** | Builds a DNS map of a domain: current and historical A, AAAA, NS, MX, SOA and TXT records, and subdomains |
| **Fierce** | DNS reconnaissance: finds subdomains and nearby, non-contiguous IP space |
| **DNSRecon** | Command-line DNS enumeration, zone transfers and reverse lookups |
| DNSChecker, zdns, DNSdumpster {R} | Further DNS interrogation tools |

Fierce commands to recognise: {R}

| Command | Effect |
| --- | --- |
| `fierce --domain example.com` | Basic scan |
| `fierce --domain example.com --subdomains admin mail` | Test only the named subdomains |
| `fierce --domain example.com --subdomains mail --traverse 10` | Also check 10 addresses either side of each record found |
| `fierce --domain example.com --subdomains mail --connect` | Try an HTTP connection to each host found |
| `fierce --domain example.com --wide` | Scan the whole range of every record found |

### Reverse DNS lookup {U}

An ordinary lookup turns a name into an address. A **reverse DNS lookup** turns an address into a name by finding its **PTR** record. Run across a whole range, it reveals hosts that share a block with a known server.

```bash
dnsrecon -d example.com -t std            # standard enumeration of a domain
dnsrecon -r 192.0.2.0-192.0.2.255         # reverse lookup of every address in a range
```

Other reverse lookup tools to recognise: Reverse Lookup (MxToolbox), puredns, Reverse IP Domain Check and Reverse IP Lookup. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** the courseware's AI example asks for all subdomains "using dig" and answers with a command that queries the domain's **NS** records, saying the name servers listed "often include the subdomains as well".

    **In practice:** NS records list name servers and nothing else. `dig` finds subdomains only if you guess them one by one, or if a zone transfer (`dig axfr`) is permitted. Recognise the command for the exam; do not rely on the claim.

!!! update "Updated: January 2019"
    **What changed.** The courseware's AI-generated script runs `dig <domain> ANY` to fetch every record type at once. **RFC 8482**, published **January 2019**, allows a DNS server to refuse that: it may answer an `ANY` query with a small subset of records, or with a single made-up HINFO record whose CPU field reads "RFC8482". Many large providers do exactly this, so `ANY` now returns almost nothing from them.

    **The exam still expects:** `ANY` as the query that requests all record types. In real work, ask for each type by name.

!!! cpent "CPENT depth: how professionals map a domain"
    - **Check ownership first.** A name that points at a cloud provider or a shared host belongs partly to someone else. Confirm with the client which names and ranges they may authorise.
    - **Certificate transparency.** Every publicly trusted TLS certificate is logged. Searching those logs (crt.sh is the usual front end) lists hostnames without sending one packet to the target.
    - **Layer the sources.** Passive tools first (subfinder, amass in passive mode), then resolve what they found, then brute-force names, then try `dig axfr` against each name server. Record which source produced each name.
    - **From names to networks.** Group the resolved addresses by the registry's NetRange and by autonomous system to see which blocks really belong to the client.

!!! try "Try it"
    Ask the lab's name server for everything. In the L01 attacker container:

    ```bash
    dig axfr kestrel-freight.lab @10.77.0.10
    ```

    Compare the answer with your list from section 3. One host is new: guessing could not find it and an ordinary lookup of its name returns NXDOMAIN. Read the TXT records too. The lab has no reverse zone, so `dig -x 10.77.0.20 @10.77.0.10` is refused.

!!! recap "Recap: section 6"
    - A and AAAA addresses; MX mail; NS name server; CNAME alias; SOA authority; SRV service; PTR reverse; RP person; HINFO host; TXT text.
    - A zone transfer (AXFR) copies the whole zone. Open to anyone, it is a full host list.
    - Tools: SecurityTrails, Fierce, DNSRecon, DNSChecker, zdns, DNSdumpster.
    - `dnsrecon -d domain -t std`; `dnsrecon -r range` for reverse lookups, which use PTR records.
    - In practice `ANY` queries are often refused, and NS records do not list subdomains.

## 7. Network and email footprinting {U}

### Finding the network range {U}

Once Whois has given a server's IP address, the regional registry's database gives the whole block it belongs to. For an address in North America that means the ARIN Whois search. The range shows how big the network is and where to look for live machines in Module 3.

Three ranges are reserved for **private** networks and never appear on the public internet: `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`. Seeing one in a leaked document or an email header tells you about the inside of a network.

### Traceroute {M: Traceroute: sends probes with rising TTL; each router subtracts 1 and at 0 discards the packet and returns ICMP time exceeded, revealing itself. Windows `tracert` uses ICMP; Linux `traceroute` uses UDP; `tcptraceroute` uses TCP when ICMP is blocked. Tools: NetScanTools Pro, PingPlotter, Traceroute NG}

**Traceroute** lists the routers between you and a target. It works by abusing a safety feature. Every IP packet carries a **time to live (TTL)** number. Each router subtracts one. A router that brings it to zero throws the packet away and sends back an ICMP "time exceeded" message, which reveals that router's address.

```diagram m02-traceroute
Traceroute sends probes with TTL 1, 2, 3 and so on. Each one dies one router further along.
```

| Variant | Command | Probe |
| --- | --- | --- |
| ICMP traceroute | `tracert 192.0.2.10` (Windows default) | ICMP echo requests |
| UDP traceroute | `traceroute www.example.com` (Linux default) | UDP datagrams |
| TCP traceroute | `sudo tcptraceroute www.example.com` | TCP packets; gets through where ICMP is blocked |

**Traceroute analysis** means running traces to several hosts in the target's range and comparing the last few hops. A hop that appears just before many different targets is probably their gateway router or firewall. That is how an outsider sketches a network's layout. {U}

Traceroute tools to recognise: **NetScanTools Pro** (ICMP, UDP or TCP traces, with the country of each hop), **PingPlotter** (graphs latency and packet loss over time), Traceroute NG and the built-in `tracert`. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** traceroute uses ICMP and the TTL field; Windows `tracert` uses ICMP and Linux `traceroute` uses UDP. One line of the courseware places the TTL "in the ICMP header", and says the destination finally answers with a normal ping reply.

    **In practice:** TTL is a field of the **IP header**. The final answer depends on the probe: an ICMP echo reply for `tracert`, an ICMP "port unreachable" for a UDP trace, a TCP reply for `tcptraceroute`. Lines of `* * *` mean a router chose not to answer, not that the path is broken.

### Tracking email {M: Email header shows: sender's mail server, sender's IP address, date and time sent and received, authentication system used by the sender's server, a unique message ID, sender's full name. Email tracking tools: eMailTrackerPro, IP2LOCATION Email Header Tracer, MxToolbox, Holehe, DNS Checker Email Header Analyzer, Social Catfish}

**Email tracking** monitors what happens to a message after it is sent. Tracking tools can report the recipient's IP address and rough location, when the message was received and read, how long it was open, whether links were clicked, whether it was forwarded, and the device, operating system and browser used.

An **email header** is the routing record at the top of every message, normally hidden. It contains:

- the sender's mail server and the authentication system it used;
- the sender's IP address and the address the message was sent from;
- the date and time the message was sent, and when each server received it;
- a unique message ID;
- the sender's full name.

```diagram m02-mail
An email's journey. Every server stamps the header, newest stamp on top.
```

Tools to recognise: **eMailTrackerPro** (analyses headers and maps the sender's location), **IP2LOCATION's Email Header Tracer**, MxToolbox, Holehe, DNS Checker Email Header Analyzer and Social Catfish. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** email tracking reveals the recipient's IP address, location, device and reading time.

    **In practice:** tracking depends on the mail program loading a hidden image. Large mail services now fetch images through their own servers, so the tracker sees the provider's address, not the reader's. Header analysis is still reliable for the path a message took.

!!! try "Try it"
    The lab is one network segment, so a traceroute there has nothing to show. Read the mail server's greeting instead; it names the host and its software:

    ```bash
    printf 'QUIT\r\n' | nc -w 3 10.77.0.40 25
    ```

    **With internet:** run `traceroute example.com` (macOS, Linux) or `tracert example.com` (Windows) from your own computer and count the hops. Then open any email you have received, choose "show original" or "view source", and find the bottom `Received:` line.

!!! recap "Recap: section 7"
    - The regional registry gives the network range for a known IP address.
    - Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.
    - Traceroute raises the TTL one hop at a time; routers reply "time exceeded".
    - Windows `tracert` is ICMP; Linux `traceroute` is UDP; `tcptraceroute` is TCP.
    - An email header shows the sender's server, IP address, times, authentication and message ID.

## 8. Footprinting through social engineering {U}

**Social engineering** is getting information from people by deceiving them. It is non-technical: the target does not realise anything was taken. The attacker first wins the confidence of someone authorised, then leads them to reveal what should have stayed private. Module 9 covers it in full; this section covers its use for footprinting.

What it yields: card details, usernames and passwords, the security products in use, operating system and software versions, IP addresses, server names and the layout of the network.

### The four techniques {M: Social engineering for footprinting: eavesdropping (intercepting audio, video or written communication without consent); shoulder surfing (secretly watching someone enter passwords or PINs); dumpster diving, also called trashing (searching bins for bills, printouts, notes); impersonation (pretending to be a legitimate or authorised person)}

| Technique | What the attacker does |
| --- | --- |
| Eavesdropping | Intercepts communication of any kind (audio, video or written) without the consent of the people communicating |
| Shoulder surfing | Secretly watches a person type a password, PIN or account number, usually from behind in a crowded place |
| Dumpster diving (trashing) | Searches rubbish bins, printer waste and desk notes for bills, contact lists, printouts and other discarded information |
| Impersonation | Pretends to be someone legitimate (a courier, cleaner, technician, client or visitor), in person or by phone |

The courseware also names tailgating, piggybacking, third-party authorisation and reverse social engineering; Module 9 defines them. {R}

### What social networks give away {R}

| What users do | What the attacker gets |
| --- | --- |
| Maintain a profile | Contact information, location |
| Connect to friends, chat | Friends list and information about friends |
| Share photos and videos | Identity of family members, interests |
| Play games, join groups | Interests |
| Create events | Activities |

| What organisations do | What the attacker gets |
| --- | --- |
| Run user surveys | Business strategies |
| Promote products | Product profile |
| Give user support | An opening for social engineering |
| Recruit | Platform and technology information |
| Check the background of new hires | Type of business |

!!! try "Try it"
    No command for this one. From the lab's staff page and the web server's response headers, write a three-line phone script a caller could use to sound like a supplier's engineer. Then write the one question the help desk should ask to stop it. Do this on paper only; calling real people is out of scope everywhere without written permission.

!!! recap "Recap: section 8"
    - Social engineering deceives people into revealing information; the victim does not notice.
    - Eavesdropping intercepts communication; shoulder surfing watches; dumpster diving searches rubbish; impersonation pretends.
    - Profiles reveal contacts and location; photos reveal family and interests; events reveal activities.
    - Recruitment posts reveal platforms and technology; surveys reveal business strategy.
    - Collecting posts is section 4; tricking people is this section.

## 9. Footprinting tools and AI {R}

The earlier sections each used one tool for one job. The tools here chain many jobs together.

### Frameworks {M: Footprinting tools: Maltego (maps relationships between people, organizations, domains, infrastructure); Recon-ng (modular web reconnaissance framework, e.g. module `recon/domains-hosts/brute_hosts`); FOCA (finds metadata and hidden information in documents); OSINT Framework (web directory of OSINT tools; markers (T) install locally, (D) Google dork, (R) registration required, (M) edit the URL manually); subfinder (passive subdomain discovery)}

| Tool | What it is |
| --- | --- |
| **Maltego** | Draws the relationships between people, groups, organisations, websites, domains, IP addresses and documents as a graph. Start from one entity, such as a website, and expand to its email addresses and phone numbers |
| **Recon-ng** | A web reconnaissance framework built from independent modules with their own database. The module `recon/domains-hosts/brute_hosts` lists hosts for a domain |
| **FOCA** | "Fingerprinting Organizations with Collected Archives". Downloads a domain's public documents (Office, OpenOffice, PDF) and extracts their **metadata**: usernames, software versions, internal server names |
| **subfinder** | Finds valid subdomains from passive online sources; output as JSON, file or screen |
| **OSINT Framework** | A website that arranges free OSINT tools as a tree by category. Each entry may carry a marker |
| **Recon-Dog** | All-in-one tool using public interfaces: Whois, name server lookup, port scan, CMS detection, honeypot detection, subdomains, reverse IP lookup |
| **BillCipher** | Information gathering for a website or IP address: DNS and Whois lookups, port scan, zone transfer, host finder, reverse IP lookup |

OSINT Framework's four markers: **(T)** a tool you must install and run locally; **(D)** a Google dork; **(R)** registration required; **(M)** a link whose address you must edit by hand.

FOCA's features: web search, DNS search, IP resolution, PTR scanning, Bing IP and common names (a dictionary attack against DNS). {R}

Others to recognise by name: Sudomy, whatweb, Raccoon, Orb, Web Check and OSINT.SH. {R}

!!! exam "Exam answer / In practice"
    **Exam answer:** match each tool to its description above.

    **In practice:** several are showing their age. As checked in November 2026, FOCA runs only on Windows and needs a SQL Server database; Sublist3r's own page still recommends Python 2.7 and 3.4; Recon-Dog and BillCipher date from the Python 2 era. Working testers lean on maintained tools such as subfinder, amass and Recon-ng. The exam asks about all of them.

!!! update "Updated: October 2024"
    **What changed.** The free edition of Maltego is now called Maltego Graph Community Edition and sits in the free "Basic" plan. In **October 2024** (version 4.8.1) Maltego introduced a credit system for it: a monthly allowance of 200 credits to spend on the included data sources, with a Maltego ID account required. Status checked 18 November 2026.

    **The exam still expects:** "Maltego" as the tool that maps relationships and real-world links between entities.

### AI-powered OSINT {M: AI in OSINT: use cases are web scraping, pattern recognition, content summarization, sentiment analysis, image recognition, AI detection; benefits are improved efficiency, greater scope, enhanced visibility, increased investigator safety. Tools: Taranis AI (news and situational analysis), OSS Insight (analyses GitHub events)}

**Six use cases:** web scraping; pattern recognition (finding entities and the links between them); content summarisation; sentiment analysis; image recognition (face recognition, metadata analysis, reverse image search and deepfake detection); and AI detection (spotting content another AI produced).

**Four benefits:** improved efficiency, greater scope, enhanced visibility and increased investigator safety.

| Tool | What the courseware says it does |
| --- | --- |
| **Taranis AI** {R} | Collects unstructured news articles from many sources, improves them with language processing, and helps analysts turn them into structured reports |
| **OSS Insight** {R} | Analyses billions of GitHub events; answers plain-language questions about repositories, developers and trends |
| DorkGPT, DorkGenius {R} | Generate Google dorks from a description |
| Google Word Sniper {R} | Refines search queries with targeted keywords |
| Cylect.io {R} | Combines many OSINT databases in one interface |
| ChatPDF {R} | Answers questions about an uploaded PDF |
| Bardeen.ai {R} | Automates collecting data from websites |
| DarkGPT {R} | Queries leaked databases through a language model |
| PenLink Cobwebs {R} | Collects and analyses data from many online sources for investigations |
| Explore AI {R} | Searches inside YouTube videos |
| AnyPicker {R} | Visual web scraper that needs no code |

### Prompt to command {D}

In the AI-assisted steps you describe the task and the assistant returns a command. The exam may show the prompt and ask which command fits.

| You ask for | A correct command looks like |
| --- | --- |
| PDF files on a site, found with a search operator, saved to a file {D} | `lynx --dump "https://www.google.com/search?q=site:example.com+filetype:pdf" > recon1.txt` |
| VPN login pages, using `inurl` {D} | A `lynx --dump` of a Google search for `inurl:"remote login"` plus the vendor name, piped through `grep` to keep the links |
| Subdomains with Sublist3r, saved to a file {D} | `sublist3r -d example.com -o subdomains.txt` |
| 200 email accounts from one source, saved {D} | `theHarvester -d example.com -l 200 -b baidu -f emails.xml` |
| Accounts for a username, saved {D} | `sherlock <username> --output recon2.txt` |
| Install and run DNS enumeration {D} | `sudo apt-get update && sudo apt-get install -y dnsrecon && dnsrecon -d example.com -t std` |
| The routers on the path to a host {D} | `traceroute www.example.com` |

The courseware finishes with a short AI-written Python script. It wraps three shell commands (`dig <domain> ANY +noall +answer`, `whois <domain>` and `theHarvester -d <domain> -b all -l 100`) in functions and prints each result in turn.

!!! exam "Exam answer / In practice"
    **Exam answer:** the commands above are what the courseware shows for each prompt.

    **In practice:** generated commands need checking. In the courseware's own examples the script is written to disk with a malformed `cat <<<` line, the Sherlock option is printed as `- - output`, and search engines block scripted queries from `lynx`. Read every switch against the tool's help before you run it. A model drafting a command is not permission to run it.

!!! coasp "COASP link: footprinting AI systems"
    Everything in this chapter applies when the target is an AI system, with new things to look for.

    - **Exposed model servers.** IoT search engines index model-serving software on its default ports, often with no login (Module 3's COASP box lists the ports).
    - **Leaked keys.** API keys for AI services are among the secrets most often committed to public code repositories. The dorks in section 2 and the repository searches in section 3 find them.
    - **Published models and data.** A team's public model pages and datasets reveal what its system was trained on and how it is prompted.
    - **Job adverts.** "Experience with a named vector database and model gateway" is section 3's technology leak again.

    MITRE ATLAS, the AI counterpart of ATT&CK, begins with a Reconnaissance tactic for this reason. And OSINT is itself becoming AI-assisted, so your own posts are now read by models as well as people.

!!! try "Try it"
    A footprinting script in one line. In the L01 attacker container:

    ```bash
    D=kestrel-freight.lab; for t in SOA NS TXT; do dig +noall +answer $D $t @10.77.0.10; done; curl -s http://10.77.0.20/staff | grep -oE '[a-z]+@[a-z.-]+' | sort -u
    ```

    It asks for three record types by name, not `ANY`, then harvests the email addresses. Ask an AI assistant to write the same thing and compare its answer with this one.

!!! recap "Recap: section 9"
    - Maltego maps relationships; Recon-ng is a modular framework; FOCA extracts document metadata.
    - OSINT Framework markers: (T) install, (D) dork, (R) register, (M) edit the URL.
    - AI helps OSINT with scraping, pattern recognition, summarising, sentiment, images and AI detection.
    - Taranis AI works on news; OSS Insight works on GitHub data.
    - Know the commands for Sublist3r, theHarvester, Sherlock, DNSRecon and traceroute, and check generated ones.

## 10. Footprinting countermeasures {M}

Footprinting cannot be blocked with a firewall, because most of it never reaches you. The defence is to publish less, and to find your own leaks first.

### The list, grouped {M: Footprinting countermeasures: restrict zone transfers to authorized servers; use split DNS (separate internal and external); opt for Whois privacy services; disable directory listings; configure web servers to avoid information leakage; limit what is published on websites, press releases and job adverts; security awareness training against social engineering; stop search engines caching pages; ask archive.org to delete site history; disable geo-tagging; delete accounts of former employees; encrypt and password-protect sensitive information; use footprinting on yourself to find and remove leaks}

| Area | Countermeasures |
| --- | --- |
| DNS and Whois | Restrict zone transfers to authorised servers. Keep internal and external DNS apart (**split DNS**). Use privacy services on Whois records and keep the domain profile private. Sanitise the details given to registrars |
| Web servers | Disable directory listings. Configure servers (including IIS) so banners do not leak software details. Stop search engines caching pages. Avoid cross-linking critical assets at domain level. Ask archive.org to delete the site's history. Use CAPTCHAs and rate limiting against automated collection |
| What you publish | Limit information on the website, in press releases, annual reports, product catalogues and job adverts. Keep business plans and proprietary documents offline. Encrypt and password-protect sensitive information |
| People | Train staff regularly to recognise social engineering. Enforce policies on what may be shared with outsiders. Have staff use pseudonyms on blogs, groups and forums. Restrict access to social networks from the work network. Do not post locations or travel plans |
| Devices and locations | Disable geo-tagging on cameras; turn off location access on phones when it is not needed. Keep strategic information off noticeboards and walls |
| Accounts and network | Disable or delete the accounts of people who have left. Use multi-factor authentication. Switch off protocols that are not required. Use TCP/IP and IPsec filters. Hide server addresses behind a VPN or proxy. Have mail servers ignore mail from anonymous senders. Deploy honeypots to detect and divert footprinting |
| Test yourself | Run footprinting techniques against your own organisation and remove whatever sensitive information you find |

!!! exam "Exam answer / In practice"
    **Exam answer:** "prevent search engines from caching a web page" and "request archive.org to delete the history of the website" are listed countermeasures.

    **In practice:** Google no longer offers cached pages (section 2), so the caching control matters mainly for other search engines and archives. Removing something from an archive does not remove the copies people already made. Treat anything that was once public as public.

!!! hospital "Worked example: what a stranger can learn about a hospital"
    A 300-bed hospital asks what an outsider could find without logging in to anything. One afternoon of footprinting returns this.

    1. **Staff and structure.** The departments page lists the laboratory in-charge, the radiology technologist and the IT officer, with email addresses. The username pattern is obvious.
    2. **Technology.** A job advert asks for experience with a named laboratory information system and imaging archive. A tender notice on a public procurement portal names the model of the new CT scanner.
    3. **Hosts.** DNS names such as `pacs-archive` and `lis-legacy` say what each server does. An open zone transfer lists every one.
    4. **Old pages.** An archived copy of the website still holds a staff phone directory that was removed two years ago.
    5. **Devices.** An IoT search engine shows the hospital's address range answering on a medical imaging port.

    Put together, that is enough for a convincing phone call to the laboratory "from the vendor's support desk". The fixes are section 10: role mailboxes, vaguer adverts, neutral host names, closed zone transfers, imaging systems off the internet.

    Swap "hospital" for "freight company" and "CT scanner" for "warehouse scanners": the lab's generic skin is the same story.

!!! try "Try it"
    Be the defender. List what the lab web server would need to stop announcing:

    ```bash
    curl -s -D - -o /dev/null http://10.77.0.20/ | grep -i -E 'server|powered'
    ```

    Then name, from the table above, the fix for each of your findings in sections 2, 3, 4 and 6.

!!! recap "Recap: section 10"
    - DNS: restrict zone transfers, use split DNS. Whois: privacy services.
    - Web: disable directory listings, hide banners, control caching and archives.
    - Publishing: say less in adverts, press releases and reports; keep sensitive documents offline and encrypted.
    - People: awareness training, clear policy, no travel plans online, delete leavers' accounts.
    - Footprint yourself and remove what you find.

## 11. Lab walk-through {D}

Run this in course lab L01. The generic skin (Kestrel Freight, `kestrel-freight.lab`) and the healthcare skin (Aarogya Demo Hospital, `aarogya-demo.lab`) behave identically; swap the domain. Work from the attacker container. Allow about 60 minutes including notes.

```bash
# 1. Start the lab and open the attacker shell
cd labs/L01-recon-enumeration
docker compose up -d --build
docker compose exec attacker bash

# 2. Organisation information: who works here, and what is the username pattern?
curl -s http://10.77.0.20/staff | grep -oE '[a-z]+@[a-z.-]+' | sort -u

# 3. What did the developer leave in the page source?
curl -s http://10.77.0.20/ | grep -o '<!--.*-->'

# 4. What is the site asking search engines not to index?
curl -s http://10.77.0.20/robots.txt

# 5. System information: server software and language
curl -s -D - -o /dev/null http://10.77.0.20/

# 6. Network information: the zone's authority record, then the whole zone
dig +noall +answer kestrel-freight.lab SOA @10.77.0.10
dig axfr kestrel-freight.lab @10.77.0.10

# 7. Hidden paths, the way a crawler would find them
gobuster dir -q -u http://10.77.0.20 -w /usr/share/wordlists/common-small.txt
```

Answer these in your log as you go:

1. Which of steps 2 to 7 are passive and which are active? (Careful: you are talking to the target every time.)
2. Fill in the three-row table from section 1, organisation, network and system information, with what you found.
3. Which host appears in step 6 that normal lookups deny? What does its name tell you?
4. For each leak, write the countermeasure from section 10.

That log is your footprint report. Module 3 starts from it.

## Quiz

Twelve questions. The options are shuffled every time you load the page.

```quiz
Q: Which of these is passive footprinting?
- Requesting a DNS zone transfer from the target's name server
- Phoning the help desk while posing as a supplier
- * Reading an archived copy of the target's website on archive.org
- Port scanning the target's web server
WHY: Passive footprinting involves no direct interaction with the target. The other three all contact the target's systems or people.
TAG: M

Q: Which operator restricts results to pages that have ALL the given words in the page title?
- `intitle:`
- `allinurl:`
- * `allintitle:`
- `inanchor:`
WHY: The all- prefix requires every word; intitle: needs only the one word that follows it, and allinurl: looks in the URL.
TAG: M

Q: What is the Google Hacking Database?
- A list of Google employees' leaked passwords
- * A collection of search queries (dorks) that find sensitive information, hosted on Exploit-DB
- Google's own vulnerability scanner
- A database of websites Google has removed
WHY: The GHDB is the dork collection that forms part of Exploit-DB. SearchSploit searches Exploit-DB offline.
TAG: M

Q: Startpage, MetaGer and eTools.ch are examples of what?
- IoT search engines
- FTP search engines
- * Meta search engines
- People search services
WHY: Meta search engines send a query to other engines and merge the results; they keep no index of their own. Shodan and Censys are IoT search engines.
TAG: M

Q: Which layer of the web is, by definition, not indexed by ordinary search engines and reachable only with special tools that allow anonymous use?
- Surface web
- Deep web
- * Dark web
- Meta web
WHY: The deep web is everything unindexed; the dark web is the subset that needs tools such as Tor Browser.
TAG: M

Q: Which site would you use to read a US company's official financial filings?
- SimilarWeb
- * EDGAR
- SEMRush
- Wikimapia
WHY: EDGAR is the SEC's filing system. SimilarWeb estimates traffic, SEMRush researches keywords, Wikimapia is a map.
TAG: M

Q: In `theHarvester -d example.com -l 200 -b baidu`, what does `-b` set?
- The number of results
- A brute-force mode
- * The data source to search
- The output file
WHY: -d is the domain, -l the result limit, -b the data source and -f the output file.
TAG: M

Q: On which port does the Whois protocol listen?
- TCP 53
- UDP 161
- * TCP 43
- TCP 443
WHY: Whois is a query and response protocol on TCP port 43. Port 53 is DNS.
TAG: M

Q: Which DNS record maps an IP address back to a hostname?
- CNAME
- * PTR
- MX
- SOA
WHY: PTR records serve reverse lookups. CNAME is an alias, MX the mail server, SOA the authority record.
TAG: M

Q: A Linux user runs `traceroute www.example.com` with no options. Which protocol carries the probes?
- ICMP
- * UDP
- TCP
- ARP
WHY: Linux traceroute sends UDP by default; Windows tracert sends ICMP. tcptraceroute is the TCP variant.
TAG: M

Q: An attacker dressed as a courier walks through an office reading notes left on desks. Which technique is this?
- Eavesdropping
- Dumpster diving
- * Impersonation
- Shoulder surfing
WHY: Pretending to be a legitimate person is impersonation. Dumpster diving searches rubbish; shoulder surfing watches someone type.
TAG: M

Q: A hospital's name server gives its whole zone to anyone who asks. Which countermeasure fixes this directly?
- Whois privacy services
- Disabling directory listings
- * Restricting zone transfers to authorised servers
- Disabling geo-tagging
WHY: Only the organisation's own secondary name servers should be allowed to transfer the zone. Split DNS further limits what the public zone contains.
TAG: U
```

## Exam cheat sheet

Only the MEMORISE items from this chapter, collected automatically. If a fact is not here, you need to understand or recognise it, not recite it.

[[cheatsheet]]

## Coverage check against the official Module 2

Each sub-topic of the official module and where this chapter covers it. The section-by-section verification report is kept with the handbook source as `verification/ceh/m02-footprinting-and-reconnaissance.md`. No official text is reproduced.

| Official sub-topic | Covered in | Status |
| --- | --- | --- |
| Reconnaissance; passive and active footprinting | 1 | OK, exam/practice note on scanning and on the passive attack class |
| Information obtained; objectives; footprinting threats; methodology | 1 | OK |
| Advanced Google hacking techniques and operators | 2 | OK, exam/practice note and update on retired operators |
| What a hacker can do with Google hacking; Google hacking with AI | 2, 9 | OK |
| Google Hacking Database; SearchSploit | 2 | OK |
| VPN footprinting through the GHDB, with AI, and through Shodan | 2, 9 | OK, dork tables reduced to patterns |
| Advanced search, image search, reverse image search | 2 | OK |
| Video, meta, FTP and IoT search engines | 2 | OK, FTP dork table reduced to patterns |
| Top-level domains and subdomains; tools; with AI | 3, 9 | OK, exam/practice note on the dig example |
| Extracting website information from archive.org; Photon | 3 | OK |
| People search services; job sites | 3 | OK |
| Dark web footprinting; advanced dark web search parameters | 3 | OK, exam/practice note; query table reduced to one example |
| Determining the operating system (Netcraft, Shodan, Censys) | 3 | OK, update on Censys |
| Competitive intelligence: sources and the three groups of sites | 3 | OK, update on USPTO |
| Geographical location; financial services; business profile sites; alerts; online reputation; groups, forums and blogs; public source-code repositories | 3 | OK |
| People search on social networking sites; LinkedIn; harvesting email lists, and with AI | 4, 9 | OK, exam/practice note on theHarvester sources |
| Analysing social media presence; tools; with AI | 4, 9 | OK |
| Whois lookup, data models, RIRs, lookup tools; IP geolocation | 5 | OK, exam/practice note and update on RDAP |
| DNS records; DNS interrogation tools; Fierce; DNS lookup with AI; reverse DNS lookup | 6, 9 | OK, update on ANY queries |
| Locating the network range; traceroute (ICMP, TCP, UDP), with AI; traceroute analysis and tools | 7, 9 | OK, exam/practice note on TTL |
| Tracking email communications; email headers; email tracking tools | 7 | OK, exam/practice note |
| Footprinting through social engineering; information available on social networking sites | 8 | OK |
| Footprinting tools: Maltego, Recon-ng, FOCA, subfinder, OSINT Framework, Recon-Dog, BillCipher, others | 9 | OK, update on Maltego |
| AI-powered OSINT tools; custom Python script with AI | 9 | OK, exam/practice note |
| Footprinting countermeasures | 10 | OK, grouped |
| Module summary | Recaps and cheat sheet | OK |

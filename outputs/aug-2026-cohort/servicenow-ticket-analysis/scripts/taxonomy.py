"""
Canonical 3-tier IT service desk taxonomy for the ServiceNow ticket analysis workflow.

This file is the single source of truth. The data generator uses it to create tickets,
the categorizer uses it as the fixed list of allowed buckets, and the analyzer uses it
to roll numbers up from L3 to L1.

Structure: L1 Category > L2 Subcategory > L3 Issue Type > [raw description phrasings]

The phrasings are deliberately written the way real users type into a portal:
lowercase, typos, no punctuation, no mention of the category name. That is the whole
point of the exercise. A description that says "password reset needed" is trivial.
A description that says "cant get in since morning" is the real job.
"""

TAXONOMY = {
    "Access & Identity": {
        "_group": "IAM Support",
        "Password": {
            "Password reset": [
                "cant get into the system since morning, tried twice already",
                "locked out again. need it opened asap, have a client call at 11",
                "my login is not working. it says invalid credentials but im sure its right",
                "forgot the credentials after the holiday, please help",
                "system not accepting my details after i changed it last week",
            ],
            "Account locked after failed attempts": [
                "account got blocked, i think i typed wrong 3 times",
                "it says too many attempts, locked. pls unlock",
                "blocked out of the portal, keeps saying account disabled",
                "i am unable to sign in, message says account is locked contact admin",
            ],
            "Password expiry not notified": [
                "no warning came and today it just stopped letting me in",
                "expired without any mail to me, now i cant work",
                "did not get the 14 day reminder, credentials expired suddenly",
            ],
        },
        "Account Provisioning": {
            "New joiner account setup": [
                "new person joining monday in my team, nothing is set up for her yet",
                "need everything ready for the new resource starting next week",
                "our new hire has no login, laptop is there but cannot start",
            ],
            "Leaver account deactivation": [
                "person left last friday, please close everything for him",
                "resignation done, need the access removed before audit",
                "his last working day was 28th, still showing active in the system",
            ],
            "Role change access update": [
                "moved from support to delivery team, my old screens are gone",
                "promoted last month but still seeing the old menu options",
                "transferred to another department, need the right screens now",
            ],
        },
        "MFA": {
            "MFA device lost or replaced": [
                "changed my phone, now the 6 digit code app is empty",
                "lost my handset yesterday, cannot get the verification code",
                "new device, the authenticator is not showing anything for work",
            ],
            "MFA prompt loop": [
                "it keeps asking me for the code again and again in a loop",
                "approve on phone, then it asks again on laptop, never ends",
                "verification keeps repeating every 5 minutes, very annoying",
            ],
        },
        "Group Membership": {
            "Shared mailbox or folder access": [
                "cannot open the team folder, says you do not have permission",
                "need to see the shared inbox that priya uses",
                "the drive that finance shared is not opening for me",
            ],
            "Application permission request": [
                "need edit rights in the reporting tool, i only have view",
                "i can see the dashboard but cannot download anything",
                "please give me approval rights for the requests queue",
            ],
        },
    },
    "Hardware": {
        "_group": "Desktop Support",
        "Laptop": {
            "Laptop slow or freezing": [
                "machine takes 15 mins to start, unusable in the morning",
                "everything hangs when i open more than 2 things",
                "very slow since last week, fan runs loud all the time",
            ],
            "Battery or charging fault": [
                "not charging even when plugged in, shows 4%",
                "battery drains in one hour, was fine before",
                "the adapter is warm but percentage keeps going down",
            ],
            "Screen or display fault": [
                "half the screen is flickering, lines coming",
                "display goes black randomly then comes back",
                "there is a crack after it fell, still working but hard to read",
            ],
        },
        "Peripherals": {
            "Docking station not working": [
                "the dock is dead, nothing connects when i put the laptop",
                "external monitors not detecting through the port replicator",
                "when i attach it the keyboard and mouse stop responding",
            ],
            "Keyboard or mouse fault": [
                "few keys not typing, mainly e and r",
                "the pointer jumps on its own while typing",
                "wireless mouse disconnects every few minutes",
            ],
            "Headset or audio device": [
                "no one can hear me on calls, tried both sides",
                "audio only comes in left side of the headphone",
                "mic is picking up too much noise, team complained",
            ],
        },
        "Printer": {
            "Printer offline": [
                "the machine on 3rd floor shows offline for everyone",
                "nothing prints, jobs just sit in the queue",
                "cannot find the device in the list anymore",
            ],
            "Print quality or paper jam": [
                "pages coming with lines across, toner maybe",
                "paper stuck inside, tried removing but still error",
                "output is very light, hard to read the invoice copies",
            ],
        },
        "Mobile": {
            "Company mobile setup": [
                "new handset given, need the work apps put on it",
                "cannot add my official mail on the new phone",
                "phone is not syncing anything from office",
            ],
        },
    },
    "Software & Applications": {
        "_group": "Application Support",
        "Office Productivity Suite": {
            "Spreadsheet crash or corruption": [
                "the file closes by itself every time i open the big sheet",
                "my workbook says it cannot be opened, worked yesterday",
                "keeps saying not responding when i refresh the pivot",
            ],
            "Document or slide app fault": [
                "the deck will not save, says file is in use",
                "formatting breaks when i reopen the document",
                "cannot open the attachment, unsupported format error",
            ],
        },
        "ERP System": {
            "ERP login failure": [
                "the finance system is throwing an error at login for me only",
                "cannot get into the module since the weekend patch",
                "it says session could not be created, others are fine",
            ],
            "ERP transaction error": [
                "posting fails with a dump error at the last step",
                "the entry is not going through, gives an error number",
                "batch job for month end failed midway again",
            ],
        },
        "CRM System": {
            "CRM sync or data issue": [
                "my opportunities are not showing the latest numbers",
                "the records i updated yesterday are missing today",
                "data from the marketing tool is not flowing in",
            ],
            "CRM report not loading": [
                "the pipeline view spins forever and never loads",
                "dashboard is blank for me but fine for my manager",
            ],
        },
        "Licensing": {
            "New license request": [
                "need the design tool for a project starting next month",
                "please arrange a seat for the analytics software",
                "my trial expired, i need the proper version now",
            ],
            "License expired or reassigned": [
                "it says my subscription has ended, cannot open anything",
                "the tool logged me out saying no seat available",
            ],
        },
        "Browser and Plugins": {
            "Add-in not loading": [
                "the toolbar button disappeared after the update",
                "extension is installed but nothing happens when i click",
            ],
            "Site not opening in browser": [
                "internal portal gives a certificate warning every time",
                "the page loads blank, works on my colleague machine",
            ],
        },
    },
    "Network & Connectivity": {
        "_group": "Network Operations",
        "VPN": {
            "VPN disconnects frequently": [
                "the tunnel drops every 20 minutes while working from home",
                "keeps disconnecting during calls, have to reconnect again and again",
                "connection is unstable since the new client version",
            ],
            "VPN will not connect": [
                "it just says connecting and stays there forever",
                "getting authentication failed when i try from home",
                "no connection from my home line since yesterday evening",
            ],
        },
        "WiFi": {
            "Weak WiFi in a zone": [
                "signal is very poor near the east side meeting rooms",
                "on the 4th floor it drops constantly, ground floor is fine",
                "cafeteria area has almost no connectivity",
            ],
            "Cannot join office WiFi": [
                "my laptop does not see the office network at all",
                "it asks for a certificate and then fails to join",
            ],
        },
        "LAN and Cabling": {
            "Port dead at desk": [
                "the wall socket at my new seat is not giving anything",
                "moved desks and now there is no connection through the cable",
            ],
        },
        "Bandwidth and Performance": {
            "Slow network performance": [
                "everything is crawling since 10am today across the floor",
                "file transfers to the server are taking forever this week",
            ],
        },
    },
    "Email & Collaboration": {
        "_group": "Messaging Support",
        "Mail Client": {
            "Mailbox full or quota": [
                "cannot send anything, says storage limit reached",
                "mails are bouncing back to senders, box seems full",
            ],
            "Mail not syncing": [
                "not receiving anything since morning but web version shows them",
                "sent items are not updating on my laptop",
            ],
        },
        "Meetings and Calls": {
            "Call quality poor": [
                "voice breaks badly in every call from my end",
                "video freezes for others while my network looks fine",
            ],
            "Cannot join or schedule meeting": [
                "the invite link says organiser has not started, but he has",
                "cannot book a room in the invite, option is greyed out",
            ],
        },
        "Document Collaboration": {
            "Site or library access": [
                "the team site says access denied after the migration",
                "cannot upload to the project library anymore",
            ],
        },
        "Distribution Lists": {
            "Distribution list change": [
                "please add the two new joiners to the delivery mail group",
                "i am still getting mails from a team i left",
            ],
        },
    },
    "Security & Compliance": {
        "_group": "Security Operations",
        "Phishing and Fraud": {
            "Suspicious email reported": [
                "got a mail asking for my details, looks fake, forwarding it",
                "someone claiming to be the director asked me for gift cards",
                "strange link in a mail from an unknown sender, did not click",
            ],
        },
        "Malware": {
            "Malware or virus alert": [
                "a warning popped up saying threat detected and quarantined",
                "my machine is behaving oddly after i opened an attachment",
            ],
        },
        "Data Access Control": {
            "Removable media exception": [
                "need to copy files to a pen drive for the client, it is blocked",
                "usb ports are disabled, i need it for one day only",
            ],
            "Sensitive data access request": [
                "need access to the payroll folder for the audit work",
                "requesting rights to the restricted client data set",
            ],
        },
        "Audit and Review": {
            "Access review or evidence request": [
                "auditors are asking for the list of who has access to the finance app",
                "need the login history for our team for last quarter",
            ],
        },
    },
}


def leaves():
    """Yield (l1, l2, l3, phrasings, assignment_group) for every leaf in the taxonomy."""
    for l1, subs in TAXONOMY.items():
        group = subs.get("_group", "Service Desk")
        for l2, issues in subs.items():
            if l2 == "_group":
                continue
            for l3, phrasings in issues.items():
                yield l1, l2, l3, phrasings, group


def allowed_paths():
    """Flat list of 'L1 > L2 > L3' strings. This is what the categorizer must choose from."""
    return [f"{l1} > {l2} > {l3}" for l1, l2, l3, _, _ in leaves()]

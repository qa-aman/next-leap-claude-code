# IT service desk taxonomy

Three tiers. **6 categories, 25 subcategories, 46 issue types.**

This file is generated from `scripts/taxonomy.py`, which is the source of truth. Edit the Python, then regenerate this.

The classifier must return a path that matches one of these rows character for character. Anything else is rejected, not silently accepted.

## Access & Identity

Handled by **IAM Support**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| Password | Password reset | "cant get into the system since morning, tried twice already" |
|  | Account locked after failed attempts | "account got blocked, i think i typed wrong 3 times" |
|  | Password expiry not notified | "no warning came and today it just stopped letting me in" |
| Account Provisioning | New joiner account setup | "new person joining monday in my team, nothing is set up for her yet" |
|  | Leaver account deactivation | "person left last friday, please close everything for him" |
|  | Role change access update | "moved from support to delivery team, my old screens are gone" |
| MFA | MFA device lost or replaced | "changed my phone, now the 6 digit code app is empty" |
|  | MFA prompt loop | "it keeps asking me for the code again and again in a loop" |
| Group Membership | Shared mailbox or folder access | "cannot open the team folder, says you do not have permission" |
|  | Application permission request | "need edit rights in the reporting tool, i only have view" |

## Hardware

Handled by **Desktop Support**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| Laptop | Laptop slow or freezing | "machine takes 15 mins to start, unusable in the morning" |
|  | Battery or charging fault | "not charging even when plugged in, shows 4%" |
|  | Screen or display fault | "half the screen is flickering, lines coming" |
| Peripherals | Docking station not working | "the dock is dead, nothing connects when i put the laptop" |
|  | Keyboard or mouse fault | "few keys not typing, mainly e and r" |
|  | Headset or audio device | "no one can hear me on calls, tried both sides" |
| Printer | Printer offline | "the machine on 3rd floor shows offline for everyone" |
|  | Print quality or paper jam | "pages coming with lines across, toner maybe" |
| Mobile | Company mobile setup | "new handset given, need the work apps put on it" |

## Software & Applications

Handled by **Application Support**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| Office Productivity Suite | Spreadsheet crash or corruption | "the file closes by itself every time i open the big sheet" |
|  | Document or slide app fault | "the deck will not save, says file is in use" |
| ERP System | ERP login failure | "the finance system is throwing an error at login for me only" |
|  | ERP transaction error | "posting fails with a dump error at the last step" |
| CRM System | CRM sync or data issue | "my opportunities are not showing the latest numbers" |
|  | CRM report not loading | "the pipeline view spins forever and never loads" |
| Licensing | New license request | "need the design tool for a project starting next month" |
|  | License expired or reassigned | "it says my subscription has ended, cannot open anything" |
| Browser and Plugins | Add-in not loading | "the toolbar button disappeared after the update" |
|  | Site not opening in browser | "internal portal gives a certificate warning every time" |

## Network & Connectivity

Handled by **Network Operations**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| VPN | VPN disconnects frequently | "the tunnel drops every 20 minutes while working from home" |
|  | VPN will not connect | "it just says connecting and stays there forever" |
| WiFi | Weak WiFi in a zone | "signal is very poor near the east side meeting rooms" |
|  | Cannot join office WiFi | "my laptop does not see the office network at all" |
| LAN and Cabling | Port dead at desk | "the wall socket at my new seat is not giving anything" |
| Bandwidth and Performance | Slow network performance | "everything is crawling since 10am today across the floor" |

## Email & Collaboration

Handled by **Messaging Support**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| Mail Client | Mailbox full or quota | "cannot send anything, says storage limit reached" |
|  | Mail not syncing | "not receiving anything since morning but web version shows them" |
| Meetings and Calls | Call quality poor | "voice breaks badly in every call from my end" |
|  | Cannot join or schedule meeting | "the invite link says organiser has not started, but he has" |
| Document Collaboration | Site or library access | "the team site says access denied after the migration" |
| Distribution Lists | Distribution list change | "please add the two new joiners to the delivery mail group" |

## Security & Compliance

Handled by **Security Operations**.

| Subcategory (L2) | Issue Type (L3) | What a user actually writes |
|---|---|---|
| Phishing and Fraud | Suspicious email reported | "got a mail asking for my details, looks fake, forwarding it" |
| Malware | Malware or virus alert | "a warning popped up saying threat detected and quarantined" |
| Data Access Control | Removable media exception | "need to copy files to a pen drive for the client, it is blocked" |
|  | Sensitive data access request | "need access to the payroll folder for the audit work" |
| Audit and Review | Access review or evidence request | "auditors are asking for the list of who has access to the finance app" |

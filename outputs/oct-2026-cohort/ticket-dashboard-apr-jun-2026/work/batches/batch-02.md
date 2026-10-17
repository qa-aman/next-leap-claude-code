# Classification batch 2 of 4

Domain: IT Service Desk.

Assign every case below to exactly one path from the allowed list.
Return one JSON object per line, nothing else:
`{"case_id":"C001","path":"L1 > L2 > L3","confidence":"High|Medium|Low","reason":"one short line"}`

Rules, and the reason each one exists:
1. The path must match the allowed list character for character. The next script rejects anything else rather than silently accepting an invented category.
2. If nothing fits, return `UNCATEGORIZED` with confidence `Low`. A forced fit is worse than an honest gap, because it hides in the numbers where nobody sees it.
3. `Low` confidence means a human must review it. You are allowed to not know.
4. Judge only from what the user wrote. Do not assume a team, a system or a cause that is not in the text.
5. `reason` is one short line a service desk manager could read and agree or disagree with. It is what makes the classification auditable.

## Allowed paths

- Access & Identity > Password > Password reset
- Access & Identity > Password > Account locked after failed attempts
- Access & Identity > Password > Password expiry not notified
- Access & Identity > Account Provisioning > New joiner account setup
- Access & Identity > Account Provisioning > Leaver account deactivation
- Access & Identity > Account Provisioning > Role change access update
- Access & Identity > MFA > MFA device lost or replaced
- Access & Identity > MFA > MFA prompt loop
- Access & Identity > Group Membership > Shared mailbox or folder access
- Access & Identity > Group Membership > Application permission request
- Hardware > Laptop > Laptop slow or freezing
- Hardware > Laptop > Battery or charging fault
- Hardware > Laptop > Screen or display fault
- Hardware > Peripherals > Docking station not working
- Hardware > Peripherals > Keyboard or mouse fault
- Hardware > Peripherals > Headset or audio device
- Hardware > Printer > Printer offline
- Hardware > Printer > Print quality or paper jam
- Hardware > Mobile > Company mobile setup
- Software & Applications > Office Productivity Suite > Spreadsheet crash or corruption
- Software & Applications > Office Productivity Suite > Document or slide app fault
- Software & Applications > ERP System > ERP login failure
- Software & Applications > ERP System > ERP transaction error
- Software & Applications > CRM System > CRM sync or data issue
- Software & Applications > CRM System > CRM report not loading
- Software & Applications > Licensing > New license request
- Software & Applications > Licensing > License expired or reassigned
- Software & Applications > Browser and Plugins > Add-in not loading
- Software & Applications > Browser and Plugins > Site not opening in browser
- Network & Connectivity > VPN > VPN disconnects frequently
- Network & Connectivity > VPN > VPN will not connect
- Network & Connectivity > WiFi > Weak WiFi in a zone
- Network & Connectivity > WiFi > Cannot join office WiFi
- Network & Connectivity > LAN and Cabling > Port dead at desk
- Network & Connectivity > Bandwidth and Performance > Slow network performance
- Email & Collaboration > Mail Client > Mailbox full or quota
- Email & Collaboration > Mail Client > Mail not syncing
- Email & Collaboration > Meetings and Calls > Call quality poor
- Email & Collaboration > Meetings and Calls > Cannot join or schedule meeting
- Email & Collaboration > Document Collaboration > Site or library access
- Email & Collaboration > Distribution Lists > Distribution list change
- Security & Compliance > Phishing and Fraud > Suspicious email reported
- Security & Compliance > Malware > Malware or virus alert
- Security & Compliance > Data Access Control > Removable media exception
- Security & Compliance > Data Access Control > Sensitive data access request
- Security & Compliance > Audit and Review > Access review or evidence request

## Cases

### C041  (covers 5 tickets)
- Short description: Please assist
- Description: HIS LAST WORKING DAY WAS 28TH, STILL SHOWING ACTIVE IN THE SYSTEM
- Departments: Engineering, Finance, Human Resources, Sales
- Channels: Email, Phone, Self-Service Portal

### C042  (covers 5 tickets)
- Short description: The team site says access denied
- Description: raising this again, the team site says access denied after the migration
- Departments: Customer Success, Finance, Manufacturing, Operations
- Channels: Chat, Email, Phone, Self-Service Portal

### C043  (covers 5 tickets)
- Short description: System not accepting my details after
- Description: team, system not accepting my details after i changed it last week let me know if you need anything from my side
- Departments: Customer Success, Engineering, Legal, Sales
- Channels: Email, Phone, Self-Service Portal

### C044  (covers 5 tickets)
- Short description: Did not get the 14 day
- Description: team, did not get the 14 day reminder, credentials expired suddenly
- Departments: Customer Success, Finance, Sales
- Channels: Phone, Self-Service Portal

### C045  (covers 4 tickets)
- Short description: Verification keeps repeating every 5 minutes
- Description: good morning, verification keeps repeating every 5 minutes, very annoying
- Departments: Finance, Legal, Marketing, Procurement
- Channels: Chat, Phone, Self-Service Portal

### C046  (covers 4 tickets)
- Short description: Transferred to another department, need the
- Description: second time reporting this, transferred to another department, need teh right screens now kindly look into it urgently
- Departments: Human Resources, Manufacturing, Marketing
- Channels: Chat, Self-Service Portal

### C047  (covers 4 tickets)
- Short description: Request
- Description: there is a crack after it fell, still working but hard to read kindly look into it urgently
- Departments: Customer Success, Manufacturing, Marketing
- Channels: Email, Self-Service Portal

### C048  (covers 4 tickets)
- Short description: Need access to the payroll folder
- Description: hi team, need access to the payroll folder for teh audit work this is blocking my work
- Departments: Manufacturing, Marketing, Procurement
- Channels: Chat, Phone, Self-Service Portal

### C049  (covers 4 tickets)
- Short description: The wall socket at my new
- Description: THE WALL SOCKET AT MY NEW SEAT IS NOT GIVING ANYTHING
- Departments: Customer Success, Human Resources, Legal, Marketing
- Channels: Self-Service Portal

### C050  (covers 4 tickets)
- Short description: The tool logged me out saying
- Description: hi, the tool logged me out saying no seat available appreciate a quick fix
- Departments: Engineering, Procurement
- Channels: Email, Phone, Self-Service Portal

### C051  (covers 4 tickets)
- Short description: Urgent help needed
- Description: TEH MACHINE ON 3RD FLOOR SHOWS OFFLINE FOR EVERYONE
- Departments: Customer Success, Legal, Marketing
- Channels: Phone, Self-Service Portal

### C052  (covers 4 tickets)
- Short description: The pointer jumps on its own
- Description: hi team, the pointer jumps on its own while typing
- Departments: Customer Success, Marketing, Operations
- Channels: Email, Self-Service Portal

### C053  (covers 4 tickets)
- Short description: Output is very light, hard to
- Description: GOOD MORNING, OUTPUT IS VERY LIGHT, HARD TO READ THE INVOICE COPIES KINDLY LOOK INTO IT URGENTLY
- Departments: Engineering, Operations, Procurement
- Channels: Email, Phone, Self-Service Portal

### C054  (covers 4 tickets)
- Short description: Not charging even when plugged in
- Description: hello, not charging even when plugged in, shows 4% let me know if you need anything from my side
- Departments: Engineering, Operations, Procurement
- Channels: Email, Self-Service Portal

### C055  (covers 4 tickets)
- Short description: The entry is not going through
- Description: good morning, the entry is nto going through, gives an error number thanks in advance
- Departments: Finance, Human Resources, Marketing
- Channels: Email, Phone, Self-Service Portal

### C056  (covers 4 tickets)
- Short description: Request
- Description: hello, the deck will not save, says file is in use
- Departments: Customer Success, Finance, Operations
- Channels: Phone, Self-Service Portal

### C057  (covers 4 tickets)
- Short description: IT issue
- Description: second time reporting this, resignation done, need the access removed before audit
- Departments: Customer Success, Finance, Marketing
- Channels: Email, Phone, Self-Service Portal

### C058  (covers 4 tickets)
- Short description: On the 4th floor it drops
- Description: team, on the 4th floor it drops constantly, ground floor is fine kindly look into it urgently
- Departments: Customer Success, Manufacturing, Marketing, Sales
- Channels: Email, Self-Service Portal

### C059  (covers 4 tickets)
- Short description: Urgent help needed
- Description: GOOD MORNING, MY LOGIN IS NOT WORKING. IT SAYS INVALID CREDENTIALS BUT IM SURE ITS RIGHT KINDLY LOOK INTO IT URGENTLY
- Departments: Customer Success, Operations, Procurement
- Channels: Email, Self-Service Portal

### C060  (covers 4 tickets)
- Short description: A warning popped up saying threat
- Description: good morning, a warning popped up saying threat detected and quarantined need this today
- Departments: Engineering, Human Resources, Marketing, Operations
- Channels: Email, Self-Service Portal

### C061  (covers 4 tickets)
- Short description: Audio only comes in left side
- Description: good morning, audio only comes in left side of the headphone
- Departments: Customer Success, Legal, Marketing, Operations
- Channels: Email, Phone, Self-Service Portal

### C062  (covers 4 tickets)
- Short description: Formatting breaks when i reopen the
- Description: formatting breaks when i reopen the document
- Departments: Finance, Sales
- Channels: Email, Self-Service Portal

### C063  (covers 4 tickets)
- Short description: Not working
- Description: hi team, approve on phone, then it asks again on laptop, never ends
- Departments: Engineering, Legal, Operations
- Channels: Email, Phone, Self-Service Portal

### C064  (covers 4 tickets)
- Short description: Extension is installed but nothing happens
- Description: raising this again, extension is installed but nothing happens when i click
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Email, Phone

### C065  (covers 4 tickets)
- Short description: Lost my handset yesterday, cannot get
- Description: second time reporting this, lost my handset yesterday, cannt get teh verification code need this today
- Departments: Customer Success, Engineering, Procurement
- Channels: Email, Self-Service Portal

### C066  (covers 4 tickets)
- Short description: Auditors are asking for the list
- Description: raising this again, auditors are asking for teh list of who has acces to the finance app need this today
- Departments: Human Resources, Manufacturing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C067  (covers 4 tickets)
- Short description: Few keys not typing, mainly e
- Description: few keys not typing, mainly e and r
- Departments: Engineering, Human Resources, Legal, Procurement
- Channels: Chat, Phone, Self-Service Portal

### C068  (covers 3 tickets)
- Short description: System problem
- Description: the records i updated yesterday are missing today need this today
- Departments: Customer Success, Marketing, Sales
- Channels: Chat, Email, Self-Service Portal

### C069  (covers 3 tickets)
- Short description: Internal portal gives a certificate warning
- Description: hi team, internal portal gives a certificate warning every time
- Departments: Customer Success, Marketing, Operations
- Channels: Chat, Email

### C070  (covers 3 tickets)
- Short description: Our new hire has no login
- Description: raising this again, our new hire has no login, laptop is there but cannot start
- Departments: Customer Success, Engineering, Marketing
- Channels: Email, Self-Service Portal

### C071  (covers 3 tickets)
- Short description: I can see the dashboard but
- Description: hi team, i can see the dashboard but cannot download anything kindly look into it urgently
- Departments: Engineering, Legal, Marketing
- Channels: Chat, Self-Service Portal

### C072  (covers 3 tickets)
- Short description: Pages coming with lines across, toner
- Description: pages coming with lines across, toner maybe thanks in advance
- Departments: Finance, Marketing, Operations
- Channels: Email, Phone, Self-Service Portal

### C073  (covers 3 tickets)
- Short description: Paper stuck inside, tried removing but
- Description: hello, paper stuck inside, tried removing but still error thanks in advance
- Departments: Engineering, Human Resources, Legal
- Channels: Email, Phone, Self-Service Portal

### C074  (covers 3 tickets)
- Short description: Please assist
- Description: team, cannot find the device in the list anymore please help
- Departments: Customer Success, Human Resources, Sales
- Channels: Phone, Self-Service Portal

### C075  (covers 3 tickets)
- Short description: Got a mail asking for my
- Description: TEAM, GOT A MAIL ASKING FOR MY DETAILS, LOOKS FAKE, FORWARDING IT APPRECIATE A QUICK FIX
- Departments: Customer Success, Legal, Manufacturing
- Channels: Chat, Email, Self-Service Portal

### C076  (covers 3 tickets)
- Short description: Cannot open the attachment, unsupported format
- Description: team, cannot open the attachment, unsupported format error
- Departments: Human Resources, Marketing, Procurement
- Channels: Chat, Self-Service Portal

### C077  (covers 3 tickets)
- Short description: Please arrange a seat for the
- Description: team, please arrange a seat for the analytics software need this today
- Departments: Engineering, Marketing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C078  (covers 3 tickets)
- Short description: Request
- Description: second time reporting this, cafeteria area has almost no connectivity
- Departments: Customer Success, Human Resources, Sales
- Channels: Phone, Self-Service Portal

### C079  (covers 3 tickets)
- Short description: Locked out again. need it opened
- Description: locked out again. need it opened asap, have a client call at 11
- Departments: Human Resources, Manufacturing
- Channels: Phone, Self-Service Portal

### C080  (covers 3 tickets)
- Short description: Very slow since last week, fan
- Description: VERY SLOW SINCE LAST WEEK, FAN RUNS LOUD ALL THE TIME
- Departments: Customer Success, Engineering, Procurement
- Channels: Chat, Phone, Self-Service Portal

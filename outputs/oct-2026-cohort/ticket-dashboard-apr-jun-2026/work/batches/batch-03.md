# Classification batch 3 of 4

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

### C081  (covers 3 tickets)
- Short description: Urgent help needed
- Description: hi team, teh pipeline view spins forever and never loads appreciate a quick fix
- Departments: Marketing, Procurement, Sales
- Channels: Phone, Self-Service Portal

### C082  (covers 3 tickets)
- Short description: System problem
- Description: hello, cant get into the system since morning, tried twice already
- Departments: Human Resources, Legal, Marketing
- Channels: Email, Self-Service Portal

### C083  (covers 3 tickets)
- Short description: Need support
- Description: good morning, when i attach it the keyboard and mouse stop responding need this today
- Departments: Engineering, Human Resources, Operations
- Channels: Chat, Phone, Self-Service Portal

### C084  (covers 3 tickets)
- Short description: System problem
- Description: hello, the file closes by itself every time i open the big sheet appreciate a quick fix
- Departments: Engineering, Marketing, Operations
- Channels: Email, Self-Service Portal

### C085  (covers 3 tickets)
- Short description: Promoted last month but still seeing
- Description: HELLO, PROMOTED LAST MONTH BUT STILL SEEING THE OLD MENU OPTIONS APPRECIATE A QUICK FIX
- Departments: Legal, Manufacturing
- Channels: Chat, Phone, Self-Service Portal

### C086  (covers 2 tickets)
- Short description: Signal is very poor near the
- Description: signal is very poor near the east side meeting rooms let me know if you need anything from my side
- Departments: Engineering, Sales
- Channels: Self-Service Portal

### C087  (covers 2 tickets)
- Short description: File transfers to the server are
- Description: SECOND TIME REPORTING THIS, FILE TRANSFERS TO THE SERVER ARE TAKING FOREVER THIS WEEK NEED THIS TODAY
- Departments: Human Resources, Marketing
- Channels: Email

### C088  (covers 2 tickets)
- Short description: External monitors not detecting through the
- Description: good morning, external monitors not detecting through the port replicator this is blocking my work
- Departments: Customer Success, Operations
- Channels: Self-Service Portal

### C089  (covers 2 tickets)
- Short description: Please assist
- Description: hello, cannt send anything, says storage limit reached this is blocking my work
- Departments: Marketing, Sales
- Channels: Email, Self-Service Portal

### C090  (covers 2 tickets)
- Short description: Request
- Description: the adapter is warm but percentage keeps going down
- Departments: Finance, Sales
- Channels: Self-Service Portal

### C091  (covers 2 tickets)
- Short description: Data from the marketing tool is
- Description: data from the marketing tool is not flowing in
- Departments: Marketing, Sales
- Channels: Email, Self-Service Portal

### C092  (covers 2 tickets)
- Short description: Urgent help needed
- Description: TEAM, DASHBOARD IS BLANK FOR ME BUT FINE FOR MY MANAGER
- Departments: Customer Success, Legal
- Channels: Self-Service Portal

### C093  (covers 2 tickets)
- Short description: Cannot open the team folder, says
- Description: cannot open the team folder, says you do not have permission thanks in advance
- Departments: Engineering, Finance
- Channels: Email, Self-Service Portal

### C094  (covers 2 tickets)
- Short description: Cannot add my official mail on
- Description: cannot add my official mail on the new phone let me know if you need anything from my side
- Departments: Customer Success
- Channels: Email

### C095  (covers 2 tickets)
- Short description: Issue
- Description: hi, it says too many attempts, locked. pls unlock appreciate a quick fix
- Departments: Finance, Human Resources
- Channels: Self-Service Portal

### C096  (covers 2 tickets)
- Short description: New device, the authenticator is not
- Description: new device, teh authenticator is nto showing anything for work this is blocking my work
- Departments: Customer Success, Legal
- Channels: Self-Service Portal

### C097  (covers 2 tickets)
- Short description: Request
- Description: second time reporting this, need the design tool for a project starting next month
- Departments: Engineering, Operations
- Channels: Phone

### C098  (covers 2 tickets)
- Short description: Need edit rights in the reporting
- Description: raising this again, need edit rights in teh reporting tool, i only have view
- Departments: Finance, Procurement
- Channels: Self-Service Portal

### C099  (covers 2 tickets)
- Short description: Need access to the payroll folder
- Description: need acces to teh payroll folder for teh audit work plz help
- Departments: Marketing
- Channels: Email

### C100  (covers 2 tickets)
- Short description: Issue
- Description: second time reporting this, machine takes 15 mins to start, unusable in teh mornign let me know if you need anything from my side
- Departments: Engineering, Procurement
- Channels: Chat, Self-Service Portal

### C101  (covers 2 tickets)
- Short description: My opportunities are not showing the
- Description: my opportunities are not showing the latest numbers this is blocking my work
- Departments: Legal, Manufacturing
- Channels: Email, Self-Service Portal

### C102  (covers 1 ticket)
- Short description: The invite link says organiser has
- Description: the invite link says organiser has not started, but he has
- Departments: Engineering
- Channels: Self-Service Portal

### C103  (covers 1 ticket)
- Short description: Battery drains in one hour, was
- Description: HELLO, BATTERY DRAINS IN ONE HOUR, WAS FINE BEFORE THIS IS BLOCKING MY WORK
- Departments: Engineering
- Channels: Email

### C104  (covers 1 ticket)
- Short description: Batch job for month end failed
- Description: SECOND TIME REPORTING THIS, BATCH JOB FOR MONTH END FAILED MIDWAY AGAIN APPRECIATE A QUICK FIX
- Departments: Marketing
- Channels: Email

### C105  (covers 1 ticket)
- Short description: Usb ports are disabled, i need
- Description: hello, usb ports are disabled, i need it for one day only thanks in advance
- Departments: Human Resources
- Channels: Email

### C106  (covers 1 ticket)
- Short description: Changed my phone, now the 6
- Description: raising this again, changed my phone, now teh 6 digit code app is empty plz help
- Departments: Legal
- Channels: Self-Service Portal

### C107  (covers 1 ticket)
- Short description: Not working
- Description: moved from support to delivery team, my old screens are gone
- Departments: Manufacturing
- Channels: Email

### C108  (covers 1 ticket)
- Short description: Requesting rights to the restricted client
- Description: second time reporting this, requesting rights to the restricted client data set need this today
- Departments: Finance
- Channels: Phone

### C109  (covers 1 ticket)
- Short description: Not working
- Description: hello, the drive that finance shared is not opening for me this is blocking my work
- Departments: Legal
- Channels: Phone

### C110  (covers 1 ticket)
- Short description: It says session could not be
- Description: HI, IT SAYS SESSION COULD NOT BE CREATED, OTHERS ARE FINE
- Departments: Sales
- Channels: Phone

### C111  (covers 1 ticket)
- Short description: Moved desks and now there is
- Description: raising this again, moved desks and now there is no connection through teh cable
- Departments: Manufacturing
- Channels: Phone

### C112  (covers 1 ticket)
- Short description: Request
- Description: GOOD MORNING, MIC IS PICKING UP TOO MUCH NOISE, TEAM COMPLAINED NEED THIS TODAY
- Departments: Operations
- Channels: Email

### C113  (covers 1 ticket)
- Short description: Need the login history for our
- Description: need teh login history for our team for last quarter please help
- Departments: Legal
- Channels: Email

### C114  (covers 1 ticket)
- Short description: Need to copy files to a
- Description: need to copy files to a pen drive for the client, it is blocked kindly look into it urgently
- Departments: Operations
- Channels: Self-Service Portal

### C115  (covers 1 ticket)
- Short description: Not working
- Description: hello, need to see the shared inbox that priya uses
- Departments: Sales
- Channels: Phone

### C116  (covers 1 ticket)
- Short description: Please assist
- Description: good morning, new person joining monday in my team, nothing is set up for her yet
- Departments: Marketing
- Channels: Phone

### C117  (covers 1 ticket)
- Short description: No one can hear me on
- Description: hello, no one can hear me on calls, tried both sides
- Departments: Legal
- Channels: Self-Service Portal

### C118  (covers 1 ticket)
- Short description: It just says connecting and stays
- Description: it just says connecting and stays there forever plz help
- Departments: Human Resources
- Channels: Self-Service Portal

### C119  (covers 1 ticket)
- Short description: The dock is dead, nothing connects
- Description: the dock is dead, nothing connects when i put the laptop
- Departments: Legal
- Channels: Email

### C120  (covers 1 ticket)
- Short description: Nothing prints, jobs just sit in
- Description: GOOD MORNING, NOTHING PRINTS, JOBS JUST SIT IN TEH QUEUE KINDLY LOOK INTO IT URGENTLY
- Departments: Operations
- Channels: Phone

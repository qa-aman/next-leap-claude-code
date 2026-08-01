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
- Short description: System problem
- Description: hi, keeps disconnecting during calls, have to reconnect again and again this is blocking my work
- Departments: Customer Success, Engineering, Operations
- Channels: Email, Self-Service Portal

### C082  (covers 3 tickets)
- Short description: Verification keeps repeating every 5 minutes
- Description: verification keeps repeating every 5 minutes, very annoying please help
- Departments: Customer Success, Procurement
- Channels: Chat, Email, Phone

### C083  (covers 3 tickets)
- Short description: The tunnel drops every 20 minutes
- Description: team, the tunnel drops every 20 minutes while working from home kindly look into it urgently
- Departments: Human Resources, Legal, Marketing
- Channels: Email, Self-Service Portal

### C084  (covers 3 tickets)
- Short description: Need the login history for our
- Description: HI, NEED THE LOGIN HISTORY FOR OUR TEAM FOR LAST QUARTER NEED THIS TODAY
- Departments: Finance, Legal, Procurement
- Channels: Email, Phone, Self-Service Portal

### C085  (covers 3 tickets)
- Short description: The toolbar button disappeared after the
- Description: hello, the toolbar button disappeared after the update appreciate a quick fix
- Departments: Customer Success, Human Resources, Marketing
- Channels: Email, Phone, Self-Service Portal

### C086  (covers 2 tickets)
- Short description: Transferred to another department, need the
- Description: hi, transferred to another department, need the right screens now
- Departments: Engineering, Operations
- Channels: Email, Self-Service Portal

### C087  (covers 2 tickets)
- Short description: There is a crack after it
- Description: RAISING THIS AGAIN, THERE IS A CRACK AFTER IT FELL, STILL WORKIGN BUT HARD TO READ LET ME KNOW IF YOU NEED ANYTHING FROM MY SIDE
- Departments: Engineering, Marketing
- Channels: Phone

### C088  (covers 2 tickets)
- Short description: The wall socket at my new
- Description: raising this again, the wall socket at my new seat is not giving anything this is blocking my work
- Departments: Customer Success, Legal
- Channels: Phone, Self-Service Portal

### C089  (covers 2 tickets)
- Short description: The machine on 3rd floor shows
- Description: hi, teh machine on 3rd floor shows offline for everyone appreciate a quick fix
- Departments: Finance, Sales
- Channels: Chat, Email

### C090  (covers 2 tickets)
- Short description: Please assist
- Description: second time reporting this, display goes black randomly then comes back appreciate a quick fix
- Departments: Finance, Manufacturing
- Channels: Chat, Email

### C091  (covers 2 tickets)
- Short description: Everything is crawling since 10am today
- Description: everything is crawling since 10am today across teh floor let me know if you need anything from my side
- Departments: Engineering, Procurement
- Channels: Email

### C092  (covers 2 tickets)
- Short description: Please assist
- Description: GOOD MORNING, EXTENSION IS INSTALLED BUT NOTHING HAPPENS WHEN I CLICK
- Departments: Engineering, Operations
- Channels: Phone, Self-Service Portal

### C093  (covers 2 tickets)
- Short description: External monitors not detecting through the
- Description: external monitors not detecting through the port replicator
- Departments: Legal, Operations
- Channels: Self-Service Portal

### C094  (covers 2 tickets)
- Short description: Moved from support to delivery team
- Description: moved from support to delivery team, my old screens are gone
- Departments: Legal, Procurement
- Channels: Phone, Self-Service Portal

### C095  (covers 2 tickets)
- Short description: Need support
- Description: hello, file transfers to the server are taking forever this week plz help
- Departments: Legal, Manufacturing
- Channels: Phone, Self-Service Portal

### C096  (covers 2 tickets)
- Short description: Output is very light, hard to
- Description: team, output is very light, hard to read the invoice copies
- Departments: Finance, Human Resources
- Channels: Email, Self-Service Portal

### C097  (covers 2 tickets)
- Short description: It keeps asking me for the
- Description: hi, it keeps asking me for the code again and again in a loop
- Departments: Customer Success, Sales
- Channels: Phone, Self-Service Portal

### C098  (covers 2 tickets)
- Short description: No one can hear me on
- Description: hi, no one can hear me on calls, tried both sides thanks in advance
- Departments: Operations, Sales
- Channels: Email, Phone

### C099  (covers 2 tickets)
- Short description: On the 4th floor it drops
- Description: second time reporting this, on the 4th floor it drops constantly, ground floor is fine thanks in advance
- Departments: Legal, Marketing
- Channels: Email, Self-Service Portal

### C100  (covers 2 tickets)
- Short description: Our new hire has no login
- Description: raising this again, our new hire has no login, laptop is there but cannot start need this today
- Departments: Legal, Manufacturing
- Channels: Email, Self-Service Portal

### C101  (covers 2 tickets)
- Short description: Need the design tool for a
- Description: hi, need the design tool for a project starting next month
- Departments: Operations, Procurement
- Channels: Email, Phone

### C102  (covers 2 tickets)
- Short description: Approve on phone, then it asks
- Description: SECOND TIME REPORTING THIS, APPROVE ON PHONE, THEN IT ASKS AGIAN ON LAPTOP, NEVER ENDS
- Departments: Marketing, Sales
- Channels: Chat, Email

### C103  (covers 2 tickets)
- Short description: I can see the dashboard but
- Description: second time reporting this, i can see the dashboard but cannt download anything
- Departments: Customer Success, Human Resources
- Channels: Email, Phone

### C104  (covers 2 tickets)
- Short description: Person left last friday, please close
- Description: second time reporting this, person left last friday, please close everything for him kindly look into it urgently
- Departments: Engineering, Manufacturing
- Channels: Self-Service Portal

### C105  (covers 2 tickets)
- Short description: Getting authentication failed when i try
- Description: GETTING AUTHENTICATION FAILED WHEN I TRY FROM HOME PLEASE HELP
- Departments: Engineering, Finance
- Channels: Phone, Self-Service Portal

### C106  (covers 2 tickets)
- Short description: Please assist
- Description: good morning, moved from support to delivery team, my old screens are gone plz help
- Departments: Procurement, Sales
- Channels: Email, Self-Service Portal

### C107  (covers 2 tickets)
- Short description: Need to copy files to a
- Description: need to copy files to a pen drive for the client, it is blocked thanks in advance
- Departments: Manufacturing, Procurement
- Channels: Chat, Email

### C108  (covers 1 ticket)
- Short description: My machine is behaving oddly after
- Description: good morning, my machine is behaving oddly after i opened an attachment plz help
- Departments: Operations
- Channels: Self-Service Portal

### C109  (covers 1 ticket)
- Short description: System problem
- Description: raising this again, batch job for month end failed midway agian
- Departments: Operations
- Channels: Self-Service Portal

### C110  (covers 1 ticket)
- Short description: Please assist
- Description: team, my workbook says it cannot be opened, worked yesterday plz help
- Departments: Operations
- Channels: Self-Service Portal

### C111  (covers 1 ticket)
- Short description: Please assist
- Description: usb ports are disabled, i need it for one day only
- Departments: Operations
- Channels: Email

### C112  (covers 1 ticket)
- Short description: Request
- Description: raising this again, need access to the payroll folder for the audit work kindly look into it urgently
- Departments: Operations
- Channels: Self-Service Portal

### C113  (covers 1 ticket)
- Short description: Need edit rights in the reporting
- Description: need edit rights in the reporting tool, i only have view please help
- Departments: Human Resources
- Channels: Self-Service Portal

### C114  (covers 1 ticket)
- Short description: When i attach it the keyboard
- Description: SECOND TIME REPORTING THIS, WHEN I ATTACH IT THE KEYBOARD AND MOUSE STOP RESPONDING LET ME KNOW IF YOU NEED ANYTHING FROM MY SIDE
- Departments: Sales
- Channels: Email

### C115  (covers 1 ticket)
- Short description: It says session could not be
- Description: hello, it says session could not be created, others are fine plz help
- Departments: Legal
- Channels: Phone

### C116  (covers 1 ticket)
- Short description: No connection from my home line
- Description: no connection from my home line since yesterday evening plz help
- Departments: Human Resources
- Channels: Email

### C117  (covers 1 ticket)
- Short description: Issue
- Description: it keeps asking me for the code again and agian in a loop plz help
- Departments: Finance
- Channels: Email

### C118  (covers 1 ticket)
- Short description: Cannot add my official mail on
- Description: hi, cannt add my official mail on teh new phone
- Departments: Procurement
- Channels: Self-Service Portal

### C119  (covers 1 ticket)
- Short description: Resignation done, need the access removed
- Description: good morning, resignation done, need the access removed before audit
- Departments: Sales
- Channels: Self-Service Portal

### C120  (covers 1 ticket)
- Short description: It just says connecting and stays
- Description: it just says connecting adn stays there forever plz help
- Departments: Procurement
- Channels: Self-Service Portal

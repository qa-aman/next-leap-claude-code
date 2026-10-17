# Classification batch 1 of 4

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

### C001  (covers 13 tickets)
- Short description: The tunnel drops every 20 minutes
- Description: THE TUNNEL DROPS EVERY 20 MINUTES WHILE WORKIGN FROM HOME
- Departments: Customer Success, Engineering, Human Resources, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C002  (covers 13 tickets)
- Short description: It just says connecting and stays
- Description: second time reporting this, it just says connecting and stays there forever let me know if you need anything from my side
- Departments: Engineering, Human Resources, Manufacturing, Marketing
- Channels: Chat, Email, Phone, Self-Service Portal

### C003  (covers 10 tickets)
- Short description: No warning came and today it
- Description: TEAM, NO WARNING CAME ADN TODAY IT JUST STOPPED LETTING ME IN
- Departments: Engineering, Finance, Legal, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C004  (covers 10 tickets)
- Short description: Connection is unstable since the new
- Description: HI TEAM, CONNECTION IS UNSTABLE SINCE THE NEW CLIENT VERSION THANKS IN ADVANCE
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Email, Self-Service Portal

### C005  (covers 10 tickets)
- Short description: No connection from my home line
- Description: no connection from my home line since yesterday evening
- Departments: Customer Success, Engineering, Finance, Legal
- Channels: Chat, Email, Phone, Self-Service Portal

### C006  (covers 10 tickets)
- Short description: I am unable to sign in
- Description: i am unable to sign in, message says account is locked contact admin kindly look into it urgently
- Departments: Customer Success, Finance, Legal, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C007  (covers 9 tickets)
- Short description: Not working
- Description: MAILS ARE BOUNCING BACK TO SENDERS, BOX SEEMS FULL LET ME KNOW IF YOU NEED ANYTHING FROM MY SIDE
- Departments: Engineering, Finance, Human Resources, Legal
- Channels: Chat, Email, Phone, Self-Service Portal

### C008  (covers 9 tickets)
- Short description: Urgent help needed
- Description: getting authentication failed when i try from home
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Email, Phone, Self-Service Portal

### C009  (covers 8 tickets)
- Short description: Not working
- Description: half the screen is flickering, lines coming
- Departments: Customer Success, Engineering, Marketing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C010  (covers 8 tickets)
- Short description: Not receiving anything since morning but
- Description: second time reporting this, not receiving anything since mornign but web version shows them kindly look into it urgently
- Departments: Engineering, Finance, Legal, Marketing
- Channels: Email, Self-Service Portal

### C011  (covers 8 tickets)
- Short description: Blocked out of the portal, keeps
- Description: HI, BLOCKED OUT OF THE PORTAL, KEEPS SAYING ACCOUNT DISABLED THANKS IN ADVANCE
- Departments: Engineering, Legal, Manufacturing, Marketing
- Channels: Chat, Email, Phone, Self-Service Portal

### C012  (covers 8 tickets)
- Short description: My laptop does not see the
- Description: hi team, my laptop does nto see the office network at all kindly look into it urgently
- Departments: Customer Success, Finance, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C013  (covers 8 tickets)
- Short description: System problem
- Description: GOOD MORNING, CHANGED MY PHONE, NOW THE 6 DIGIT CODE APP IS EMPTY APPRECIATE A QUICK FIX
- Departments: Engineering, Finance, Human Resources, Marketing
- Channels: Chat, Email, Phone, Self-Service Portal

### C014  (covers 7 tickets)
- Short description: Not working
- Description: hello, i am still getting mails from a team i left appreciate a quick fix
- Departments: Finance, Human Resources, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C015  (covers 7 tickets)
- Short description: Expired without any mail to me
- Description: hi team, expired without any mail to me, now i cant work
- Departments: Customer Success, Finance, Legal, Manufacturing
- Channels: Phone, Self-Service Portal

### C016  (covers 7 tickets)
- Short description: Sent items are not updating on
- Description: team, sent items are not updating on my laptop need this today
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Email, Self-Service Portal

### C017  (covers 7 tickets)
- Short description: Request
- Description: everything hangs when i open more than 2 things
- Departments: Engineering, Manufacturing, Operations, Procurement
- Channels: Chat, Email, Phone, Self-Service Portal

### C018  (covers 7 tickets)
- Short description: Please assist
- Description: second time reporting this, forgot the credentials after the holiday, please help
- Departments: Human Resources, Legal, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C019  (covers 7 tickets)
- Short description: IT issue
- Description: hi team, video freezes for others while my network looks fine let me know if you need anything from my side
- Departments: Engineering, Finance, Human Resources, Legal
- Channels: Chat, Phone, Self-Service Portal

### C020  (covers 7 tickets)
- Short description: System problem
- Description: the page loads blank, works on my colleague machine
- Departments: Engineering, Human Resources, Manufacturing, Sales
- Channels: Email, Self-Service Portal

### C021  (covers 7 tickets)
- Short description: Issue
- Description: second time reporting this, cannot upload to teh project library anymore kindly look into it urgently
- Departments: Customer Success, Engineering, Finance, Legal
- Channels: Email, Phone, Self-Service Portal

### C022  (covers 7 tickets)
- Short description: Keeps disconnecting during calls, have to
- Description: keeps disconnecting during calls, have to reconnect again and again thanks in advance
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Chat, Email, Phone, Self-Service Portal

### C023  (covers 7 tickets)
- Short description: Keeps saying not responding when i
- Description: hi team, keeps saying not responding when i refresh the pivot
- Departments: Customer Success, Engineering, Legal, Manufacturing
- Channels: Email, Phone, Self-Service Portal

### C024  (covers 7 tickets)
- Short description: Need support
- Description: PLEASE ADD THE TWO NEW JOINERS TO THE DELIVERY MAIL GROUP NEED THIS TODAY
- Departments: Engineering, Finance, Human Resources, Operations
- Channels: Chat, Email, Self-Service Portal

### C025  (covers 7 tickets)
- Short description: Cannot book a room in the
- Description: good morning, cannot book a room in the invite, option is greyed out let me know if you need anything from my side
- Departments: Engineering, Legal, Manufacturing, Procurement
- Channels: Chat, Email, Phone, Self-Service Portal

### C026  (covers 7 tickets)
- Short description: My workbook says it cannot be
- Description: my workbook says it cannot be opened, worked yesterday thanks in advance
- Departments: Finance, Human Resources, Manufacturing, Operations
- Channels: Chat, Email, Phone, Self-Service Portal

### C027  (covers 6 tickets)
- Short description: It asks for a certificate and
- Description: team, it asks for a certificate and then fails to join
- Departments: Human Resources, Marketing, Procurement
- Channels: Chat, Email, Self-Service Portal

### C028  (covers 6 tickets)
- Short description: Posting fails with a dump error
- Description: hi team, posting fails with a dump error at the last step need this today
- Departments: Engineering, Human Resources, Legal, Marketing
- Channels: Chat, Email, Phone, Self-Service Portal

### C029  (covers 6 tickets)
- Short description: System problem
- Description: someone claiming to be the director asked me for gift cards need this today
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Email, Self-Service Portal

### C030  (covers 6 tickets)
- Short description: Urgent help needed
- Description: second time reporting this, it says my subscription has ended, cannot open anything let me know if you need anything from my side
- Departments: Finance, Human Resources, Marketing, Operations
- Channels: Phone, Self-Service Portal

### C031  (covers 6 tickets)
- Short description: Need support
- Description: raising this again, voice breaks badly in every call from my end need this today
- Departments: Customer Success, Legal, Manufacturing, Sales
- Channels: Chat, Email, Phone, Self-Service Portal

### C032  (covers 6 tickets)
- Short description: System problem
- Description: hi team, everything is crawling since 10am today across the floor
- Departments: Human Resources, Manufacturing, Operations, Sales
- Channels: Chat, Email, Self-Service Portal

### C033  (covers 6 tickets)
- Short description: It keeps asking me for the
- Description: good morning, it keeps asking me for teh code agian and again in a loop appreciate a quick fix
- Departments: Customer Success, Finance, Manufacturing, Operations
- Channels: Email, Phone, Self-Service Portal

### C034  (covers 6 tickets)
- Short description: Need support
- Description: the finance system is throwing an error at login for me only
- Departments: Customer Success, Engineering, Manufacturing, Sales
- Channels: Email, Phone

### C035  (covers 6 tickets)
- Short description: Account got blocked, i think i
- Description: second time reporting this, account got blocked, i think i typed wrong 3 times
- Departments: Customer Success, Finance, Operations, Sales
- Channels: Email, Self-Service Portal

### C036  (covers 6 tickets)
- Short description: Cannot get into the module since
- Description: second time reporting this, cannt get into teh module since teh weekend patch thanks in advance
- Departments: Customer Success, Engineering, Manufacturing, Sales
- Channels: Email, Phone, Self-Service Portal

### C037  (covers 6 tickets)
- Short description: The toolbar button disappeared after the
- Description: second time reporting this, the toolbar button disappeared after the update
- Departments: Finance, Legal, Manufacturing, Marketing
- Channels: Phone, Self-Service Portal

### C038  (covers 6 tickets)
- Short description: My trial expired, i need the
- Description: team, my trial expired, i need the proper version now need this today
- Departments: Engineering, Legal, Marketing, Operations
- Channels: Chat, Email, Self-Service Portal

### C039  (covers 5 tickets)
- Short description: IT issue
- Description: HI, NEW HANDSET GIVEN, NEED THE WORK APPS PUT ON IT PLEASE HELP
- Departments: Engineering, Finance, Marketing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C040  (covers 5 tickets)
- Short description: Strange link in a mail from
- Description: hi, strange link in a mail from an unknown sender, did nto click appreciate a quick fix
- Departments: Engineering, Human Resources, Procurement
- Channels: Email, Self-Service Portal

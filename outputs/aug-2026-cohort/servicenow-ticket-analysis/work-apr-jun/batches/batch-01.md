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
- Short description: Expired without any mail to me
- Description: expired without any mail to me, now i cant work
- Departments: Customer Success, Engineering, Manufacturing, Marketing
- Channels: Chat, Email, Phone, Self-Service Portal

### C002  (covers 11 tickets)
- Short description: Account got blocked, i think i
- Description: good morning, account got blocked, i think i typed wrong 3 times
- Departments: Human Resources, Manufacturing, Operations, Procurement
- Channels: Chat, Email, Phone, Self-Service Portal

### C003  (covers 10 tickets)
- Short description: I am unable to sign in
- Description: hello, i am unable to sign in, message says account is locked contact admin let me know if you need anything from my side
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Chat, Email, Phone, Self-Service Portal

### C004  (covers 10 tickets)
- Short description: No warning came and today it
- Description: hello, no warning came and today it just stopped letting me in please help
- Departments: Customer Success, Finance, Human Resources, Manufacturing
- Channels: Email, Phone, Self-Service Portal

### C005  (covers 10 tickets)
- Short description: System problem
- Description: team, my login is not working. it says invalid credentials but im sure its right let me know if you need anything from my side
- Departments: Customer Success, Finance, Human Resources, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C006  (covers 10 tickets)
- Short description: Urgent help needed
- Description: hi, posting fails with a dump error at the last step let me know if you need anything from my side
- Departments: Customer Success, Engineering, Human Resources, Manufacturing
- Channels: Email, Phone, Self-Service Portal

### C007  (covers 10 tickets)
- Short description: Did not get the 14 day
- Description: did not get the 14 day reminder, credentials expired suddenly this is blocking my work
- Departments: Customer Success, Finance, Human Resources, Legal
- Channels: Chat, Email, Phone, Self-Service Portal

### C008  (covers 10 tickets)
- Short description: Cannot send anything, says storage limit
- Description: good morning, cannot send anything, says storage limit reached
- Departments: Engineering, Finance, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C009  (covers 9 tickets)
- Short description: Blocked out of the portal, keeps
- Description: hello, blocked out of the portal, keeps saying account disabled
- Departments: Customer Success, Engineering, Finance, Manufacturing
- Channels: Email, Phone, Self-Service Portal

### C010  (covers 9 tickets)
- Short description: Cannot upload to the project library
- Description: good morning, cannot upload to the project library anymore thanks in advance
- Departments: Customer Success, Engineering, Finance, Human Resources
- Channels: Email, Phone, Self-Service Portal

### C011  (covers 8 tickets)
- Short description: Please assist
- Description: raising this again, cant get into the system since morning, tried twice already this is blocking my work
- Departments: Finance, Human Resources, Legal, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C012  (covers 8 tickets)
- Short description: Not working
- Description: HI, NO CONNECTION FROM MY HOME LINE SINCE YESTERDAY EVENING PLEASE HELP
- Departments: Customer Success, Finance, Human Resources, Manufacturing
- Channels: Email, Phone, Self-Service Portal

### C013  (covers 8 tickets)
- Short description: Sent items are not updating on
- Description: second time reporting this, sent items are not updating on my laptop
- Departments: Customer Success, Engineering, Legal, Manufacturing
- Channels: Chat, Phone, Self-Service Portal

### C014  (covers 8 tickets)
- Short description: Not working
- Description: MY WORKBOOK SAYS IT CANNOT BE OPENED, WORKED YESTERDAY KINDLY LOOK INTO IT URGENTLY
- Departments: Human Resources, Marketing, Operations, Procurement
- Channels: Email, Phone, Self-Service Portal

### C015  (covers 8 tickets)
- Short description: System problem
- Description: hi, it says too many attempts, locked. pls unlock
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Email, Self-Service Portal

### C016  (covers 7 tickets)
- Short description: Locked out again. need it opened
- Description: locked out again. need it opened asap, have a client call at 11 let me know if you need anything from my side
- Departments: Human Resources, Marketing, Procurement, Sales
- Channels: Email, Self-Service Portal

### C017  (covers 7 tickets)
- Short description: Everything hangs when i open more
- Description: everything hangs when i open more than 2 things
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Email, Phone, Self-Service Portal

### C018  (covers 7 tickets)
- Short description: IT issue
- Description: got a mail asking for my details, looks fake, forwarding it this is blocking my work
- Departments: Human Resources, Legal, Manufacturing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C019  (covers 7 tickets)
- Short description: Not working
- Description: battery drains in one hour, was fine before this is blocking my work
- Departments: Finance, Human Resources, Marketing, Operations
- Channels: Email, Self-Service Portal

### C020  (covers 7 tickets)
- Short description: Someone claiming to be the director
- Description: second time reporting this, someone claiming to be the director asked me for gift cards appreciate a quick fix
- Departments: Customer Success, Engineering, Operations, Procurement
- Channels: Chat, Email, Phone, Self-Service Portal

### C021  (covers 7 tickets)
- Short description: Cannot book a room in the
- Description: cannot book a room in the invite, option is greyed out kindly look into it urgently
- Departments: Customer Success, Finance, Marketing, Operations
- Channels: Email, Phone, Self-Service Portal

### C022  (covers 7 tickets)
- Short description: Urgent help needed
- Description: raising this again, connection is unstable since the new client version this is blocking my work
- Departments: Engineering, Finance, Human Resources, Marketing
- Channels: Email, Phone, Self-Service Portal

### C023  (covers 7 tickets)
- Short description: It says my subscription has ended
- Description: hello, it says my subscription has ended, cannt open anything thanks in advance
- Departments: Engineering, Finance, Legal, Operations
- Channels: Chat, Email, Phone, Self-Service Portal

### C024  (covers 6 tickets)
- Short description: Changed my phone, now the 6
- Description: raising this again, changed my phone, now the 6 digit code app is empty
- Departments: Manufacturing, Marketing, Operations, Procurement
- Channels: Email, Phone, Self-Service Portal

### C025  (covers 6 tickets)
- Short description: Forgot the credentials after the holiday
- Description: forgot the credentials after the holiday, please help
- Departments: Finance, Human Resources, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C026  (covers 6 tickets)
- Short description: It just says connecting and stays
- Description: hi, it just says connecting and stays there forever
- Departments: Finance, Human Resources, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C027  (covers 6 tickets)
- Short description: Video freezes for others while my
- Description: raising this again, video freezes for others while my network looks fine this is blocking my work
- Departments: Finance, Human Resources, Legal, Marketing
- Channels: Email, Phone, Self-Service Portal

### C028  (covers 6 tickets)
- Short description: His last working day was 28th
- Description: good morning, his last workign day was 28th, still showing active in the sytem
- Departments: Engineering, Finance, Human Resources, Marketing
- Channels: Email, Phone, Self-Service Portal

### C029  (covers 6 tickets)
- Short description: Request
- Description: half the screen is flickering, lines coming thanks in advance
- Departments: Finance, Human Resources, Legal, Operations
- Channels: Email, Phone, Self-Service Portal

### C030  (covers 6 tickets)
- Short description: System problem
- Description: second time reporting this, nto receiving anything since morning but web version shows them this is blocking my work
- Departments: Customer Success, Legal, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C031  (covers 6 tickets)
- Short description: The pointer jumps on its own
- Description: team, the pointer jumps on its own while typing this is blocking my work
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Chat, Email, Self-Service Portal

### C032  (covers 6 tickets)
- Short description: Issue
- Description: system not accepting my details after i changed it last week
- Departments: Customer Success, Engineering, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C033  (covers 6 tickets)
- Short description: It asks for a certificate and
- Description: it asks for a certificate adn then fails to join
- Departments: Engineering, Finance, Human Resources, Legal
- Channels: Chat, Phone, Self-Service Portal

### C034  (covers 6 tickets)
- Short description: Cannot open the attachment, unsupported format
- Description: hi, cannt open the attachment, unsupported format error let me know if you need anything from my side
- Departments: Engineering, Human Resources, Legal, Operations
- Channels: Chat, Email, Phone, Self-Service Portal

### C035  (covers 6 tickets)
- Short description: The deck will not save, says
- Description: good morning, the deck will not save, says file is in use thanks in advance
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Email, Phone, Self-Service Portal

### C036  (covers 5 tickets)
- Short description: New handset given, need the work
- Description: second time reporting this, new handset given, need the work apps put on it
- Departments: Customer Success, Finance, Operations, Procurement
- Channels: Phone, Self-Service Portal

### C037  (covers 5 tickets)
- Short description: Not working
- Description: second time reporting this, lost my handset yesterday, cannot get the verification code please help
- Departments: Finance, Manufacturing, Operations
- Channels: Email, Phone, Self-Service Portal

### C038  (covers 5 tickets)
- Short description: Request
- Description: raising this again, need everything ready for the new resource starting next week thanks in advance
- Departments: Customer Success, Engineering, Finance, Manufacturing
- Channels: Chat, Email, Phone, Self-Service Portal

### C039  (covers 5 tickets)
- Short description: Mails are bouncing back to senders
- Description: second time reporting this, mails are bouncing back to senders, box seems full please help
- Departments: Finance, Procurement, Sales
- Channels: Email, Phone, Self-Service Portal

### C040  (covers 5 tickets)
- Short description: New device, the authenticator is not
- Description: new device, the authenticator is not showing anything for work this is blocking my work
- Departments: Engineering, Legal, Marketing, Procurement
- Channels: Email, Phone, Self-Service Portal

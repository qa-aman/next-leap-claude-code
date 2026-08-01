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
- Short description: File transfers to the server are
- Description: file transfers to the server are taking forever this week
- Departments: Finance, Human Resources, Manufacturing, Operations
- Channels: Email, Self-Service Portal

### C042  (covers 5 tickets)
- Short description: Paper stuck inside, tried removing but
- Description: second time reporting this, paper stuck inside, tried removing but still error thanks in advance
- Departments: Customer Success, Engineering, Finance, Operations
- Channels: Email, Phone, Self-Service Portal

### C043  (covers 5 tickets)
- Short description: I am still getting mails from
- Description: i am still getting mails from a team i left thanks in advance
- Departments: Customer Success, Engineering, Human Resources, Legal
- Channels: Email, Phone, Self-Service Portal

### C044  (covers 5 tickets)
- Short description: Need support
- Description: HELLO, PLEASE ADD THE TWO NEW JOINERS TO THE DELIVERY MAIL GROUP
- Departments: Engineering, Legal, Operations, Procurement
- Channels: Chat, Email, Self-Service Portal

### C045  (covers 5 tickets)
- Short description: Few keys not typing, mainly e
- Description: team, few keys not typing, mainly e and r
- Departments: Customer Success, Manufacturing, Marketing, Operations
- Channels: Email, Self-Service Portal

### C046  (covers 5 tickets)
- Short description: Strange link in a mail from
- Description: strange link in a mail from an unknown sender, did not click please help
- Departments: Finance, Legal, Operations
- Channels: Chat, Email, Phone, Self-Service Portal

### C047  (covers 5 tickets)
- Short description: Issue
- Description: the entry is nto going through, gives an error number this is blocking my work
- Departments: Customer Success, Finance, Marketing, Procurement
- Channels: Chat, Email, Phone, Self-Service Portal

### C048  (covers 5 tickets)
- Short description: The file closes by itself every
- Description: hi, the file closes by itself every time i open the big sheet thanks in advance
- Departments: Customer Success, Human Resources, Manufacturing, Operations
- Channels: Email, Self-Service Portal

### C049  (covers 5 tickets)
- Short description: My laptop does not see the
- Description: hi team, my laptop does not see the office network at all let me know if you need anything from my side
- Departments: Customer Success, Human Resources, Legal, Marketing
- Channels: Phone, Self-Service Portal

### C050  (covers 4 tickets)
- Short description: Issue
- Description: TEAM, PHONE IS NTO SYNCING ANYTHING FROM OFFICE APPRECIATE A QUICK FIX
- Departments: Engineering, Human Resources, Marketing, Sales
- Channels: Self-Service Portal

### C051  (covers 4 tickets)
- Short description: Moved desks and now there is
- Description: moved desks and now there is no connection through the cable let me know if you need anything from my side
- Departments: Legal, Manufacturing, Operations
- Channels: Chat, Email, Self-Service Portal

### C052  (covers 4 tickets)
- Short description: The adapter is warm but percentage
- Description: raising this again, the adapter is warm but percentage keeps going down thanks in advance
- Departments: Customer Success, Legal, Manufacturing, Marketing
- Channels: Chat, Email, Phone

### C053  (covers 4 tickets)
- Short description: Need support
- Description: my machine is behaving oddly after i opened an attachment let me know if you need anything from my side
- Departments: Engineering, Finance, Human Resources, Legal
- Channels: Email, Phone, Self-Service Portal

### C054  (covers 4 tickets)
- Short description: IT issue
- Description: hi team, the invite link says organiser has not started, but he has
- Departments: Marketing, Operations, Procurement, Sales
- Channels: Phone, Self-Service Portal

### C055  (covers 4 tickets)
- Short description: The team site says access denied
- Description: hi team, the team site says access denied after the migration kindly look into it urgently
- Departments: Finance, Legal, Manufacturing, Procurement
- Channels: Chat, Email, Self-Service Portal

### C056  (covers 4 tickets)
- Short description: Voice breaks badly in every call
- Description: team, voice breaks badly in every call from my end
- Departments: Customer Success, Finance, Human Resources
- Channels: Chat, Email, Phone, Self-Service Portal

### C057  (covers 4 tickets)
- Short description: Need support
- Description: wireless mouse disconnects every few minutes kindly look into it urgently
- Departments: Legal, Procurement, Sales
- Channels: Email, Self-Service Portal

### C058  (covers 4 tickets)
- Short description: Formatting breaks when i reopen the
- Description: hello, formatting breaks when i reopen the document kindly look into it urgently
- Departments: Human Resources, Legal, Procurement
- Channels: Email, Self-Service Portal

### C059  (covers 4 tickets)
- Short description: Issue
- Description: hello, machine takes 15 mins to start, unusable in teh mornign appreciate a quick fix
- Departments: Engineering, Legal, Manufacturing, Marketing
- Channels: Email, Phone, Self-Service Portal

### C060  (covers 4 tickets)
- Short description: Need support
- Description: cannot get into the module since the weekend patch appreciate a quick fix
- Departments: Customer Success, Finance, Manufacturing, Sales
- Channels: Chat, Email, Self-Service Portal

### C061  (covers 3 tickets)
- Short description: The tool logged me out saying
- Description: team, the tool logged me out saying no seat available let me know if you need anything from my side
- Departments: Customer Success, Legal
- Channels: Email, Self-Service Portal

### C062  (covers 3 tickets)
- Short description: Signal is very poor near the
- Description: signal is very poor near the east side meeting rooms
- Departments: Engineering, Finance, Human Resources
- Channels: Chat, Self-Service Portal

### C063  (covers 3 tickets)
- Short description: Pages coming with lines across, toner
- Description: good morning, pages coming with lines across, toner maybe kindly look into it urgently
- Departments: Procurement, Sales
- Channels: Self-Service Portal

### C064  (covers 3 tickets)
- Short description: System problem
- Description: TEAM, DATA FROM THE MARKETING TOOL IS NOT FLOWING IN NEED THIS TODAY
- Departments: Customer Success, Operations, Procurement
- Channels: Self-Service Portal

### C065  (covers 3 tickets)
- Short description: System problem
- Description: hello, dashboard is blank for me but fine for my manager thanks in advance
- Departments: Manufacturing, Marketing, Procurement
- Channels: Email, Phone, Self-Service Portal

### C066  (covers 3 tickets)
- Short description: Cannot open the team folder, says
- Description: hi team, cannt open the team folder, says you do not have permission
- Departments: Marketing, Operations
- Channels: Email, Phone, Self-Service Portal

### C067  (covers 3 tickets)
- Short description: Issue
- Description: nothing prints, jobs just sit in the queue kindly look into it urgently
- Departments: Human Resources, Manufacturing, Sales
- Channels: Email, Phone, Self-Service Portal

### C068  (covers 3 tickets)
- Short description: Urgent help needed
- Description: team, internal portal gives a certificate warning every time
- Departments: Engineering, Finance
- Channels: Chat, Phone, Self-Service Portal

### C069  (covers 3 tickets)
- Short description: Request
- Description: second time reporting this, not charging even when plugged in, shows 4% thanks in advance
- Departments: Customer Success, Finance, Sales
- Channels: Chat, Phone, Self-Service Portal

### C070  (covers 3 tickets)
- Short description: The page loads blank, works on
- Description: the page loads blank, works on my colleague machine
- Departments: Customer Success, Human Resources, Procurement
- Channels: Phone, Self-Service Portal

### C071  (covers 3 tickets)
- Short description: The pipeline view spins forever and
- Description: second time reporting this, the pipeline view spins forever and never loads
- Departments: Human Resources, Marketing, Operations
- Channels: Email, Self-Service Portal

### C072  (covers 3 tickets)
- Short description: Cafeteria area has almost no connectivity
- Description: hi team, cafeteria area has almost no connectivity thanks in advance
- Departments: Marketing, Operations
- Channels: Chat, Self-Service Portal

### C073  (covers 3 tickets)
- Short description: Promoted last month but still seeing
- Description: hi, promoted last month but still seeing the old menu options need this today
- Departments: Finance, Human Resources
- Channels: Self-Service Portal

### C074  (covers 3 tickets)
- Short description: New person joining monday in my
- Description: hello, new person joining monday in my team, nothing is set up for her yet need this today
- Departments: Human Resources, Manufacturing, Sales
- Channels: Email, Self-Service Portal

### C075  (covers 3 tickets)
- Short description: It says session could not be
- Description: team, it says session could not be created, others are fine
- Departments: Operations, Sales
- Channels: Email, Self-Service Portal

### C076  (covers 3 tickets)
- Short description: Need support
- Description: need to see the shared inbox that priya uses
- Departments: Engineering, Finance, Marketing
- Channels: Email, Self-Service Portal

### C077  (covers 3 tickets)
- Short description: Mic is picking up too much
- Description: hi, mic is picking up too much noise, team complained need this today
- Departments: Finance, Human Resources, Operations
- Channels: Email, Phone, Self-Service Portal

### C078  (covers 3 tickets)
- Short description: Keeps saying not responding when i
- Description: second time reporting this, keeps saying not responding when i refresh the pivot
- Departments: Legal, Marketing
- Channels: Self-Service Portal

### C079  (covers 3 tickets)
- Short description: IT issue
- Description: auditors are asking for the list of who has access to the finance app
- Departments: Engineering, Finance, Operations
- Channels: Phone, Self-Service Portal

### C080  (covers 3 tickets)
- Short description: Very slow since last week, fan
- Description: hi team, very slow since last week, fan runs loud all teh time let me know if you need anything from my side
- Departments: Finance, Manufacturing, Procurement
- Channels: Chat, Self-Service Portal

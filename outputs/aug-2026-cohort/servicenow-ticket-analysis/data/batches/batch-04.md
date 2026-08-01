# Classification batch 4 of 4

Assign every case below to exactly one path from the allowed list.
Return one JSON object per line: {"case_id":"C001","path":"L1 > L2 > L3","confidence":"High|Medium|Low","reason":"one short line"}

Rules:
1. The path must match the allowed list character for character.
2. If no path fits, use path `UNCATEGORIZED` and confidence `Low`.
3. Confidence Low means a human must review it. Do not force a fit.
4. Judge only from what the user wrote. Do not assume a team or a system that is not mentioned.

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

### C121  (covers 1 ticket)
- Short description: It says session could not be
- Description: IT SAYS SESSION COULD NOT BE CREATED, OTHERS ARE FINE PLZ HELP
- Departments: Human Resources
- Channels: Email

### C122  (covers 1 ticket)
- Short description: Urgent help needed
- Description: hi team, it keeps asking me for the code again and again in a loop
- Departments: Marketing
- Channels: Self-Service Portal

### C123  (covers 1 ticket)
- Short description: It asks for a certificate and
- Description: it asks for a certificate adn then fails to join plz help
- Departments: Operations
- Channels: Self-Service Portal

### C124  (covers 1 ticket)
- Short description: I can see the dashboard but
- Description: i can see the dashboard but cannot download anything this is blocking my work
- Departments: Procurement
- Channels: Phone

### C125  (covers 1 ticket)
- Short description: Urgent help needed
- Description: good morning, teh finance system is throwing an error at login for me only appreciate a quick fix
- Departments: Engineering
- Channels: Self-Service Portal

### C126  (covers 1 ticket)
- Short description: New person joining monday in my
- Description: hi team, new person joining monday in my team, nothing is set up for her yet
- Departments: Human Resources
- Channels: Email

### C127  (covers 1 ticket)
- Short description: Urgent help needed
- Description: the invite link says organiser has not started, but he has need this today
- Departments: Manufacturing
- Channels: Phone

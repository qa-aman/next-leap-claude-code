# Classification batch 4 of 4

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

### C121  (covers 1 ticket)
- Short description: Phone is not syncing anything from
- Description: HELLO, PHONE IS NOT SYNCING ANYTHING FROM OFFICE
- Departments: Marketing
- Channels: Chat

### C122  (covers 1 ticket)
- Short description: Please add the two new joiners
- Description: team, plz add teh two new joiners to the delivery mail group plz help
- Departments: Manufacturing
- Channels: Self-Service Portal

### C123  (covers 1 ticket)
- Short description: Please assist
- Description: raising this again, please give me approval rights for the requests queue
- Departments: Human Resources
- Channels: Chat

### C124  (covers 1 ticket)
- Short description: My machine is behaving oddly after
- Description: hi team, my machine is behaving oddly after i opened an attachment
- Departments: Human Resources
- Channels: Self-Service Portal

### C125  (covers 1 ticket)
- Short description: Not working
- Description: good morning, expired without any mail to me, now i cant work plz help
- Departments: Sales
- Channels: Chat

### C126  (covers 1 ticket)
- Short description: Display goes black randomly then comes
- Description: second time reporting this, display goes black randomly then comes back need this today
- Departments: Manufacturing
- Channels: Email

### C127  (covers 1 ticket)
- Short description: Wireless mouse disconnects every few minutes
- Description: wireless mouse disconnects every few minutes please help
- Departments: Operations
- Channels: Self-Service Portal

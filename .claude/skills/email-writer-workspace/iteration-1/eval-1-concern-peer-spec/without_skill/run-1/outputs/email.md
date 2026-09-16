Subject: Two gaps in the SSO spec before sprint starts

Hi Tomas,

I went through the Enterprise tier SSO spec today and wanted to flag two things before the sprint kicks off on 17-03-2026, since dev will need answers to build against.

1. Failed login UX isn't defined. The spec doesn't say what the user sees if SSO login fails, for example a wrong IdP configuration or an expired certificate. Right now there's no error state for either case, so a user could just hit a dead end.

2. Audit log retention period isn't specified anywhere in the spec. I know the compliance pilot asked for 12 months, so it would help to confirm that's the number we're building to, or flag if it's still open.

Happy to help think through either of these if useful. Let me know what you think.

Best,
Aman

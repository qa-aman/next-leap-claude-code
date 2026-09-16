Subject: ACTION: Two gaps in the SSO spec before sprint starts today

Hi Tomas,

I read through the Enterprise SSO spec today and found two gaps worth closing before the team picks it up this sprint.

Why it matters: without these, dev and QA will each build to a different assumption, and the compliance pilot's ask may not get met in time.

1. Login failure state. The spec does not say what the user sees when SSO login fails, a wrong IdP config or an expired cert. If we add this now, engineering builds it once instead of improvising it mid-sprint.
2. Audit log retention. The retention period is not defined anywhere, and the compliance pilot asked for 12 months. If we put that number in the spec, it closes the one thing the pilot is waiting on.

Could we get both added before engineering starts building this week? Happy to help draft either section if that is useful. Let me know if I have read either of these wrong.

---

Conversation type: Practical (a decision/plan gap to close, not an emotional or social exchange).
Module loaded: `references/module-concern.md` (raising a concern to a peer who owns the spec).
Assumption: [no specific response deadline was given, so I framed the ask as "before engineering starts building this week" rather than a hard date].

# Account setup (Phase 1)

Four online accounts, in this order, plus a second Supabase project for testing (Step 5). The Google step needs an address from the Supabase step. It takes about 50 minutes.

Button names may differ slightly from what's written here, since these sites change their layouts. If you can't find something, note what you see and ask.

## Keeping keys safe

Several steps give you a secret key. Save each one in a password manager or a private note on your Mac. **Never paste keys into the Claude chat**, email or Slack.

By the end you'll have saved these:

| # | Name | Secret? | From step |
|---|---|---|---|
| 1 | Anthropic API key | **Yes** | 1 |
| 2 | workers.dev subdomain | No | 2 |
| 3 | Supabase database password | **Yes** | 3 |
| 4 | Supabase Project URL | No | 3 |
| 5 | Supabase secret key | **Yes** | 3 |
| 6 | Google Client ID | No | 4 |
| 7 | Google Client secret | **Yes** | 4 |
| 8 | Test Supabase database password | **Yes** | 5 |
| 9 | Test Supabase Project URL | No | 5 |
| 10 | Test Supabase secret key | **Yes** | 5 |

---

## Step 1: Anthropic (the Claude API, which reads the meeting notes)

- [ ] 1. Go to **console.anthropic.com** and sign up.
- [ ] 2. Open **Billing** and add **$10** of credit. That should last well over a month at our expected usage.
- [ ] 3. Open **Settings → Limits** and set a **monthly spend limit of $15**. This is the safety cap from SPEC §7.
- [ ] 4. Open **API Keys → Create Key** and name it `action-items-app`.
- [ ] 5. Copy the key right away (it's only shown once) and save it as **"Anthropic API key"**.

## Step 2: Cloudflare (hosts the website)

- [ ] 1. Go to **dash.cloudflare.com/sign-up**, sign up, and confirm your email. The free plan doesn't need a card.
- [ ] 2. In the left menu, click **Workers & Pages**.
- [ ] 3. If it asks you to choose a **workers.dev subdomain**, pick something short, like `aman-team`. The app's address will end in `<your-subdomain>.workers.dev`.
- [ ] 4. Note the subdomain you picked.

## Step 3: Supabase (the database and login)

- [ ] 1. Go to **supabase.com**, click **Start your project**, and sign up with your email.
- [ ] 2. Click **New project** and fill in:
  - **Name:** `action-items`
  - **Database password:** click **Generate**, then save it as **"Supabase database password"**
  - **Region:** **South Asia (Mumbai)**
  - **Plan:** Free
- [ ] 3. Wait about 2 minutes while it sets up.
- [ ] 4. Open **Project Settings → API** (it may say **API Keys**) and save two things:
  - **Project URL**, which looks like `https://abcdxyz.supabase.co`. This one isn't secret.
  - The **secret key**, which may be labelled `service_role`. Save it as **"Supabase secret key"**. Don't use the key labelled `anon` or `publishable`.
- [ ] 5. Open **Authentication → Sign In / Providers → Google**. Copy the **Callback URL** shown there; you'll need it in Step 4. **Leave this browser tab open.**

## Step 4: Google sign-in (lets the team log in with Google)

- [ ] 1. Go to **console.cloud.google.com** and sign in with your Google account.
- [ ] 2. At the top, click the project picker, then **New project**. Name it `action-items`, click **Create**, then make sure it's selected.
- [ ] 3. In the search bar, type **Google Auth Platform**, open it, and click **Get started**:
  - **App name:** `Action Items`
  - **Support email:** your email
  - **Audience:** **External**
  - **Contact email:** your email
  - Agree to the terms, then click **Create**.
- [ ] 4. Go to **Audience → Test users → Add users** and add two accounts:
  - **Your own Gmail.** This will be the admin.
  - **A second Google account** that will *not* be on the team, such as a spare Gmail. It's needed for the Phase 1 check that outsiders are refused. It must be on this list, or Google blocks it before the app ever sees it.
- [ ] 5. Go to **Clients → Create client**:
  - **Type:** **Web application**
  - **Name:** `Action Items web`
  - Under **Authorized redirect URIs**, click **Add URI** and paste the **Callback URL** from Step 3.5.
  - Click **Create**. Save the **Client ID** and **Client secret**.
- [ ] 6. Go back to the Supabase tab. Turn **Google** on, paste the Client ID and Client secret, and click **Save**.

## Step 5: A second Supabase project, for automated tests only

The app's automated tests create and delete test data, so they get their own empty database and never touch the real one. It's free: the free plan allows 2 projects.

- [ ] 1. Go to **supabase.com** and open your dashboard. You're already signed in from Step 3.
- [ ] 2. Click **New project** and fill in:
  - **Name:** `action-items-test`
  - **Database password:** click **Generate**, then save it as **"Test Supabase database password"**
  - **Region:** **South Asia (Mumbai)**
  - **Plan:** Free
- [ ] 3. Wait about 2 minutes while it sets up.
- [ ] 4. Open **Project Settings → API** (it may say **API Keys**) and save:
  - **Project URL**, saved as **"Test Supabase Project URL"**
  - The **secret key** (may be labelled `service_role`), saved as **"Test Supabase secret key"**
- [ ] 5. That's all. This project doesn't need Google sign-in.

**Don't mix them up:** the real project is `action-items`, the test one is `action-items-test`. Check the project name at the top left of the Supabase page before copying anything.

---

## When you're done

Send Claude (**no keys**):
- ✅ or ❌ for each of the 5 steps, and where you got stuck if anywhere
- Your **workers.dev subdomain**
- Your **Supabase Project URL** (the real one) and your **Test Supabase Project URL**

The next part of Phase 1 is the code: empty app, database tables, sign-in, team list page, and the 2-minute Claude call check. The keys go into a private settings file on your Mac at that point, and Claude will give you exact steps for it.

## Later: when the company Google Workspace is ready

Until then, the allowed domain is temporarily `gmail.com`, with only Aman's Gmail on the team list (see SPEC §10). Once the Workspace exists:

- [ ] 1. In **Google Auth Platform → Audience**, switch the app from **External** to **Internal**.
- [ ] 2. Tell Claude the company domain, so the allowed domain can be switched from `gmail.com` to it.
- [ ] 3. Send Claude the 8 team emails for the team list.

# Customer transition — announcement email sequence (DRAFT)

> **NOT PUBLISHED — INTERNAL DRAFT.** This file is copy for review under SW-317.
> It is **not** a customer-facing KB page and is intentionally **not** listed in
> `SUMMARY.md`. Do not send until Graham signs off on the transition date and the
> decisions in the SW-317 Linear thread (pre-provision vs. self-signup,
> read-only window). Placeholders in `{{ }}` are filled at send time.
>
> - **spec:** SW-317 (promote to REQ-ID at implementation)
> - **exit-impact:** revenue (retention through the platform transition)
> - Landing page for all three emails: **[Switching to the new OcuTrap app](../README.md)** → publishes at `app.ocutrap.com/docs/switching-to-the-new-app` (final URL confirmed at cutover, coordinates with SW-143 / SW-314).

A three-touch sequence. Touch 1 sets expectations, Touch 2 is the call to action, Touch 3 is the deadline nudge. Send only to customers with traps/subscriptions parked under a known email (the audience the trap re-link depends on).

---

## Touch 1 — Announce (T‑minus ~2 weeks)

**Subject:** The new OcuTrap app is here — here's what it means for you

**Preheader:** Same traps, same subscription, a much better app. A quick heads-up before you switch.

Hi {{ first_name }},

We've rebuilt the OcuTrap app from the ground up — faster, clearer, and made for the field. In the next couple of weeks we'll invite you to move over to it at **app.ocutrap.com**.

Here's the short version:

- **Your traps, images, and subscription all come with you.** Nothing to re-register, no data lost.
- **You'll create a new login** using **the same email you use today** — that's how we reconnect your traps. (For your security, passwords can't be carried over, so you'll set a fresh one.)
- **Nothing breaks today.** Your current app keeps working until you're ready to switch. We'll tell you exactly when and how.

Want a preview of what's changed? Read **[What's new](../whats-new.md)**.

We'll be in touch soon with your move link. Questions in the meantime? Just reply to this email.

— The OcuTrap Team

---

## Touch 2 — Action needed (T‑zero, move window opens)

**Subject:** Action needed: set up your new OcuTrap account

**Preheader:** It takes about two minutes. Use the same email and your traps are waiting.

Hi {{ first_name }},

Your new OcuTrap app is ready. Here's how to move over — it takes about two minutes:

1. **Go to [app.ocutrap.com]({{ signup_url }}) and sign up.** Use **{{ customer_email }}** — the same email your traps are under.
2. **Verify your email** when prompted.
3. **Check your traps.** They'll appear automatically, with your images and history.
4. **Check your billing.** Open a trap's Billing page and your account Billing to confirm your plan carried over.

Full walkthrough: **[Switching to the new OcuTrap app]({{ transition_guide_url }})**.

{{ #if read_only_window }}
Your current app ({{ legacy_url }}) will stay available in **read-only** mode until **{{ read_only_end_date }}**, so you can look back at anything you need.
{{ /if }}

Run into anything — a missing trap, a billing question — just reply or [contact support]({{ support_url }}). Don't start a new subscription; we'll reconnect whatever needs it.

— The OcuTrap Team

---

## Touch 3 — Last call (T‑plus, a few days before read-only ends)

**Subject:** Last call: move your OcuTrap account by {{ cutover_date }}

**Preheader:** A couple of minutes now keeps your traps and history at your fingertips.

Hi {{ first_name }},

Quick reminder — you haven't set up your new OcuTrap account yet. To keep managing your traps, please move over before **{{ cutover_date }}**:

1. Go to **[app.ocutrap.com]({{ signup_url }})** and sign up with **{{ customer_email }}**.
2. Verify your email — your traps and subscription reconnect automatically.

It takes about two minutes: **[Start here]({{ transition_guide_url }})**.

{{ #if read_only_window }}
After **{{ read_only_end_date }}**, the old app closes and **{{ legacy_url }}** will bring you to the new app. Your account and data are safe — you'll just sign in at the new address.
{{ /if }}

Need help or prefer we set it up with you? [Contact support]({{ support_url }}) — we're glad to help.

— The OcuTrap Team

---

## Send notes (internal)

- **Audience gate:** only customers whose traps/shares are parked under a known email (`pendingOwnerEmail` / `trapShares.inviteEmail`) will auto-reconnect on signup. Confirm the send list against that data before Touch 2.
- **Placeholder wiring:** `{{ read_only_window }}` conditional and `{{ read_only_end_date }}` depend on Graham's read-only-window decision (SW-317). If the decision is "no read-only window," drop those blocks.
- **Pre-provision variant:** if Graham chooses to pre-provision accounts in WorkOS (see SW-317 decision list), Touch 2 changes from "sign up" to "set your password" — a second copy variant is needed. This draft assumes **fresh self-signup**.
- **Deliverability:** send from the transactional domain used for OcuTrap notifications; suppress addresses that already have a new-app account.

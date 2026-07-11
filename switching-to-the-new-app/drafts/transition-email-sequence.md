# Customer transition — announcement email sequence (DRAFT)

> **NOT PUBLISHED — INTERNAL DRAFT, SUPERSEDED FOR SEND COPY.** This file is early
> review copy under SW-317. It is **not** a customer-facing KB page and is
> intentionally **not** listed in `SUMMARY.md`.
>
> **The authoritative send copy now lives in internal-docs** —
> `cutover/2026-07-cutover-email-sequence.md` (CUT-05). Use that for the actual
> blast; this file is kept only as the guide-side reference and has been aligned to
> the same decisions so it doesn't contradict the product.
>
> **Decisions landed 2026-07-10 (CUT-D1..D5):** accounts are **pre-provisioned** in
> WorkOS (no self-signup) and customers **set a password** from a link; the old app
> **retires** (it has no read-only mode) then redirects to the new app. The two
> open questions this draft was gated on — pre-provision vs. self-signup, and the
> read-only window — are therefore **resolved** (pre-provision; no read-only mode).
> Placeholders in `{{ }}` are filled at send time.
>
> - **spec:** SW-317 → CUT-05 (canonical email copy in internal-docs)
> - **exit-impact:** revenue (retention through the platform transition)
> - Landing page for all emails: **[Switching to the new OcuTrap app](../README.md)** → publishes at `app.ocutrap.com/docs/switching-to-the-new-app` (final URL confirmed at cutover, coordinates with SW-143 / SW-314).

A three-touch sequence. Touch 1 sets expectations, Touch 2 is the call to action, Touch 3 is the deadline nudge. Send only to customers with traps/subscriptions parked under a known email (the audience the trap re-link depends on).

---

## Touch 1 — Announce (T‑minus ~2 weeks)

**Subject:** The new OcuTrap app is here — here's what it means for you

**Preheader:** Same traps, same subscription, a much better app. A quick heads-up before you switch.

Hi {{ first_name }},

We've rebuilt the OcuTrap app from the ground up — faster, clearer, and made for the field. In the next couple of weeks we'll invite you to move over to it at **app.ocutrap.com**.

Here's the short version:

- **Your traps, images, and subscription all come with you.** Nothing to re-register, no data lost.
- **Your account is already set up** under **the same email you use today** — when it's your turn, you'll just set a password from a link we send. (For your security, passwords can't be carried over from the old app.)
- **Nothing breaks today.** Your current app keeps working until you're ready to switch. We'll tell you exactly when and how.

Want a preview of what's changed? Read **[What's new](../whats-new.md)**.

We'll be in touch soon with your move link. Questions in the meantime? Just reply to this email.

— The OcuTrap Team

---

## Touch 2 — Action needed (T‑zero, move window opens)

**Subject:** Your new OcuTrap account is ready — just set your password

**Preheader:** It takes about a minute. Your account is set up and your traps are waiting.

Hi {{ first_name }},

Your new OcuTrap app is ready, and **your account is already set up** — your traps, images, shared access, and subscription are all waiting. One step:

1. **[Set your password]({{ set_password_url }})** — the account is under **{{ customer_email }}**, the same email your traps are on. *(Fresh link — minted per send.)*
2. **Sign in** at **[app.ocutrap.com]({{ app_url }})** (or the mobile app) with that email and your new password.
3. **Check your traps.** They're already connected, with your images and history.
4. **Check your billing.** Open a trap's Billing page and your account Billing to confirm your plan carried over.

Full walkthrough: **[Switching to the new OcuTrap app]({{ transition_guide_url }})**.

Your current app ({{ legacy_url }}) stays available until **{{ retire_date }}**, when it retires and sends you to the new app.

Run into anything — a missing trap, a billing question — just reply or [contact support]({{ support_url }}). Don't start a new subscription; we'll reconnect whatever needs it.

— The OcuTrap Team

---

## Touch 3 — Last call (T‑plus, a few days before read-only ends)

**Subject:** Last call: move your OcuTrap account by {{ retire_date }}

**Preheader:** A couple of minutes now keeps your traps and history at your fingertips.

Hi {{ first_name }},

Quick reminder — you haven't set your new OcuTrap password yet. Your account is ready and your traps are waiting. To keep managing them, please move over before **{{ retire_date }}**:

1. **[Set your password]({{ set_password_url }})** — your account is under **{{ customer_email }}**. *(Fresh link.)*
2. Sign in at **[app.ocutrap.com]({{ app_url }})** — your traps and subscription are already connected.

It takes about a minute: **[Start here]({{ transition_guide_url }})**.

After **{{ retire_date }}**, the old app retires and **{{ legacy_url }}** will bring you to the new app. Your account and data are safe — you'll just sign in at the new address.

Need help or prefer we set it up with you? [Contact support]({{ support_url }}) — we're glad to help.

— The OcuTrap Team

---

## Send notes (internal)

- **Canonical copy:** the actual send copy is `internal-docs/cutover/2026-07-cutover-email-sequence.md` (CUT-05, five emails + banner). This file is guide-side reference only — keep it aligned, don't diverge.
- **Audience gate:** only customers whose traps/shares are parked under a known email (`pendingOwnerEmail` / `trapShares.inviteEmail`) reconnect on claim. Confirm the send list against that data before Touch 2. Sends are segmented claimed vs. not-yet-claimed (SW-183) — Touch 3 goes only to non-claimers.
- **Set-password links:** `{{ set_password_url }}` is a WorkOS set-password/reset link and **expires** — mint a **fresh** link per user per send, never reuse a prior email's link.
- **Retire, not read-only:** Bubble has no view-only mode; after the DNS flip it retires and redirects. Copy says "retires"/"shuts down", never "read-only". `{{ retire_date }}` is the CUT-D4 retire date (gate-conditioned).
- **Deliverability:** send from the transactional domain used for OcuTrap notifications (SW-145); suppress addresses that already claimed a new-app account.

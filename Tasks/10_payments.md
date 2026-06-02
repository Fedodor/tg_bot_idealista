# 10 — Payments

**Epic 9 · Milestone 3**

Stripe integration, subscription plans, webhooks, and plan enforcement.

> ⚠️ **Do not start this epic before Milestone 2 is complete and demand is validated.**
> Manual payment collection (Stripe link, Revolut, PayPal) is acceptable for the first beta.

---

## Priority

`P4 — Low`

Payments are not an MVP blocker. The product must prove value first.
Start this only after ≥5 users say alerts are useful and ≥1 person pays manually.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Manual Payment Bridge (Beta Only)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 10.1 | Create a Stripe Payment Link for Hunt Pass (€9–19 / 7 days) | P3 | ⬜ |
| 10.2 | Manually upgrade `users.plan` to `beta` after confirming payment | P3 | ⬜ |
| 10.3 | Add admin CLI command: `grant-plan <telegram_id> <plan> <days>` | P3 | ⬜ |

---

### Database — Stripe Tables

| # | Task | Priority | Status |
|---|------|----------|--------|
| 10.4 | Add `stripe_customers` table: `user_id`, `stripe_customer_id`, `created_at` | P4 | ⬜ |
| 10.5 | Add `subscriptions` table: `user_id`, `plan`, `started_at`, `expires_at`, `stripe_subscription_id` | P4 | ⬜ |
| 10.6 | Add Alembic migration for payment tables | P4 | ⬜ |

---

### Stripe Integration

| # | Task | Priority | Status |
|---|------|----------|--------|
| 10.7 | Add `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` to config | P4 | ⬜ |
| 10.8 | Create Stripe Checkout session on bot command `/buy` | P4 | ⬜ |
| 10.9 | Implement webhook handler for `checkout.session.completed` | P4 | ⬜ |
| 10.10 | Implement webhook handler for `customer.subscription.deleted` | P4 | ⬜ |
| 10.11 | Set `users.plan` based on active subscription status | P4 | ⬜ |

---

### Plan Enforcement

| # | Task | Priority | Status |
|---|------|----------|--------|
| 10.12 | Free plan: daily digest only, 1 search, limited AI explanation | P4 | ⬜ |
| 10.13 | Hunt Pass (beta): instant alerts, AI red flags, EN/RU summaries, questions | P4 | ⬜ |
| 10.14 | Pro plan: multiple searches, priority alerts, saved listings, advanced filters | P4 | ⬜ |
| 10.15 | Check `users.plan` before sending instant alert vs queuing digest | P4 | ⬜ |
| 10.16 | Check plan expiration — downgrade to free if expired | P4 | ⬜ |

---

### Bot Commands for Payments

| # | Task | Priority | Status |
|---|------|----------|--------|
| 10.17 | `/buy` — show plan options with pricing | P4 | ⬜ |
| 10.18 | `/my_plan` — show current plan and expiry date | P4 | ⬜ |
| 10.19 | Notify user 1 day before plan expires | P4 | ⬜ |

---

## Plan Pricing Reference

| Plan | Price | Key Features |
|------|-------|-------------|
| **Free** | €0 | Daily digest, 1 search, Barcelona, limited AI |
| **Hunt Pass** | €9–19 / 7 days | Instant alerts, AI red flags, EN/RU summaries |
| **Pro** | €7–12 / month | Multiple searches, priority alerts, saved listings |

---

## Definition of Done

```text
✅ Manual plan grant command works in admin CLI
✅ Stripe checkout session creates successfully
✅ Webhook correctly upgrades/downgrades user plan
✅ Instant alerts only sent to paid users
✅ Free users receive daily digest
✅ /my_plan shows correct status
✅ Plan expiry enforced automatically
```

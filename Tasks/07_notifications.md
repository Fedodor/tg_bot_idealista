# 07 — Notifications

**Epic 7 · Milestone 1–2 · Day 5**

Telegram alert delivery, duplicate prevention, feedback buttons, and daily digest.

---

## Priority

`P2 — High`

Notifications are the product's output — what users actually see and interact with.
Must work for Milestone 1 (manual import), improves with AI data in Milestone 2.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Notification Service (Day 5)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.1 | Create `app/services/notifications.py` | P1 | ⬜ |
| 7.2 | Implement `send_listing_alert(user_id, match)` function | P1 | ⬜ |
| 7.3 | Format alert message per the template in §8.2 of the plan | P1 | ⬜ |
| 7.4 | Include: price, type, area, match score, risk level, why it matches | P1 | ⬜ |
| 7.5 | Include AI summary and red flags if `listing_analysis` available | P2 | ⬜ |
| 7.6 | Include `questions_to_ask` if available from AI | P2 | ⬜ |
| 7.7 | Include `[Open listing]` link button to original URL | P1 | ⬜ |

---

### Alert Message Format

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.8 | Use emoji to improve readability: 🏠 🟢 🔴 ⚠️ | P2 | ⬜ |
| 7.9 | Show match score as `Match: 86/100` | P1 | ⬜ |
| 7.10 | Show risk level as `Risk: Low / Medium / High` | P1 | ⬜ |
| 7.11 | Show "Why it matches" bullet list from `reason_en` / `reason_ru` | P1 | ⬜ |
| 7.12 | Message respects user's selected language (EN/RU) | P1 | ⬜ |
| 7.13 | Message stays within Telegram 4096-char limit — truncate if needed | P2 | ⬜ |

---

### Feedback Buttons (Day 5)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.14 | Attach inline keyboard to each alert: `👍 Useful` · `👎 Not relevant` · `🚩 Suspicious` · `📩 Contacted` · `🙈 Hide similar` | P1 | ⬜ |
| 7.15 | Each button sends callback with `listing_id` and `feedback_type` | P1 | ⬜ |
| 7.16 | Feedback saved to `feedback` table via `handlers_feedback.py` | P1 | ⬜ |
| 7.17 | Bot replies with short confirmation on feedback press | P2 | ⬜ |

---

### Duplicate Notification Prevention (Day 5)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.18 | Check `notifications` table before sending — skip if already sent | P1 | ⬜ |
| 7.19 | Save Telegram `message_id` and `sent_at` to `notifications` table | P1 | ⬜ |
| 7.20 | Handle Telegram API errors (rate limits, blocked users) gracefully | P2 | ⬜ |
| 7.21 | Log failed sends and retry up to N times | P2 | ⬜ |

---

### Notification Worker

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.22 | Create `app/workers/notify_worker.py` | P1 | ⬜ |
| 7.23 | Poll `matches` where `should_notify = True` and no notification sent | P1 | ⬜ |
| 7.24 | Send alerts and mark notifications as sent | P1 | ⬜ |
| 7.25 | Run notify worker after analyze worker completes | P1 | ⬜ |

---

### Instant vs Daily Digest

| # | Task | Priority | Status |
|---|------|----------|--------|
| 7.26 | Instant alerts for `plan = beta` or `plan = pro` users | P2 | ⬜ |
| 7.27 | Daily digest (batch of top matches) for `plan = free` users | P3 | ⬜ |
| 7.28 | Schedule daily digest at configurable time (e.g. 08:00 local) | P3 | ⬜ |

---

## Alert Template Reference

```text
🏠 New rental match

€850 / month
Room in Eixample, Barcelona
Available now

Match: 86/100
Risk level: Low

Why it matches:
- within your budget
- central area
- furnished
- no obvious scam wording

Possible questions to ask:
- Is empadronamiento possible?
- Is the contract long-term or temporary?
- Are utilities included?

[Open listing] [👍 Useful] [👎 Not relevant] [🚩 Suspicious] [📩 Contacted] [🙈 Hide]
```

---

## Definition of Done

```text
✅ Alert sent for each new match with should_notify = True
✅ Message formatted correctly in EN and RU
✅ Feedback buttons attached and functional
✅ No duplicate alerts sent
✅ Notifications table populated after each send
✅ Failed sends logged and retried
```

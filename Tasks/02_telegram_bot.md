# 02 — Telegram Bot

**Epic 2 · Milestone 1 · Day 1–2**

Bot skeleton, language onboarding, search creation flow, and all user-facing commands.

---

## Priority

`P1 — Critical`

The bot is the only interface for MVP users. Must be working before beta launch.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Bot Skeleton (Day 1)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.1 | Create `app/bot/telegram_app.py` with aiogram Application setup | P1 | ✅ |
| 2.2 | Register all routers in main app entry point | P1 | ✅ |
| 2.3 | Bot starts cleanly with `/start` command recognized | P1 | ✅ |
| 2.4 | Add graceful shutdown handler | P2 | ✅ |

---

### Language Onboarding (Day 2)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.5 | Implement `/start` handler in `handlers_start.py` | P1 | ✅ |
| 2.6 | Show language selector: `[English]` / `[Русский]` inline buttons | P1 | ✅ |
| 2.7 | Save selected language to `users.language` in DB | P1 | ✅ |
| 2.8 | All subsequent bot messages respect language selection | P1 | ✅ |

---

### Search Creation Flow (Day 2)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.9 | Ask rental type: `[Apartment]` / `[Room]` / `[Both]` | P1 | ✅ |
| 2.10 | Ask city (Barcelona only for MVP) | P1 | ✅ |
| 2.11 | Ask budget: min / max price input | P1 | ✅ |
| 2.12 | Ask preferred areas (text input or multi-select) | P1 | ✅ |
| 2.13 | Ask must-have filters: furnished, empadronamiento, pet-friendly, no agency fee, long-term, near metro | P2 | ⬜ |
| 2.14 | Save completed search to `user_searches` table | P1 | ✅ |
| 2.15 | Confirm search created with summary message | P1 | ✅ |

---

### Search Management Commands (Day 2)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.16 | Implement `/my_search` — show active search summary | P1 | ✅ |
| 2.17 | Implement `/edit_search` — allow updating filters | P2 | ⬜ |
| 2.18 | Implement `/pause` — deactivate search without deleting | P2 | ⬜ |
| 2.19 | Implement `/delete_me` — delete all user data (GDPR) | P1 | ✅ |

---

### Keyboards & UI (Day 2)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.20 | Create reusable inline keyboards in `keyboards.py` | P1 | ✅ |
| 2.21 | Language selection keyboard | P1 | ✅ |
| 2.22 | Rental type keyboard | P1 | ✅ |
| 2.23 | Must-have filters multi-select keyboard | P2 | ⬜ |
| 2.24 | Feedback buttons keyboard (Useful / Not relevant / Suspicious / Contacted / Hide similar) | P1 | ✅ |

---

### Feedback Handlers

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.25 | Create `handlers_feedback.py` for callback button handlers | P1 | ✅ |
| 2.26 | Save feedback type to `feedback` table on button press | P1 | ✅ |
| 2.27 | Confirm feedback with short bot reply | P2 | ✅ |

---

### Localization

| # | Task | Priority | Status |
|---|------|----------|--------|
| 2.28 | Create simple string translation helper or constants file | P2 | ⬜ |
| 2.29 | All user-visible strings exist in both EN and RU | P2 | ⬜ |

---

## Definition of Done

```text
✅ /start launches language + onboarding flow
✅ User can create a search with all filters
✅ /my_search displays active search
✅ /delete_me removes user data from DB
✅ Feedback buttons are registered and save to DB
✅ All messages shown in selected language (EN/RU)
```

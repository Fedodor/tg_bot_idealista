# 09 — Privacy & Compliance

**Epic — Cross-cutting · Milestone 1**

GDPR compliance, privacy policy, data minimisation, and legal guardrails.
Must be addressed from the beginning — not treated as an afterthought.

---

## Priority

`P2 — High`

Cannot launch a real SaaS without these. Many items must be done before inviting beta users.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Legal Documents

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.1 | Write Privacy Policy (what data is collected, how it's used, how to delete) | P2 | ⬜ |
| 9.2 | Write Terms of Service (service scope, disclaimers, limitations) | P2 | ⬜ |
| 9.3 | Host documents publicly (GitHub Pages, Notion, or simple web page) | P2 | ⬜ |
| 9.4 | Link to Privacy Policy and ToS during onboarding `/start` flow | P2 | ⬜ |

---

### User Consent

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.5 | Store `consent_at` timestamp in `users` table when user accepts terms | P2 | ⬜ |
| 9.6 | User must explicitly accept before searches are created | P2 | ⬜ |
| 9.7 | Add inline button: `[I agree to Terms and Privacy Policy]` | P2 | ⬜ |

---

### Data Deletion

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.8 | Implement `/delete_me` command | P1 | ⬜ |
| 9.9 | `/delete_me` deletes: user row, all user_searches, all matches, all feedback, all notifications | P1 | ⬜ |
| 9.10 | Confirm deletion with final bot message before data is removed | P1 | ⬜ |
| 9.11 | Log deletion event (no personal data in log — just user_id + timestamp) | P2 | ⬜ |

---

### Data Minimisation

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.12 | Do not log message content (user messages must not appear in logs) | P1 | ⬜ |
| 9.13 | Do not store listing contact data (phone numbers, agent emails) in normalized fields | P2 | ⬜ |
| 9.14 | Strip phone numbers and emails from `listing_text` before sending to LLM | P1 | ⬜ |
| 9.15 | Do not store more listing data than required for matching and display | P2 | ⬜ |
| 9.16 | Review `raw_data` field — consider TTL or partial storage | P3 | ⬜ |

---

### AI Disclaimer

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.17 | Add disclaimer to every AI alert: "AI analysis is informational only, not legal advice" | P2 | ⬜ |
| 9.18 | Prompt instructs LLM: do not make legal conclusions | P1 | ⬜ |
| 9.19 | Prompt instructs LLM: do not score tenants, nationalities, or protected characteristics | P1 | ⬜ |

---

### Source Terms Tracking

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.20 | Create `source_terms_review.md` documenting terms for each source used | P2 | ⬜ |
| 9.21 | Record: access allowed, commercial use allowed, attribution required, rate limits | P2 | ⬜ |
| 9.22 | Review and update source terms log before adding any new source | P2 | ⬜ |

---

### Sensitive Product Boundaries

| # | Task | Priority | Status |
|---|------|----------|--------|
| 9.23 | Ensure no scoring of tenants, landlords, ethnicity, nationality, or creditworthiness | P1 | ⬜ |
| 9.24 | Score is applied to listings only — never to users | P1 | ⬜ |
| 9.25 | AI prompt review: remove any language that could score individuals indirectly | P1 | ⬜ |

---

## Definition of Done

```text
✅ Privacy Policy and ToS published and linked in /start
✅ User consent timestamp stored before creating searches
✅ /delete_me removes all user data
✅ No user message content in logs
✅ Phone/email stripped before LLM
✅ AI disclaimer in every alert
✅ Source terms documented in source_terms_review.md
✅ No tenant or personal attribute scoring anywhere
```

# Tasks — AI Housing Finder Spain (Relocation Rental Radar)

Task board following the [MVP Specification](../ai_housing_finder_spain_mvp_plan.md).

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | **Todo** — not started |
| 🔄 | **In Progress** — currently being worked on |
| ✅ | **Done** — completed and verified |

## Priority Legend

| Label | Meaning |
|-------|---------|
| `P1` | **Critical** — MVP blocker, must be done first |
| `P2` | **High** — needed for beta launch |
| `P3` | **Medium** — improves product quality |
| `P4` | **Low** — nice to have, can wait |

---

## Functional Areas

| File | Area | Milestone | Priority |
|------|------|-----------|----------|
| [01_foundation.md](./01_foundation.md) | Project setup & infrastructure | M1 | P1 |
| [02_telegram_bot.md](./02_telegram_bot.md) | Bot onboarding & commands | M1 | P1 |
| [03_data_sources.md](./03_data_sources.md) | Listing ingestion & source adapters | M2 | P1 |
| [04_listing_normalization.md](./04_listing_normalization.md) | Normalization & deduplication | M2 | P1 |
| [05_matching.md](./05_matching.md) | Filters, scoring & matching engine | M1–M2 | P1 |
| [06_ai_analysis.md](./06_ai_analysis.md) | Local LLM integration & prompts | M2 | P2 |
| [07_notifications.md](./07_notifications.md) | Telegram alerts & feedback | M1–M2 | P2 |
| [08_admin_operations.md](./08_admin_operations.md) | Admin CLI & monitoring | M2 | P2 |
| [09_privacy_compliance.md](./09_privacy_compliance.md) | Privacy, GDPR & legal | M1 | P2 |
| [10_payments.md](./10_payments.md) | Stripe & subscription logic | M3 | P4 |

---

## Milestones

| Milestone | Goal | Status |
|-----------|------|--------|
| **M1** | Technical Prototype — bot + DB + manual import + basic matching | ⬜ |
| **M2** | Automated Beta — automated ingestion + AI analysis + alerts | ⬜ |
| **M3** | Paid Validation — 10–20 users + first Hunt Pass payments | ⬜ |

---

## 7-Day Sprint Map

| Day | Focus | Task Files |
|-----|-------|------------|
| Day 1 | Repo, Docker, DB, models, bot skeleton | 01, 02 |
| Day 2 | Onboarding, search creation, filters | 02 |
| Day 3 | Manual import, normalization, dedup, admin CLI | 03, 04, 08 |
| Day 4 | Hard filters, scoring, matching | 05 |
| Day 5 | Telegram alerts, feedback, dedup notifications | 07 |
| Day 6 | Ollama, AI summary, red flags, JSON validation | 06 |
| Day 7 | Deploy, source monitoring, invite beta users | 08 |

# Agent Development Rules — Relocation Rental Radar

Rules for any AI coding agent working on this project.
Read this file fully before writing a single line of code.

---

## 1. Read Before You Act

Before starting any task:

1. Read [`ai_housing_finder_spain_mvp_plan.md`](./ai_housing_finder_spain_mvp_plan.md) — the full product specification.
2. Open the relevant file in [`Tasks/`](./Tasks/) for the area you are working on.
3. Identify the task status (`⬜ Todo`, `🔄 In Progress`, `✅ Done`) and priority (`P1`–`P4`).
4. Only work on tasks that are `⬜ Todo` unless explicitly instructed otherwise.
5. Update the task status to `🔄 In Progress` before writing code.
6. Mark the task `✅ Done` only after it has been implemented AND verified.

---

## 2. Task Priority Order

Always respect priority order. Do not start lower-priority tasks if higher-priority ones remain unfinished.

```text
P1 Critical  →  work on these first, they are MVP blockers
P2 High      →  needed for beta launch, start after P1 is done
P3 Medium    →  quality improvements, work on during spare cycles
P4 Low       →  do not touch until explicitly instructed
```

**Do not start Epic 9 (Payments / `10_payments.md`) until demand is validated.**

---

## 3. Architecture Rules

### 3.1 Follow the defined project structure

All new files must go into the correct module:

```text
app/
  main.py           — entry point only
  config.py         — config via Pydantic Settings + .env
  logging.py        — structured logging setup

  db/
    session.py      — SQLAlchemy async engine and session factory
    models.py       — all ORM models
    migrations/     — Alembic only

  bot/
    telegram_app.py       — aiogram Application, dispatcher, router registration
    handlers_start.py     — /start, onboarding, search creation
    handlers_filters.py   — filter editing handlers
    handlers_feedback.py  — feedback button callbacks
    keyboards.py          — all inline keyboards

  sources/
    base.py                   — abstract BaseSource interface
    normalized_listing.py     — NormalizedListing dataclass / Pydantic model
    manual_import.py          — CSV/JSON manual import
    user_submitted.py         — user-submitted listing URLs
    idealista_official_api.py — only if API access is approved
    rapidapi_idealista.py     — only if terms are acceptable

  services/
    matching.py        — hard filters + scoring
    scoring.py         — deterministic scoring rules
    ai_analysis.py     — Ollama LLM adapter
    notifications.py   — Telegram alert formatting and sending
    deduplication.py   — dedup hash logic
    translation.py     — EN/RU string helpers

  workers/
    ingest_worker.py   — polling loop for source adapters
    analyze_worker.py  — AI analysis queue
    notify_worker.py   — notification delivery

  admin/
    simple_cli.py      — admin CLI commands
```

### 3.2 Never mix concerns across layers

- `handlers_*.py` — only bot interaction, never business logic
- `services/` — business logic only, no Telegram imports
- `workers/` — orchestration only, delegate to services
- `models.py` — data models only, no logic

### 3.3 Source adapters must be interchangeable

Every source adapter:
- extends `BaseSource` from `sources/base.py`
- returns a list of `NormalizedListing` objects
- handles its own errors internally
- implements a `health_check()` method

Never call source-specific code outside of `sources/`.

---

## 4. Code Style Rules

### 4.1 Python

- Python 3.11+
- Use `async`/`await` throughout — synchronous DB or HTTP calls are not allowed
- Use `SQLAlchemy` async sessions (`AsyncSession`) only
- Use `Pydantic v2` for all data models and config
- Use type hints on all function signatures
- Use `dataclasses` or Pydantic models — never plain dicts for structured data

### 4.2 Naming

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- DB columns: `snake_case`

### 4.3 Error handling

- All external calls (HTTP, DB, Telegram) must be wrapped in try/except
- On failure: log the error, store in `failed_jobs`, do not crash the worker
- Never silently swallow exceptions — always log with context

### 4.4 Logging

- Use the structured logger from `app/logging.py`
- Log level via `LOG_LEVEL` env var
- Never log raw user messages
- Never log full listing descriptions at INFO level (use DEBUG)
- Include context: `source`, `listing_id`, `user_id` where relevant

---

## 5. Database Rules

- Never write raw SQL — use SQLAlchemy ORM only
- Never mutate DB schema manually — use Alembic migrations
- Every schema change requires a new Alembic migration file
- Always use `AsyncSession` from `db/session.py` — never create sessions inline
- Enforce `unique` constraints at DB level, not only in code
- Always set `created_at` with `server_default=func.now()`

### Required tables (do not rename or remove columns):

```text
users, user_searches, listings, listing_analysis,
matches, notifications, feedback
```

---

## 6. Configuration Rules

- All secrets and config go in `.env` only — never hardcoded
- Use `app/config.py` (Pydantic Settings) to load all env vars
- Required vars: `DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `LOG_LEVEL`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- Provide a complete `.env.example` — updated whenever new vars are added
- Never commit `.env` to git

---

## 7. Data Source Rules

### 7.1 Legal guardrails

Before implementing any source adapter:

```text
[ ] Is access allowed?
[ ] Is commercial SaaS use allowed?
[ ] Is automated collection allowed?
[ ] Are images/descriptions reusable?
[ ] Can we store listing data?
[ ] Must we link back to source?
[ ] Rate limits documented?
[ ] GDPR implications reviewed?
```

**Do not implement a source that has not passed this checklist.**
Record the review in `Tasks/03_data_sources.md` under the source's section.

### 7.2 Do not scrape Idealista directly

Playwright or HTTP scraping of `idealista.com` is forbidden as the primary data source.
It may be used for private experiments but must not be in production code.

### 7.3 Deduplication is mandatory

All ingested listings must be deduplicated before insert.
Use `dedup_hash` based on: `price + city + area_m2 + title`.
Update `last_seen_at` on re-encounter. Never insert a duplicate.

---

## 8. AI Analysis Rules

- Only analyze listings that passed hard filters and have `should_notify = True`
- Strip phone numbers and emails from listing text before sending to LLM
- Use the structured JSON prompt from §12 of the MVP plan — do not deviate
- Validate LLM output with Pydantic before storing
- If AI fails: fall back gracefully — send notification without AI section
- Never re-analyze a listing that already has a valid `listing_analysis` row
- Cache analysis results — one per listing, shared across users
- Store `model_name` and `analysis_version` for every analysis

### Forbidden AI tasks:

```text
✗ Score tenants, landlords, nationalities, or creditworthiness
✗ Make legal conclusions
✗ Invent missing facts
✗ Process every listing without pre-filtering
✗ Store unnecessary personal data
```

---

## 9. Privacy Rules (Non-negotiable)

- Never log user message content
- Never store phone numbers or emails in normalized listing fields
- Strip contact data from listing text before sending to AI
- `/delete_me` must remove: user, user_searches, matches, feedback, notifications
- Store `consent_at` before creating any user search
- Add AI disclaimer to every alert: *"AI analysis is informational only, not legal advice"*
- Scoring must apply to listings only — never to people

---

## 10. Telegram Bot Rules

- All bot message strings must exist in both English and Russian
- Always check `users.language` before sending any message
- Do not hard-code any user-visible text in handler files — use translation helpers
- All inline keyboards must be defined in `keyboards.py` — not inline in handlers
- Every feedback button callback must include `listing_id`
- Prevent duplicate alerts by checking `notifications` table before sending

---

## 11. Testing Rules

- Write unit tests for all scoring and normalization logic
- Write at least one integration test per epic: end-to-end from import → match → notification
- Place tests in `tests/` mirroring the `app/` structure
- Use `pytest` + `pytest-asyncio`
- All tests must pass before marking a task `✅ Done`
- Use fixtures — never real production DB or real Telegram token in tests

---

## 12. Git Rules

### Commit message format:

```text
<type>(<scope>): <short description>

Types: feat | fix | chore | docs | test | refactor
Scope: foundation | bot | sources | matching | ai | notify | admin | privacy | payments

Examples:
  feat(bot): add /start handler with language selection
  feat(matching): implement deterministic scoring rules
  fix(sources): handle missing price field in manual import
  chore(db): add Alembic migration for failed_jobs table
  test(matching): add unit tests for hard filter logic
```

### Branch naming:

```text
epic/<number>-<slug>

Examples:
  epic/01-foundation
  epic/02-telegram-bot
  epic/05-matching
```

### Rules:

- One commit per logical unit of work — do not bundle unrelated changes
- Never commit `.env`, `__pycache__`, `.pyc`, or migration outputs from failed runs
- Always run tests before committing

---

## 13. What Not To Build (MVP Scope Guard)

Do not implement these unless explicitly instructed:

```text
✗ Web dashboard or admin panel
✗ Email alerts
✗ Mobile app
✗ Multiple city support (Barcelona only for MVP)
✗ ML-based recommender
✗ Advanced Stripe subscription logic (before M2 is validated)
✗ Public listing portal
✗ Many languages beyond EN and RU
✗ Complex scraping infrastructure as primary source
```

If you are unsure whether a feature is in scope, refer to §5 of `ai_housing_finder_spain_mvp_plan.md`.

---

## 14. Milestone Gating

Respect milestone boundaries. Do not work on M2 features while M1 is incomplete.

```text
Milestone 1 (M1) — Technical Prototype
  Required before M2:
  ✅ Bot running with /start and search creation
  ✅ Manual listing import works
  ✅ Basic matching produces results
  ✅ User can receive a test alert
  ✅ Feedback buttons work and save to DB

Milestone 2 (M2) — Automated Beta
  Required before M3:
  ✅ At least one automated source adapter
  ✅ AI analysis integrated
  ✅ Full pipeline: ingest → normalize → deduplicate → match → analyze → notify
  ✅ Deployed to server

Milestone 3 (M3) — Paid Validation
  Required before Epic 9 (Payments):
  ✅ ≥5 users confirm alerts are useful
  ✅ ≥1 user pays manually for access
  ✅ ≥1 user books a viewing after an alert
```

---

## 15. Definition of Ready (Before Starting a Task)

A task is ready to start only when:

- [ ] All P1 tasks in earlier epics are `✅ Done`
- [ ] The task is `⬜ Todo` in the task file
- [ ] Dependencies (DB, config, base classes) exist
- [ ] You understand what "Done" looks like from the task file

---

## Quick Reference

| Resource | Path |
|----------|------|
| Full MVP plan | [`ai_housing_finder_spain_mvp_plan.md`](./ai_housing_finder_spain_mvp_plan.md) |
| Task index | [`Tasks/README.md`](./Tasks/README.md) |
| Foundation tasks | [`Tasks/01_foundation.md`](./Tasks/01_foundation.md) |
| Bot tasks | [`Tasks/02_telegram_bot.md`](./Tasks/02_telegram_bot.md) |
| Data source tasks | [`Tasks/03_data_sources.md`](./Tasks/03_data_sources.md) |
| Normalization tasks | [`Tasks/04_listing_normalization.md`](./Tasks/04_listing_normalization.md) |
| Matching tasks | [`Tasks/05_matching.md`](./Tasks/05_matching.md) |
| AI analysis tasks | [`Tasks/06_ai_analysis.md`](./Tasks/06_ai_analysis.md) |
| Notifications tasks | [`Tasks/07_notifications.md`](./Tasks/07_notifications.md) |
| Admin tasks | [`Tasks/08_admin_operations.md`](./Tasks/08_admin_operations.md) |
| Privacy tasks | [`Tasks/09_privacy_compliance.md`](./Tasks/09_privacy_compliance.md) |
| Payments tasks | [`Tasks/10_payments.md`](./Tasks/10_payments.md) |

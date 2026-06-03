# Relocation Rental Radar

> A bilingual AI rental radar for people relocating to Spain.
> Monitors rental listings, filters noise, detects red flags, and sends Telegram alerts in English and Russian.

---

## 🚦 Project Status

**Current Milestone:** Milestone 2 — Automated Beta (In Progress)

| Module | Status | Description |
| :--- | :--- | :--- |
| **Foundation** | ✅ Done | Database, Migrations, Env Config, Logging |
| **Telegram Bot** | ✅ Done | /start, Onboarding, Search Filters, Feedback |
| **Data Sources** | 🔄 In Progress | Manual Import (✅), RapidAPI (🔄), User Submission (⬜) |
| **Matching Engine** | ✅ Done | Hard Filters, Deterministic Scoring, Deduplication |
| **AI Analysis** | ✅ Done | Ollama Integration, Summary, Red Flag Detection |
| **Notifications** | ✅ Done | Bilingual Telegram Alerts, Feedback Buttons |
| **Deployment** | ✅ Done | Docker Compose setup, Main entry point |

---

## What it does

- Connects to rental listing sources (manual import, user-submitted URLs, and approved APIs)
- Normalizes listings into a single database schema
- Matches listings against user-defined filters (city, price, rooms, areas, furnished, etc.)
- Runs AI analysis (Ollama) for promising listings — summary, red flags, contract warnings
- Sends instant Telegram alerts with feedback buttons
- Supports `/delete_me` for full privacy compliance

---

## Tech stack

| Layer | Technology |
|---|---|
| Bot | aiogram 3.x |
| Database | PostgreSQL 16 + SQLAlchemy (async) + Alembic |
| Config | Pydantic Settings v2 |
| Logging | structlog |
| AI | Ollama (local LLM) |
| Workers | APScheduler (async) |
| Infrastructure | Docker Compose |

---

## Quick start

### 1. Clone and configure

```bash
git clone <repo-url> rental-radar
cd rental-radar
cp .env.example .env
# Edit .env — add your TELEGRAM_BOT_TOKEN and other settings
```

### 2. Start infrastructure

```bash
docker compose up -d
```

This starts PostgreSQL (port 5432) and Redis (port 6379).

### 3. Set up Python environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Run tests

```bash
pytest
```

### 6. Start the bot

```bash
python -m app.main
```

---

## Project structure

```
app/
  main.py           — entry point
  config.py         — Pydantic Settings + .env
  logging.py        — structlog setup

  db/
    session.py      — async engine and session factory
    models.py       — all ORM models
    migrations/     — Alembic migrations

  bot/
    telegram_app.py       — bot application factory
    handlers_start.py     — /start, onboarding
    handlers_filters.py   — filter editing
    handlers_feedback.py  — feedback callbacks
    keyboards.py          — inline keyboards

  sources/
    base.py               — BaseSource interface
    normalized_listing.py — NormalizedListing model
    manual_import.py      — CSV/JSON import
    user_submitted.py     — user-submitted URLs

  services/
    matching.py           — filters + scoring
    scoring.py            — deterministic rules
    ai_analysis.py        — Ollama adapter
    notifications.py      — alert formatting/sending
    deduplication.py      — dedup hash logic
    translation.py        — EN/RU strings

  workers/
    ingest_worker.py      — source polling loop
    analyze_worker.py     — AI analysis queue
    notify_worker.py      — notification delivery

  admin/
    simple_cli.py         — admin CLI

tests/             — mirrors app/ structure
docker-compose.yml
requirements.txt
alembic.ini
```

---

## Initial city

**Barcelona only** for MVP. Multi-city support comes after validation.

---

## Languages

English and Russian.

---

## Privacy

- `/delete_me` removes all user data
- No logging of user message content
- AI analysis is informational only, not legal advice
- Contact data stripped before sending to LLM

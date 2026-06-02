# 01 — Foundation

**Epic 1 · Milestone 1 · Day 1**

Project infrastructure, database, configuration, and developer tooling.
This epic is the hardest blocker — nothing else can start without it.

---

## Priority

`P1 — Critical`

All tasks in this file must be completed before any other epic can begin.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Repository & Project Setup

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.1 | Create Git repository (`rental-radar`) | P1 | ✅ |
| 1.2 | Define project folder structure per architecture plan | P1 | ✅ |
| 1.3 | Add `.gitignore` (Python, Docker, `.env`) | P1 | ✅ |
| 1.4 | Add `README.md` with project description | P2 | ✅ |
| 1.5 | Add `requirements.txt` with initial dependencies | P1 | ✅ |

---

### Docker & Infrastructure

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.6 | Create `docker-compose.yml` with PostgreSQL service | P1 | ✅ |
| 1.7 | Add Redis service to Docker Compose (for later async workers) | P3 | ✅ |
| 1.8 | Verify `docker compose up` starts all services cleanly | P1 | ✅ |

---

### Configuration

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.9 | Create `app/config.py` with Pydantic Settings model | P1 | ✅ |
| 1.10 | Create `.env.example` with all required variables | P1 | ✅ |
| 1.11 | Add config vars: `DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `LOG_LEVEL` | P1 | ✅ |

---

### Database & ORM

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.12 | Set up SQLAlchemy async session in `app/db/session.py` | P1 | ✅ |
| 1.13 | Create initial SQLAlchemy models in `app/db/models.py` | P1 | ✅ |
| 1.14 | Models: `User`, `UserSearch`, `Listing`, `ListingAnalysis`, `Match`, `Notification`, `Feedback` | P1 | ✅ |
| 1.15 | Initialize Alembic in `app/db/migrations/` | P1 | ✅ |
| 1.16 | Generate and apply initial Alembic migration | P1 | ✅ |
| 1.17 | Verify all tables created in PostgreSQL | P1 | ✅ |

---

### Logging

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.18 | Create `app/logging.py` with structured logging setup | P2 | ✅ |
| 1.19 | Use JSON or readable log format with level control via `.env` | P2 | ✅ |

---

### Testing Foundation

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1.20 | Add `pytest` and `pytest-asyncio` to requirements | P2 | ✅ |
| 1.21 | Add basic smoke test: DB connects, models import cleanly | P2 | ✅ |

---

## Definition of Done

```text
✅ docker compose up brings up PostgreSQL (and Redis)
✅ Alembic migration applies cleanly
✅ All 7 database tables exist
✅ Config loads from .env without errors
✅ Structured logging writes to stdout
✅ pytest passes with no errors
```

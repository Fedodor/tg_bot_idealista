# 08 — Admin & Operations

**Epic 8 · Milestone 2 · Day 3 & Day 7**

Admin CLI, failed job tracking, retry logic, source monitoring, and deployment.

---

## Priority

`P2 — High`

Needed for Day 7 deployment and ongoing beta operations.
Admin tools allow manual control during beta without a web dashboard.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Admin CLI (Day 3)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.1 | Create `app/admin/simple_cli.py` | P2 | ✅ |
| 8.2 | CLI command: `import` — load CSV/JSON file of listings | P2 | ✅ |
| 8.3 | CLI command: `inspect` — list recent new listings with key fields | P2 | ⬜ |
| 8.4 | CLI command: `users` — list all active users and their search configs | P2 | ⬜ |
| 8.5 | CLI command: `matches` — show recent matches per user | P2 | ⬜ |
| 8.6 | CLI command: `stats` — ingested / matched / notified / failed counts | P2 | ✅ |
| 8.7 | Use `typer` or `argparse` for CLI interface | P3 | ✅ |

---

### Failed Job Tracking

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.8 | Add `failed_jobs` table to DB schema: `id`, `job_type`, `payload`, `error`, `created_at`, `retry_count` | P2 | ⬜ |
| 8.9 | On ingestion failure: log to `failed_jobs` | P2 | ⬜ |
| 8.10 | On analysis failure: log to `failed_jobs` | P2 | ⬜ |
| 8.11 | On notification failure: log to `failed_jobs` | P2 | ⬜ |

---

### Retry Logic

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.12 | Add retry worker that processes `failed_jobs` with `retry_count < 3` | P2 | ⬜ |
| 8.13 | Exponential backoff between retries | P3 | ⬜ |
| 8.14 | Mark jobs as `dead` after max retries reached | P2 | ⬜ |
| 8.15 | CLI command: `retry` — manually trigger retry for dead jobs | P3 | ⬜ |

---

### Source Monitoring (Day 7)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.16 | Track last successful fetch time per source | P2 | ⬜ |
| 8.17 | Alert (log warn) if source has not returned listings in > 2 hours | P2 | ⬜ |
| 8.18 | Track listings-per-fetch count per source | P2 | ⬜ |
| 8.19 | Store source health status in DB or config for visibility | P3 | ⬜ |

---

### Notification Error Logging

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.20 | Log all Telegram send errors with user_id and message content | P2 | ⬜ |
| 8.21 | Detect and handle `bot was blocked by user` error — deactivate user | P2 | ⬜ |
| 8.22 | Detect Telegram rate limiting — back off and retry | P2 | ⬜ |

---

### Backup Strategy (Day 7)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.23 | Set up PostgreSQL daily backup via `pg_dump` | P2 | ⬜ |
| 8.24 | Store backup in local path or remote (S3 / Backblaze) | P3 | ⬜ |
| 8.25 | Document backup restore procedure | P3 | ⬜ |

---

### Deployment (Day 7)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 8.26 | Deploy full stack to own server / VPS via Docker Compose | P2 | ⬜ |
| 8.27 | Set up environment variables on server (`.env` file) | P2 | ⬜ |
| 8.28 | Verify bot is reachable and responds to `/start` on production | P2 | ⬜ |
| 8.29 | Verify ingestion worker runs on schedule | P2 | ⬜ |
| 8.30 | Invite first 10–20 beta users | P2 | ⬜ |

---

## Definition of Done

```text
✅ Admin CLI can import listings and inspect DB
✅ failed_jobs table populated on errors
✅ Retry logic processes failed jobs
✅ Source monitoring logs warn on stale sources
✅ Stack deployed and running on server
✅ Bot responding on production environment
✅ pg_dump backup scheduled
```

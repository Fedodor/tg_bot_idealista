# 03 — Data Sources

**Epic 3 · Milestone 2 · Day 3**

Listing ingestion from allowed sources. Source adapters, legal review, API access, deduplication.

**⚠️ Biggest business and technical risk of the entire project.**

---

## Priority

`P1 — Critical` (architecture & manual import)  
`P2 — High` (automated sources)  
`P3 — Medium` (additional sources, partner feeds)

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Source Architecture (Day 3)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.1 | Create abstract source interface `app/sources/base.py` | P1 | ⬜ |
| 3.2 | Define `NormalizedListing` dataclass in `normalized_listing.py` | P1 | ⬜ |
| 3.3 | All source adapters must return the same `NormalizedListing` format | P1 | ⬜ |
| 3.4 | Add source health check method to base interface | P2 | ⬜ |
| 3.5 | Add rate limit handling utilities | P2 | ⬜ |

---

### Manual Import Source (Day 3 — MVP Blocker)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.6 | Implement `app/sources/manual_import.py` for CSV/JSON input | P1 | ⬜ |
| 3.7 | Define expected CSV/JSON schema with all required fields | P1 | ⬜ |
| 3.8 | Validate and map input to `NormalizedListing` | P1 | ⬜ |
| 3.9 | Write sample test import file with 5–10 Barcelona listings | P1 | ⬜ |
| 3.10 | Verify manual import inserts listings into DB correctly | P1 | ⬜ |

---

### User-Submitted Listings

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.11 | Implement `app/sources/user_submitted.py` for URL submission | P2 | ⬜ |
| 3.12 | Bot command or message handler to accept a listing URL | P2 | ⬜ |
| 3.13 | Store submitted URL with `source = UserSubmitted` | P2 | ⬜ |

---

### Idealista Official API

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.14 | Submit Idealista official API access request (use template from §21 of plan) | P1 | ⬜ |
| 3.15 | Document API response status and timeline | P2 | ⬜ |
| 3.16 | Implement `app/sources/idealista_official_api.py` only if access approved | P2 | ⬜ |
| 3.17 | Map Idealista API response to `NormalizedListing` | P2 | ⬜ |

---

### RapidAPI Idealista (Fallback)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.18 | Review RapidAPI Idealista Real Estate terms of service | P1 | ⬜ |
| 3.19 | Check: commercial SaaS use allowed? Resale rights? Rate limits? GDPR? | P1 | ⬜ |
| 3.20 | Implement `app/sources/rapidapi_idealista.py` only if terms are acceptable | P2 | ⬜ |
| 3.21 | Map RapidAPI response to `NormalizedListing` | P2 | ⬜ |
| 3.22 | Add error handling and rate limit backoff | P2 | ⬜ |

---

### Other Sources Research

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.23 | Research Fotocasa — access terms and API availability | P3 | ⬜ |
| 3.24 | Research Habitaclia — access terms | P3 | ⬜ |
| 3.25 | Research pisos.com — access terms | P3 | ⬜ |
| 3.26 | Research Badi (rooms) — access terms | P3 | ⬜ |
| 3.27 | Research RSS feeds from any allowed source | P3 | ⬜ |
| 3.28 | Research agency partner CSV/XML feeds | P3 | ⬜ |
| 3.29 | Complete source review checklist for each investigated source | P2 | ⬜ |

---

### Deduplication

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.30 | Implement deduplication by URL / `external_id` / hash in `services/deduplication.py` | P1 | ⬜ |
| 3.31 | Generate `dedup_hash` from price + city + area + title | P1 | ⬜ |
| 3.32 | Skip insert if listing with same hash already exists | P1 | ⬜ |
| 3.33 | Update `last_seen_at` on re-encountered listings | P2 | ⬜ |

---

### Ingestion Worker

| # | Task | Priority | Status |
|---|------|----------|--------|
| 3.34 | Create `app/workers/ingest_worker.py` with polling loop | P2 | ⬜ |
| 3.35 | Use APScheduler or simple async loop for MVP | P2 | ⬜ |
| 3.36 | Log ingestion results: new / duplicate / failed per source | P2 | ⬜ |

---

## Source Review Checklist Template

For each source before using it:

```text
[ ] Is access allowed?
[ ] Is commercial SaaS use allowed?
[ ] Is automated collection allowed?
[ ] Are images/descriptions reusable?
[ ] Can we store listing data?
[ ] Can we show listing summaries?
[ ] Must we link back to the original source?
[ ] What rate limits apply?
[ ] What happens if the source blocks us?
[ ] GDPR implications?
```

---

## Definition of Done

```text
✅ NormalizedListing dataclass defined and documented
✅ Manual CSV/JSON import works end-to-end
✅ Sample listings importable and stored in DB
✅ Deduplication prevents duplicate rows
✅ Idealista API access request submitted
✅ RapidAPI terms reviewed and decision documented
✅ Ingest worker runs on schedule
```

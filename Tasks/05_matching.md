# 05 — Matching Engine

**Epic 5 · Milestone 1–2 · Day 4**

Hard filters, deterministic scoring, and match creation.
This is what turns ingested listings into personalised user results.

---

## Priority

`P1 — Critical`

Matching is the core product logic. Without it users receive nothing.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Hard Filters (Day 4)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.1 | Create `app/services/matching.py` | P1 | ✅ |
| 5.2 | Filter by `city` — must match user search city | P1 | ✅ |
| 5.3 | Filter by `rental_type` — apartment / room / both | P1 | ✅ |
| 5.4 | Filter by `price` — must be within user `min_price`–`max_price` | P1 | ✅ |
| 5.5 | Filter out listings with `status = removed` | P1 | ✅ |
| 5.6 | Filter by `preferred_areas` if set | P2 | ⬜ |
| 5.7 | Filter out `excluded_areas` if set | P2 | ⬜ |
| 5.8 | Filter by `must_have` flags (furnished, empadronamiento, pet-friendly, etc.) | P2 | ⬜ |

---

### Scoring Engine (Day 4)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.9 | Create `app/services/scoring.py` with deterministic scoring rules | P1 | ✅ |
| 5.10 | `+30` price within budget | P1 | ✅ |
| 5.11 | `+15` preferred area match | P1 | ✅ |
| 5.12 | `+10` furnished (if requested) | P2 | ✅ |
| 5.13 | `+10` empadronamiento mentioned | P2 | ⬜ |
| 5.14 | `+10` long-term contract | P2 | ⬜ |
| 5.15 | `+10` near metro (if requested) | P3 | ⬜ |
| 5.16 | `-20` no photos | P2 | ⬜ |
| 5.17 | `-25` suspiciously low price | P2 | ⬜ |
| 5.18 | `-25` temporada contract when user wants long-term | P2 | ⬜ |
| 5.19 | `-20` agency fee when user excluded it | P2 | ⬜ |
| 5.20 | `-30` unclear/missing location | P2 | ⬜ |
| 5.21 | `-30` missing basic information | P2 | ⬜ |
| 5.22 | Clamp final score to 0–100 range | P1 | ✅ |

---

### Score Bands

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.23 | Map score to band: 0–49 Poor · 50–69 Average · 70–84 Good · 85–100 Excellent | P2 | ⬜ |
| 5.24 | Only notify users for listings with score ≥ 50 (configurable threshold) | P1 | ⬜ |

---

### Match Creation

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.25 | For each passing listing, create or update row in `matches` table | P1 | ✅ |
| 5.26 | Enforce `unique(user_id, listing_id)` constraint — no duplicate matches | P1 | ✅ |
| 5.27 | Set `should_notify = True` on new matches above score threshold | P1 | ✅ |

---

### Match Reason Generation

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.28 | Generate human-readable `reason_en` explaining why a listing matched | P1 | ⬜ |
| 5.29 | Generate `reason_ru` Russian equivalent | P2 | ⬜ |
| 5.30 | Include top positive signals and any negative signals in reason text | P2 | ⬜ |

---

### Matching Worker

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.31 | Run matching for all active `user_searches` after each ingest cycle | P1 | ⬜ |
| 5.32 | Skip listings already matched for a user | P1 | ⬜ |
| 5.33 | Log match statistics per cycle | P2 | ⬜ |

---

### Tests

| # | Task | Priority | Status |
|---|------|----------|--------|
| 5.34 | Unit test hard filter logic with fixture listings | P2 | ⬜ |
| 5.35 | Unit test scoring with known inputs and expected scores | P2 | ⬜ |
| 5.36 | Integration test: import listing → match → match row in DB | P2 | ⬜ |

---

## Score Formula Reference

```text
Final Score =
  40% hard filters (pass/fail gate)
  25% price/location fit
  20% listing completeness
  15% AI risk assessment (added after Epic 6)
```

---

## Definition of Done

```text
✅ Hard filters correctly exclude out-of-budget and wrong-type listings
✅ Scoring logic applies all + and - rules
✅ Matches created in DB for passing listings
✅ should_notify set correctly
✅ reason_en generated for each match
✅ Unit and integration tests pass
```

# 04 — Listing Normalization

**Epic 4 · Milestone 2 · Day 3**

Transform raw source data into a unified, queryable listing format.
All source adapters must produce the same `NormalizedListing` output.

---

## Priority

`P1 — Critical`

Without normalization, the matching engine and AI analysis cannot run.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### NormalizedListing Model

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.1 | Define `NormalizedListing` dataclass / Pydantic model in `app/sources/normalized_listing.py` | P1 | ⬜ |
| 4.2 | Include all fields: `source`, `external_id`, `url`, `title`, `description`, `price`, `currency`, `city`, `district`, `neighborhood`, `address_text` | P1 | ⬜ |
| 4.3 | Include property fields: `rental_type`, `area_m2`, `rooms`, `bathrooms`, `floor`, `has_elevator`, `is_furnished`, `agency_or_private`, `available_from` | P1 | ⬜ |
| 4.4 | Include meta fields: `raw_data`, `first_seen_at`, `last_seen_at`, `status`, `dedup_hash` | P1 | ⬜ |
| 4.5 | Validate all required fields are present before insert | P1 | ⬜ |

---

### Apartment Listing Normalization

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.6 | Extract `price` from raw listing (handle ranges, suffixes like `/mes`, `/month`) | P1 | ⬜ |
| 4.7 | Normalize `currency` (default EUR) | P1 | ⬜ |
| 4.8 | Extract `city` and `district` / `neighborhood` from address or metadata | P1 | ⬜ |
| 4.9 | Extract `area_m2` (handle `m²`, `m2`, `sqm` variants) | P1 | ⬜ |
| 4.10 | Extract `rooms` and `bathrooms` count | P1 | ⬜ |
| 4.11 | Detect `is_furnished` from description keywords (`amueblado`, `furnished`) | P2 | ⬜ |
| 4.12 | Detect `has_elevator` from description (`ascensor`, `elevator`) | P2 | ⬜ |
| 4.13 | Set `rental_type = apartment` | P1 | ⬜ |

---

### Room Listing Normalization

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.14 | Apply same normalization pipeline for room listings | P1 | ⬜ |
| 4.15 | Set `rental_type = room` | P1 | ⬜ |
| 4.16 | Handle room-specific fields (shared apartment, number of flatmates) where available | P3 | ⬜ |

---

### Contract & Agency Detection

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.17 | Detect `agency_or_private` from listing metadata or text keywords | P2 | ⬜ |
| 4.18 | Detect contract type hints: `temporada`, `larga duración`, `long-term` | P2 | ⬜ |
| 4.19 | Store detected contract type in `raw_data` for AI analysis | P2 | ⬜ |

---

### Raw Data Storage

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.20 | Store original source payload in `listings.raw_data` as JSON | P1 | ⬜ |
| 4.21 | Never overwrite `raw_data` on re-ingestion — keep original | P2 | ⬜ |

---

### Normalization Service

| # | Task | Priority | Status |
|---|------|----------|--------|
| 4.22 | Create `app/services/normalization.py` with reusable extraction functions | P1 | ⬜ |
| 4.23 | Unit test price extraction with edge cases | P2 | ⬜ |
| 4.24 | Unit test area extraction with different unit formats | P2 | ⬜ |
| 4.25 | Unit test city/district detection | P2 | ⬜ |

---

## Definition of Done

```text
✅ NormalizedListing model validates all required fields
✅ Apartment and room listings normalize correctly
✅ Price, area, rooms extracted from text with edge cases handled
✅ raw_data stored per listing
✅ Unit tests pass for extraction functions
```

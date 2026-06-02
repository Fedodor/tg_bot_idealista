# 06 — AI Analysis

**Epic 6 · Milestone 2 · Day 6**

Local LLM integration via Ollama, structured JSON prompts, red flag detection, bilingual summaries.

---

## Priority

`P2 — High`

AI runs only on matched listings. The product degrades gracefully without it — deterministic scoring still works.
Do not block MVP on AI. Add it after the matching pipeline is stable.

---

## Status Legend

| Symbol | Status |
|--------|--------|
| ⬜ | Todo |
| 🔄 | In Progress |
| ✅ | Done |

---

## Tasks

### Ollama Setup (Day 6)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.1 | Install and verify Ollama on local server | P2 | ⬜ |
| 6.2 | Pull a suitable model (e.g. `llama3`, `mistral`, `phi3`) | P2 | ⬜ |
| 6.3 | Test Ollama REST API responds at `http://localhost:11434` | P2 | ⬜ |
| 6.4 | Add `OLLAMA_BASE_URL` and `OLLAMA_MODEL` to config / `.env` | P2 | ⬜ |

---

### LLM Adapter

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.5 | Create `app/services/ai_analysis.py` with Ollama HTTP client | P2 | ✅ |
| 6.6 | Implement `analyze_listing(listing_text, language)` function | P2 | ✅ |
| 6.7 | Add timeout and retry logic for Ollama requests | P2 | ✅ |
| 6.8 | Abstract adapter so it can be swapped for OpenAI or vLLM later | P3 | ⬜ |

---

### Structured JSON Prompt (Day 6)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.9 | Implement the analysis prompt from §12 of the plan | P2 | ✅ |
| 6.10 | Prompt instructs LLM to return strict JSON only | P2 | ✅ |
| 6.11 | JSON schema: `summary`, `rental_type`, `contract_type`, `empadronamiento`, `risk_level`, `red_flags`, `positive_signals`, `questions_to_ask`, `explanation` | P2 | ✅ |
| 6.12 | Strip phone numbers and emails from `listing_text` before sending to LLM | P2 | ✅ |
| 6.13 | Inject `language` param (EN or RU) so LLM outputs in correct language | P2 | ✅ |

---

### JSON Output Validation (Day 6)

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.14 | Parse LLM response as JSON | P2 | ✅ |
| 6.15 | Validate all required fields present with Pydantic model | P2 | ✅ |
| 6.16 | Handle malformed / partial JSON gracefully | P2 | ✅ |
| 6.17 | Log validation errors with raw LLM output for debugging | P2 | ✅ |

---

### Fallback Strategy

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.18 | If AI fails: set `risk_level = unknown`, skip AI fields | P2 | ⬜ |
| 6.19 | Still send notification — just without AI summary section | P2 | ⬜ |
| 6.20 | Mark `listing_analysis` row as `analysis_failed` for retry | P3 | ⬜ |

---

### Listing Analysis Storage

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.21 | Save analysis result to `listing_analysis` table | P2 | ✅ |
| 6.22 | Store `summary_en`, `summary_ru`, `risk_level`, `red_flags`, `positive_signals`, `questions_to_ask` | P2 | ✅ |
| 6.23 | Store `model_name` and `analysis_version` for traceability | P2 | ✅ |
| 6.24 | Do not re-analyze listings that already have a valid analysis | P2 | ✅ |

---

### Analysis Worker

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.25 | Create `app/workers/analyze_worker.py` | P2 | ✅ |
| 6.26 | Poll `matches` table for rows with `should_notify = True` and no `listing_analysis` | P2 | ✅ |
| 6.27 | Run AI analysis on those listings | P2 | ✅ |
| 6.28 | Update match score with AI risk factor (15% weight from §13) | P3 | ⬜ |

---

### Good vs Bad Tasks Guardrail

| # | Task | Priority | Status |
|---|------|----------|--------|
| 6.29 | Prompt explicitly forbids legal conclusions | P2 | ⬜ |
| 6.30 | Prompt says: mark unknown facts as `unknown`, do not invent | P2 | ⬜ |
| 6.31 | Never run AI on listings that failed hard filter | P1 | ⬜ |
| 6.32 | Cache analysis result — do not re-analyze the same listing for different users | P2 | ⬜ |

---

## Definition of Done

```text
✅ Ollama running locally and reachable via HTTP
✅ analyze_listing() returns valid JSON for sample listing
✅ All 9 JSON fields validated by Pydantic
✅ Results stored in listing_analysis table
✅ Fallback works when Ollama is unavailable
✅ Phone numbers/emails stripped before sending to LLM
✅ Analysis not re-run for already-analyzed listings
```

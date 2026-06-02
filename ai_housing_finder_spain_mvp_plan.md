# AI Housing Finder Spain — MVP Specification & SaaS Plan

**Working name:** Relocation Rental Radar  
**Market:** Spain rental housing  
**Initial city:** Barcelona  
**Initial users:** people relocating to Spain  
**Initial interface:** Telegram bot  
**Languages:** English + Russian  
**Product type:** real SaaS, not only a pet project  
**Primary rental types:** apartments + rooms  

---

## 1. Executive Summary

The product is a Telegram-based AI rental assistant for people relocating to Spain.

It monitors rental listing sources, normalizes apartment and room listings, filters them according to user preferences, detects potential risks, and sends only actionable alerts through Telegram.

The core value proposition:

> **A bilingual AI rental radar for people relocating to Spain.**

More practical positioning:

> **Find apartments and rooms in Spain with less noise, faster reaction, and clearer risk analysis.**

The first MVP should not try to become another real estate portal. It should help users **act faster and with more confidence** when looking for housing.

---

## 2. Product Vision

### Problem

People relocating to Spain face several problems when searching for rentals:

- good listings disappear quickly;
- users spend hours manually checking rental portals;
- listings may be overpriced or misleading;
- rental terminology can be confusing for foreigners;
- some listings are rooms, some are apartments, and users often search for both;
- important details are hidden in Spanish text;
- users may not understand risks such as `contrato de temporada`, agency fees, missing `empadronamiento`, unclear deposits, or suspiciously low prices.

### Solution

A Telegram assistant that:

1. Collects rental listings from approved, legal, or otherwise usable sources.
2. Supports both apartments and rooms.
3. Normalizes listings into a single database structure.
4. Matches listings against user filters.
5. Uses AI to summarize listings and detect red flags.
6. Sends instant Telegram alerts.
7. Allows users to give feedback.
8. Learns which listings are useful or irrelevant.

---

## 3. Core Positioning

Avoid positioning the product as simply:

> Faster than Idealista.

This creates unnecessary conflict with portals and is difficult to guarantee.

Better positioning:

> **A bilingual AI rental radar for people relocating to Spain.**

Expanded version:

> For people relocating to Spain who are tired of checking rental portals all day, our Telegram assistant monitors rental opportunities, filters irrelevant listings, explains red flags, and sends only the options worth acting on.

Russian version:

> **AI-радар аренды для переезжающих в Испанию: квартиры, комнаты, риски и уведомления в Telegram.**

---

## 4. Target Audience

### Primary audience

People relocating to Spain:

- international professionals;
- remote workers;
- expats;
- immigrants;
- students;
- Russian-speaking and English-speaking newcomers.

### Initial city

Start with:

```text
Barcelona only
```

Reasons:

- high rental pressure;
- strong relocation demand;
- many expat communities;
- high need for English/Russian explanations;
- easier to validate than launching across all Spain.

### Later cities

After validation:

```text
Madrid
Valencia
Málaga
Alicante
Girona
```

---

## 5. MVP Scope

The first MVP should do only five things well:

```text
1. Receive listing data from allowed sources.
2. Normalize apartments and rooms into one database.
3. Match listings with user preferences.
4. Run AI analysis only for relevant listings.
5. Send Telegram alerts with feedback buttons.
```

Do not build a full web platform at the beginning.

### In scope for MVP

- Telegram bot;
- English/Russian onboarding;
- apartment / room / both search mode;
- Barcelona city support;
- basic filters;
- listing ingestion;
- matching engine;
- AI summary;
- AI red flag detection;
- Telegram alerts;
- feedback buttons;
- `/delete_me` command;
- simple admin CLI.

### Out of scope for first MVP

- full web dashboard;
- advanced analytics;
- public listing portal;
- complex Stripe subscription logic;
- many cities;
- many languages;
- mobile app;
- email alerts;
- ML-based recommender system.

---

## 6. Data Source Strategy

This is the most important business and technical risk.

The product should **not depend only on unofficial scraping of Idealista**.

### 6.1 Preferred source hierarchy

```text
Priority 1: Official APIs and written permissions
Priority 2: Partner feeds from agencies or property managers
Priority 3: Third-party APIs with acceptable commercial/legal terms
Priority 4: Public sources where reuse is allowed
Priority 5: User-submitted listings
Priority 6: Manual/concierge import during beta
Priority 7: Scraping only where permitted and legally reviewed
```

### 6.2 Idealista official API

Idealista provides an official Search API access request page. The official description says the Search API allows integrating property information published on Idealista into a site or app, and access requires contacting Idealista and describing the project.

Source:  
https://developers.idealista.com/access-request

Recommended action:

```text
Submit official API request as early as possible.
```

Do not make official Idealista data access a blocker for the first beta. It may take time or may not be approved.

### 6.3 Idealista legal caution

Idealista's terms state that users may not use automatic mechanisms to copy or extract Idealista content.

Source:  
https://www.idealista.com/ayuda/articulos/legal-statement/?lang=en

Practical implication:

```text
Do not build the SaaS around direct Playwright scraping of Idealista as the main source.
```

This may be acceptable for private experiments, but it is not a stable foundation for a real SaaS.

### 6.4 Third-party Idealista APIs

Because official Idealista API access may be difficult to obtain, third-party APIs can be investigated as possible fallback sources.

One option mentioned:

```text
RapidAPI — Idealista Real Estate by kiwimaker
https://rapidapi.com/kiwimaker/api/idealista-real-estate
```

RapidAPI search result description says this API can search, filter, and enrich real-estate listings from Idealista's catalog across Spain, Portugal, and Italy through a REST interface.

Source:  
https://rapidapi.com/kiwimaker/api/idealista-real-estate

Important caution:

```text
Third-party APIs must be checked carefully before commercial use.
```

Before using a third-party provider, verify:

- whether commercial SaaS use is allowed;
- whether the provider has rights or permission to resell access;
- rate limits;
- pricing;
- data freshness;
- stability;
- GDPR/privacy implications;
- whether images, descriptions, and contact data may be stored;
- whether attribution is required;
- whether the API may disappear or be blocked.

The third-party API should be treated as a **fallback or beta data source**, not as the only long-term dependency.

### 6.5 Other possible data sources

The product can also collect data from other services, not only Idealista.

Potential source categories:

```text
- Fotocasa
- Habitaclia
- pisos.com
- Milanuncios
- Badi or room-rental platforms
- agency websites
- relocation agencies
- property management companies
- public RSS feeds if available
- partner CSV/XML feeds
- user-submitted listing links
- Telegram groups, only if allowed and with care
- manually curated beta imports
```

For each source, create a source review checklist:

```text
[ ] Is access allowed?
[ ] Is commercial use allowed?
[ ] Is automated collection allowed?
[ ] Are images/descriptions reusable?
[ ] Can we store listing data?
[ ] Can we show listing summaries?
[ ] Must we link back to the original source?
[ ] What rate limits apply?
[ ] What happens if the source blocks us?
```

---

## 7. Recommended MVP Data Strategy

For the first beta:

```text
1. Submit official Idealista API request.
2. Investigate RapidAPI Idealista Real Estate as fallback.
3. Add manual CSV/JSON import source.
4. Add support for user-submitted listing URLs.
5. Add at least one non-Idealista source if terms are acceptable.
6. Keep source adapters modular.
```

The product should be source-agnostic:

```text
IdealistaOfficialAPI
RapidAPIIdealista
ManualImport
AgencyFeed
OtherPortalSource
UserSubmittedListing
```

All sources should output the same normalized listing format.

---

## 8. MVP User Flow

### 8.1 Onboarding

User opens Telegram bot and sends:

```text
/start
```

Bot asks:

```text
Welcome! I help people relocating to Spain find apartments and rooms faster.

Choose language:
[English] [Русский]

What are you looking for?
[Apartment] [Room] [Both]

City:
[Barcelona]

Budget:
Min / Max

Preferred areas:
Eixample, Gràcia, Poblenou, Sants, Sant Antoni, etc.

Important:
[Empadronamiento possible]
[Furnished]
[Pet friendly]
[No agency fee]
[Long-term contract]
[Near metro]
```

### 8.2 Alert example

```text
🏠 New rental match

€850 / month
Room in Eixample, Barcelona
Available now

Match: 86/100
Risk level: Low

Why it matches:
- within your budget
- central area
- furnished
- no obvious scam wording

Possible questions to ask:
- Is empadronamiento possible?
- Is the contract long-term or temporary?
- Are utilities included?

[Open listing] [Useful] [Not relevant] [Suspicious] [Hide similar]
```

### 8.3 Feedback buttons

```text
👍 Useful
👎 Not relevant
🚩 Suspicious
📩 I contacted them
🙈 Hide similar
```

Feedback is critical because it helps validate whether the matching logic actually works.

---

## 9. MVP Architecture

### Data flow

```text
Source Adapter
   ↓
Raw Listing Storage
   ↓
Listing Normalizer
   ↓
Deduplication
   ↓
Database
   ↓
Hard Filters
   ↓
Scoring Engine
   ↓
AI Analysis Queue
   ↓
Matching Engine
   ↓
Notification Service
   ↓
Telegram Bot
   ↓
User Feedback
```

### Simplified project structure

```text
rental-radar/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── logging.py
│
│   ├── db/
│   │   ├── session.py
│   │   ├── models.py
│   │   └── migrations/
│
│   ├── bot/
│   │   ├── telegram_app.py
│   │   ├── handlers_start.py
│   │   ├── handlers_filters.py
│   │   ├── handlers_feedback.py
│   │   └── keyboards.py
│
│   ├── sources/
│   │   ├── base.py
│   │   ├── idealista_official_api.py
│   │   ├── rapidapi_idealista.py
│   │   ├── manual_import.py
│   │   ├── user_submitted.py
│   │   └── normalized_listing.py
│
│   ├── services/
│   │   ├── matching.py
│   │   ├── scoring.py
│   │   ├── ai_analysis.py
│   │   ├── notifications.py
│   │   ├── deduplication.py
│   │   └── translation.py
│
│   ├── workers/
│   │   ├── ingest_worker.py
│   │   ├── analyze_worker.py
│   │   └── notify_worker.py
│
│   └── admin/
│       └── simple_cli.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 10. Technology Stack

### Backend

```text
Python
PostgreSQL
SQLAlchemy
Alembic
Docker Compose
```

### Bot

```text
python-telegram-bot
or
aiogram
```

For async architecture, `aiogram` may be more natural.

### Workers

For MVP:

```text
APScheduler or simple async loops
```

Later:

```text
Redis + Celery / RQ / Dramatiq
```

### AI inference

For local server:

```text
Ollama for MVP
vLLM later if GPU is available
llama.cpp for low-resource inference
```

### Hosting

Initial:

```text
Own server / separate PC
```

Later:

```text
VPS
Hetzner
Fly.io
Render
```

---

## 11. Local AI Strategy

The local model should not analyze every listing. It should analyze only listings that pass basic filters.

Recommended pipeline:

```text
New listing
   ↓
Normalize
   ↓
Deduplicate
   ↓
Apply hard filters
   ↓
Apply deterministic scoring
   ↓
If promising: send to local LLM
   ↓
Store AI summary and risk analysis
   ↓
Notify users
```

### Good tasks for a local LLM

```text
- summarize listing;
- detect suspicious wording;
- extract rental contract warnings;
- detect `temporada`;
- detect `empadronamiento` mentions;
- detect unclear deposit/agency fee language;
- generate questions to ask landlord;
- translate summary between English and Russian.
```

### Bad tasks for a local LLM

```text
- exact price fairness without local market data;
- legal conclusions;
- final decision whether the listing is safe;
- processing every listing without filtering;
- storing or analyzing unnecessary personal data.
```

---

## 12. AI Prompt: Listing Analysis

Use structured JSON output.

```text
You are a rental housing assistant for people relocating to Spain.

Analyze the rental listing below.

Return strict JSON only.

Tasks:
1. Summarize the listing briefly.
2. Detect possible red flags.
3. Detect positive signals.
4. Identify whether it looks like long-term rental, temporary rental, room rental, or unknown.
5. Identify whether empadronamiento is mentioned or likely impossible.
6. Generate useful questions to ask the landlord or agency.
7. Give a risk level: low, medium, high.
8. Give a short explanation in the requested language.

Do not make legal conclusions.
Do not invent missing facts.
If something is unclear, mark it as unknown.

Output:

{
  "summary": "",
  "rental_type": "apartment | room | unknown",
  "contract_type": "long_term | temporada | unknown",
  "empadronamiento": "yes | no | unknown",
  "risk_level": "low | medium | high",
  "red_flags": [],
  "positive_signals": [],
  "questions_to_ask": [],
  "explanation": ""
}

Listing:
{listing_text}

Language:
{language}
```

---

## 13. Scoring Strategy

Do not make the score purely AI-based.

Use a hybrid approach:

```text
Final Score =
  40% hard filters
  25% price/location fit
  20% listing completeness
  15% AI risk assessment
```

### Example deterministic scoring

```text
+30 price within budget
+15 preferred area
+10 furnished if requested
+10 empadronamiento mentioned
+10 long-term contract
+10 near metro if requested

-20 no photos
-25 suspiciously low price
-25 temporada when user wants long-term
-20 agency fee if user excluded agency fee
-30 unclear location
-30 missing basic information
```

### Score bands

```text
0–49    Poor
50–69   Average
70–84   Good
85–100  Excellent
```

But the UI should not overemphasize the score. Better wording:

```text
Match: 86/100
Risk level: Low
Why it matches: ...
```

---

## 14. Database Schema MVP

### users

```text
id
telegram_id
language: en / ru
created_at
status: active / deleted
plan: free / beta / pro
```

### user_searches

```text
id
user_id
city
rental_type: apartment / room / both
min_price
max_price
min_rooms
preferred_areas
excluded_areas
keywords
must_have
nice_to_have
created_at
is_active
```

### listings

```text
id
source
external_id
url
title
description
price
currency
city
district
neighborhood
address_text
rental_type: apartment / room / unknown
area_m2
rooms
bathrooms
floor
has_elevator
is_furnished
agency_or_private
available_from
raw_data
first_seen_at
last_seen_at
status: active / removed / unknown
dedup_hash
```

### listing_analysis

```text
id
listing_id
summary_en
summary_ru
risk_level: low / medium / high
red_flags
positive_signals
questions_to_ask
contract_type: long_term / temporada / unknown
empadronamiento_possible: yes / no / unknown
score
model_name
analysis_version
created_at
```

### matches

```text
id
user_id
listing_id
match_score
reason_en
reason_ru
should_notify
created_at
```

### notifications

```text
id
user_id
listing_id
telegram_message_id
sent_at
status
```

Important constraint:

```text
unique(user_id, listing_id)
```

### feedback

```text
id
user_id
listing_id
feedback_type: useful / not_relevant / suspicious / contacted / hide_similar
created_at
```

---

## 15. Privacy and Compliance

Because this is a real SaaS, implement privacy from the beginning.

Minimum requirements:

```text
[ ] Privacy policy
[ ] Terms of service
[ ] /delete_me command
[ ] Minimal personal data storage
[ ] No unnecessary logging of messages
[ ] Do not store more listing data than needed
[ ] Mask phone numbers/emails before sending text to LLM if not needed
[ ] Explain that AI analysis is informational, not legal advice
[ ] Track data sources and their terms
[ ] Store user consent timestamp
```

Sensitive product boundary:

```text
The product helps tenants search listings.
It must not score tenants, landlords, ethnicity, nationality, creditworthiness, or protected characteristics.
```

---

## 16. Business Model

Classic subscription may work, but apartment hunting is usually a short, intense period.

Recommended pricing model:

### Free

```text
Daily digest
1 active search
Barcelona only
No instant alerts
Limited AI explanation
```

### Hunt Pass — €9–19 / 7 days

```text
Instant alerts
AI red flags
Apartment + room search
English/Russian summaries
Questions to ask landlord
Feedback personalization
```

### Pro — €7–12 / month

```text
Multiple searches
Multiple cities later
Priority alerts
Saved listings
Advanced filters
```

### Early beta payment

Before Stripe integration, payments can be handled manually:

```text
- Stripe payment link
- Revolut
- PayPal
- bank transfer
```

Do not build complex subscription infrastructure until users prove they are willing to pay.

---

## 17. Success Metrics

The original metrics were useful but too broad.

Better MVP metrics:

```text
Number of active beta users
Number of created searches
Number of listings ingested
Number of listings matched
Number of alerts sent
Open/click rate on alerts
% alerts marked Useful
% alerts marked Not relevant
% users who contacted landlord
% users who booked viewing
% users who paid for Hunt Pass
Cost per analyzed listing
Cost per paying user
Median time from first_seen_at to notification
```

Main success metric:

```text
Users get useful listings quickly enough to contact landlords before others.
```

---

## 18. Backlog

### Epic 1 — Foundation

```text
[ ] Create repository
[ ] Add Docker Compose
[ ] Add PostgreSQL
[ ] Add Alembic migrations
[ ] Add config via .env
[ ] Add structured logging
[ ] Add basic tests
```

### Epic 2 — Telegram Bot

```text
[ ] Implement /start
[ ] Add language selection EN/RU
[ ] Add rental type selection: apartment / room / both
[ ] Add budget input
[ ] Add preferred areas input
[ ] Add must-have filters
[ ] Add /my_search
[ ] Add /edit_search
[ ] Add /pause
[ ] Add /delete_me
```

### Epic 3 — Data Sources

```text
[ ] Submit Idealista official API access request
[ ] Implement source interface
[ ] Implement manual CSV/JSON import source
[ ] Investigate RapidAPI Idealista Real Estate
[ ] Implement RapidAPI adapter only if terms are acceptable
[ ] Implement Idealista official API adapter if approved
[ ] Add source health checks
[ ] Add rate limit handling
[ ] Add deduplication by URL/external_id/hash
[ ] Research other allowed sources
```

### Epic 4 — Listing Normalization

```text
[ ] Normalize apartment listings
[ ] Normalize room listings
[ ] Extract price
[ ] Extract city/district/neighborhood
[ ] Extract area_m2
[ ] Extract rooms/bathrooms
[ ] Extract furnished/elevator if available
[ ] Detect agency/private where possible
[ ] Detect contract type where possible
[ ] Store raw source payload
```

### Epic 5 — Matching

```text
[ ] Implement hard filters
[ ] Implement scoring rules
[ ] Support apartment/room/both
[ ] Support preferred areas
[ ] Support excluded areas
[ ] Support must-have flags
[ ] Generate match reason EN/RU
```

### Epic 6 — AI Analysis

```text
[ ] Add local LLM adapter
[ ] Add Ollama integration
[ ] Add structured JSON prompt
[ ] Add prompt for red flags
[ ] Add prompt for summary EN
[ ] Add prompt for summary RU
[ ] Add JSON output validation
[ ] Add fallback if AI fails
[ ] Store model name and analysis version
```

### Epic 7 — Notifications

```text
[ ] Send Telegram listing alert
[ ] Prevent duplicate alerts
[ ] Add buttons: Useful / Not relevant / Suspicious / Contacted / Hide similar
[ ] Store feedback
[ ] Add daily digest for free users
[ ] Add instant alerts for beta/pro users
```

### Epic 8 — Admin / Operations

```text
[ ] Add CLI to import listings manually
[ ] Add CLI to inspect new listings
[ ] Add failed job table
[ ] Add retry logic
[ ] Add source monitoring
[ ] Add notification error logging
[ ] Add backup strategy
```

### Epic 9 — Payments Later

```text
[ ] Add Stripe customer table
[ ] Add checkout link
[ ] Add webhook handler
[ ] Add plan expiration
[ ] Add paid limits
```

Do not start Epic 9 before validating demand.

---

## 19. Milestones

### Milestone 1 — Technical Prototype

Goal:

```text
Telegram bot + database + manual listing import + basic matching.
```

Definition of Done:

```text
A user can:
1. open Telegram bot;
2. select English/Russian;
3. create a search;
4. receive matching listings from manually imported data;
5. click the original listing;
6. give feedback.
```

### Milestone 2 — Automated Beta

Goal:

```text
Automated ingestion from at least one usable source.
```

Definition of Done:

```text
The system can:
1. fetch new listings automatically;
2. normalize listings;
3. deduplicate listings;
4. match users;
5. analyze relevant listings with AI;
6. send Telegram alerts.
```

### Milestone 3 — Paid Validation

Goal:

```text
10–20 beta users and first paid Hunt Pass purchases.
```

Definition of Done:

```text
At least 5 users say alerts are useful.
At least 1–3 users pay for access.
At least one user books a viewing after an alert.
```

---

## 20. Seven-Day MVP Roadmap

### Day 1

```text
Repository
Docker Compose
PostgreSQL
Basic models
Telegram bot skeleton
```

### Day 2

```text
Language onboarding
Search creation flow
User filters
/my_search
/edit_search
```

### Day 3

```text
Manual CSV/JSON import
Normalized listing model
Deduplication
Admin CLI
```

### Day 4

```text
Hard filters
Scoring rules
Apartment/room/both logic
Match creation
```

### Day 5

```text
Telegram alerts
Feedback buttons
Notification deduplication
```

### Day 6

```text
Ollama/local LLM integration
AI summary
Red flag detection
JSON validation
```

### Day 7

```text
Deploy to own server
Add source monitoring
Invite 10–20 beta users
Collect feedback
```

This is a beta MVP roadmap, not a full production SaaS roadmap.

---

## 21. Idealista API Access Request Text

Use this text in the `Describe your project` field.

```text
Hello,

I am building an early-stage SaaS product designed to help people relocating to Spain find rental housing more efficiently and safely.

The product is a Telegram-based rental assistant for international users, initially focused on Barcelona. It helps users discover relevant rental listings, understand listing details, identify potential red flags, and receive personalized alerts based on their preferences.

The service is intended for end users looking for long-term rental apartments or rooms. The first version will support English and Russian-speaking users relocating to Spain.

We would like to use the idealista Search API as an official and compliant data source instead of scraping the website. The application would retrieve rental listing information, store only the necessary structured fields, and show users short summaries, links to the original listings, and personalized alert notifications.

We do not intend to republish idealista content as a competing real estate portal. The goal is to drive interested users back to the original listing page and improve discovery, filtering, and understanding for relocation users.

Key features planned:
- personalized rental alerts;
- apartment and room search;
- bilingual English/Russian assistant;
- red-flag detection for unclear or risky listings;
- price and listing quality indicators;
- direct links back to the original source.

The project is currently in MVP stage. We would be happy to comply with your API usage terms, attribution requirements, rate limits, and any restrictions regarding data storage or display.

Thank you.
```

---

## 22. Key Risks

### Data access risk

The biggest risk is not AI. It is reliable and legally safe data access.

Mitigation:

```text
- official API request;
- multiple source adapters;
- third-party API evaluation;
- manual beta import;
- agency partnerships;
- source-agnostic architecture.
```

### Product risk

Users may not pay if alerts are not better than portal alerts.

Mitigation:

```text
- focus on relocants;
- emphasize red flags and explanation;
- collect feedback;
- measure Useful / Not relevant ratio;
- add landlord message templates.
```

### Technical risk

Local AI may be slow or inconsistent.

Mitigation:

```text
- analyze only matched listings;
- use deterministic scoring first;
- validate JSON output;
- add fallback summaries;
- cache results.
```

### Legal/compliance risk

The product handles user preferences and possibly listing/contact data.

Mitigation:

```text
- privacy policy;
- data minimization;
- /delete_me;
- source terms review;
- avoid storing unnecessary contact data;
- avoid legal conclusions.
```

---

## 23. Core Principle

Do not build a general real estate portal.

Build:

> **The fastest practical way for relocants to discover, understand, and act on good rental opportunities in Spain.**

For the first version, success is not “many features”.

Success is:

```text
20 beta users
Barcelona only
Apartment + room alerts
Useful Telegram notifications
AI red flags
User feedback
First paid Hunt Pass purchases
```

---

## 24. Immediate Next Steps

```text
1. Submit Idealista official API access request.
2. Research RapidAPI Idealista Real Estate terms and pricing.
3. Create repository and database schema.
4. Build Telegram onboarding.
5. Implement manual listing import.
6. Implement matching without AI.
7. Add local AI only for matched listings.
8. Find 10–20 beta users among relocants.
9. Test willingness to pay for a 7-day Hunt Pass.
```

---

## 25. References

- Original project plan provided by the user in `Pasted markdown.md`.
- Idealista Search API access request: https://developers.idealista.com/access-request
- Idealista general terms: https://www.idealista.com/ayuda/articulos/legal-statement/?lang=en
- RapidAPI Idealista Real Estate by kiwimaker: https://rapidapi.com/kiwimaker/api/idealista-real-estate
- Ollama API documentation: https://docs.ollama.com/api/introduction
- vLLM OpenAI-compatible server documentation: https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
- llama.cpp repository: https://github.com/ggml-org/llama.cpp

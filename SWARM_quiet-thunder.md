# SWARM Plan — Quiet Thunder (Marketing Copy Census)

> **Source:** GitHub Issues #1–#9 in `davemooney/quiet-thunder`
> **Generated:** 2026-03-18
> **Development branch:** `main`
> **Total WPs:** 9 | **Waves:** 6 + Integration | **Max concurrency:** 3

---

## 1. WORKLOG INVENTORY

| WP | Title | Phase | Type |
|----|-------|-------|------|
| WP-1 | Project scaffolding & brand database (brands.json) | Collection | Technical Task |
| WP-2 | Web copy scraper — landing pages & pricing pages | Collection | Feature |
| WP-3 | App Store listing & social bio collector | Collection | Feature |
| WP-4 | Google Ads & search copy collector | Collection | Feature |
| WP-5 | Facebook Ad Library collection (Manus task) | Collection | Technical Task |
| WP-6 | Copy tagging engine — batch-tag all extracted copy | Analysis | Feature |
| WP-7 | Structural map analysis — identify whitespace territories | Analysis | Feature |
| WP-8 | Copy generation brief & all channel outputs | Generation | Feature |
| WP-9 | Adversarial kill test materials & protocol | Testing | Feature |

---

## 2. DEPENDENCY SURGERY

### 2.1 Raw Dependency Graph (as declared in issues)

```
WP-1  →  (none)
WP-2  →  WP-1   (reads brands.json for URLs)
WP-3  →  WP-1   (reads brands.json for App Store terms + Twitter handles)
WP-4  →  WP-1   (matches ad results to brands via brands.json)
WP-5  →  WP-1   (needs brand list for Facebook Ad Library searches)
WP-6  →  WP-2, WP-3, WP-4, WP-5   (reads all raw/ data)
WP-7  →  WP-6   (reads tagged-copy.json)
WP-8  →  WP-7   (reads COPY-STRUCTURAL-MAP.md)
WP-9  →  WP-8, WP-6   (needs generated copy + competitor data)
```

**Original dependency count: 10**

### 2.2 Dependency Challenges

| Dependency | Challenge Question | Verdict | Reason |
|-----------|-------------------|---------|--------|
| WP-4 → WP-1 | Does WP-4 literally import/use brands.json? | **REMOVE** | WP-4 searches competitive *keywords* (hardcoded in the issue), not brand URLs. Brand-matching against results is a nice-to-have lookup, not a blocking input. The agent can use the known brand list from the issue body. |
| WP-5 → WP-1 | Does WP-5 need brands.json to function? | **REMOVE** | WP-5 is a Manus task. All 13 brand names are hardcoded directly in the Manus prompt inside the issue. Manus never reads brands.json. |
| WP-2 → WP-1 | Does WP-2 need brands.json? | **KEEP** | WP-2 iterates over brands.json to get homepage/pricing URLs. Without it, the agent doesn't know what to fetch. |
| WP-3 → WP-1 | Does WP-3 need brands.json? | **KEEP** | WP-3 reads `appstore_search` terms and `twitter_handle` fields from brands.json. Real data dependency. |
| WP-6 → WP-2 | Does WP-6 need WP-2's output? | **KEEP** | WP-6 loads `raw/{brand}_landing.json` files that WP-2 creates. Hard dependency. |
| WP-6 → WP-3 | Does WP-6 need WP-3's output? | **KEEP** | WP-6 loads `raw/{brand}_appstore.json` and `raw/{brand}_social.json`. Hard dependency. |
| WP-6 → WP-4 | Does WP-6 need WP-4's output? | **KEEP** | WP-6 loads `raw/ads/google_ads.json`. Hard dependency. |
| WP-6 → WP-5 | Does WP-6 need WP-5's output? | **SOFT** | WP-6 loads `raw/ads/facebook_ads.json` but the issue says "Can start with partial data." Facebook ads are supplementary — if Manus is slow, tagging can proceed without it and incorporate later. **Downgrade to soft dependency.** |
| WP-7 → WP-6 | Does WP-7 need tagged-copy.json? | **KEEP** | WP-7's entire input is the tagged dataset. Cannot start without it. |
| WP-8 → WP-7 | Does WP-8 need COPY-STRUCTURAL-MAP.md? | **KEEP** | WP-8 reads the structural map to derive voice rules and generate copy. Hard dependency. |
| WP-9 → WP-8 | Does WP-9 need generated copy? | **KEEP** | Comparison materials require Capsule's copy variants to exist. Hard dependency. |
| WP-9 → WP-6 | Does WP-9 need tagged-copy.json? | **REMOVE** | WP-9 needs "strongest competitor copy" but this is already available from the raw data or embedded in WP-8's outputs. The test protocol doesn't read tagged-copy.json directly. |

### 2.3 Pruned Dependency Graph

```
DEPENDENCY PRUNING
Original dependencies:   10
Removed (false deps):    3  (WP-4→WP-1, WP-5→WP-1, WP-9→WP-6)
Downgraded (soft deps):  1  (WP-6→WP-5)
Remaining (hard deps):   7
Parallelism gain:        WP-4 and WP-5 move from Wave 2 to Wave 1 (run alongside WP-1)

Pruned graph:
  WP-1  →  (none)
  WP-2  →  WP-1
  WP-3  →  WP-1
  WP-4  →  (none)         ← FREED
  WP-5  →  (none)         ← FREED
  WP-6  →  WP-2, WP-3, WP-4  (soft: WP-5)
  WP-7  →  WP-6
  WP-8  →  WP-7
  WP-9  →  WP-8
```

---

## 3. FILE OWNERSHIP MAPPING

### 3.1 File Touchpoints Per WP

| WP | Files Created/Modified | Action |
|----|----------------------|--------|
| WP-1 | `brands.json`, `raw/` (dir), `raw/ads/` (dir), `data/` (dir), `analysis/` (dir), `output/` (dir), `test/` (dirs) | Create all |
| WP-2 | `raw/{brand}_landing.json` (×35-40), `raw/{brand}_pricing.json` (×20-30) | Create |
| WP-3 | `raw/{brand}_appstore.json` (×20-30), `raw/{brand}_social.json` (×15-25) | Create |
| WP-4 | `raw/ads/google_ads.json` | Create |
| WP-5 | `raw/ads/facebook_ads.json` | Create |
| WP-6 | `data/tagged-copy.json` | Create |
| WP-7 | `analysis/COPY-STRUCTURAL-MAP.md` | Create |
| WP-8 | `analysis/COPY-BRIEF.md`, `output/copy-system.html`, `output/COPY-SYSTEM.md`, `output/VIDEO-SCRIPTS.md` | Create |
| WP-9 | `test/comparison-cards/*`, `test/appstore-cards/*`, `test/ad-mockups/*`, `test/TEST-PROTOCOL.md`, `test/test_results.md` | Create |

### 3.2 Conflict Analysis

**No file conflicts.** Every WP writes to unique files/directories. No two WPs touch the same file in any wave.

This is a data pipeline, not a shared codebase — each phase produces distinct output files consumed by the next phase. Merge conflicts are structurally impossible.

### 3.3 Final Ownership Map

| Directory | Wave 1 Owner | Wave 2 Owner | Wave 3 Owner | Wave 4 Owner | Wave 5 Owner | Wave 6 Owner |
|-----------|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
| `brands.json` | WP-1 | — | — | — | — | — |
| `raw/{brand}_landing.json` | — | WP-2 | — | — | — | — |
| `raw/{brand}_pricing.json` | — | WP-2 | — | — | — | — |
| `raw/{brand}_appstore.json` | — | WP-3 | — | — | — | — |
| `raw/{brand}_social.json` | — | WP-3 | — | — | — | — |
| `raw/ads/google_ads.json` | WP-4 | — | — | — | — | — |
| `raw/ads/facebook_ads.json` | WP-5 | — | — | — | — | — |
| `data/tagged-copy.json` | — | — | WP-6 | — | — | — |
| `analysis/COPY-STRUCTURAL-MAP.md` | — | — | — | WP-7 | — | — |
| `analysis/COPY-BRIEF.md` | — | — | — | — | WP-8 | — |
| `output/*` | — | — | — | — | WP-8 | — |
| `test/*` | — | — | — | — | — | WP-9 |

---

## 4. WAVE PLAN

```
WAVE PLAN
Total waves:        6 + Integration
Total agents:       9
Max concurrency:    3 (Wave 1)
Critical path:      WP-1 → WP-2 → WP-6 → WP-7 → WP-8 → WP-9

WAVE 1 — 3 agents (parallel, no dependencies)
  Agent 1: WP-1  Project scaffolding & brand database     Branch: swarm/wp-01-scaffolding
  Agent 2: WP-4  Google Ads & search copy collector        Branch: swarm/wp-04-google-ads
  Agent 3: WP-5  Facebook Ad Library collection (Manus)    Branch: swarm/wp-05-facebook-ads

  NOTE: WP-5 is a MANUS task, not a Claude Code agent. Run it separately.

MERGE WAVE 1 → main
  Merge order: WP-1 first (creates directory structure), then WP-4, then WP-5
  Conflict risk: ZERO (no shared files)
  Integration check: brands.json exists and is valid JSON; raw/ads/ has google_ads.json

---

WAVE 2 — 2 agents (depend on WP-1 for brands.json)
  Agent 4: WP-2  Web copy scraper — landing & pricing     Branch: swarm/wp-02-web-scraper
  Agent 5: WP-3  App Store & social bio collector          Branch: swarm/wp-03-appstore-social

MERGE WAVE 2 → main
  Merge order: WP-2, then WP-3 (no conflict either way)
  Conflict risk: ZERO
  Integration check: raw/ folder has {brand}_landing.json for all brands; {brand}_appstore.json for App Store brands
  Soft dependency note: If WP-5 (Manus) is not yet complete, proceed anyway. WP-6 can tag without facebook_ads.json.

---

WAVE 3 — 1 agent
  Agent 6: WP-6  Copy tagging engine                      Branch: swarm/wp-06-tagging

MERGE WAVE 3 → main
  Merge order: WP-6 only
  Conflict risk: ZERO
  Integration check: data/tagged-copy.json exists, is valid JSON, contains 150+ elements

---

WAVE 4 — 1 agent
  Agent 7: WP-7  Structural map analysis                  Branch: swarm/wp-07-structural-map

MERGE WAVE 4 → main
  Merge order: WP-7 only
  Conflict risk: ZERO
  Integration check: analysis/COPY-STRUCTURAL-MAP.md exists and contains all 8 analysis sections

---

WAVE 5 — 1 agent
  Agent 8: WP-8  Copy generation brief & outputs          Branch: swarm/wp-08-copy-generation

MERGE WAVE 5 → main
  Merge order: WP-8 only
  Conflict risk: ZERO
  Integration check: output/copy-system.html renders in browser; output/COPY-SYSTEM.md and output/VIDEO-SCRIPTS.md exist

---

WAVE 6 — 1 agent
  Agent 9: WP-9  Adversarial kill test materials           Branch: swarm/wp-09-kill-test

MERGE WAVE 6 → main
  Merge order: WP-9 only
  Conflict risk: ZERO
  Integration check: test/ folder populated with comparison cards, App Store cards, ad mockups, and protocol

---

FINAL — Integration & Verification
  Run through all directories and verify completeness
  Validate all JSON files parse correctly
  Open copy-system.html in browser and screenshot
  Verify all 9 issue acceptance criteria are met
  Close all GitHub issues
```

### Visual Pipeline

```
WAVE 1 (parallel)        WAVE 2 (parallel)     WAVE 3      WAVE 4       WAVE 5       WAVE 6
┌──────────────────┐    ┌──────────────────┐   ┌────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐
│ WP-1 Scaffolding │───▶│ WP-2 Web Scraper │──▶│        │  │         │  │          │  │        │
└──────────────────┘    └──────────────────┘   │        │  │         │  │          │  │        │
                        ┌──────────────────┐   │ WP-6   │  │ WP-7    │  │ WP-8     │  │ WP-9   │
                   ───▶ │ WP-3 AppStore    │──▶│ Tagging│─▶│ Struct  │─▶│ Copy Gen │─▶│ Kill   │
                        └──────────────────┘   │ Engine │  │ Map     │  │ + Outputs│  │ Test   │
┌──────────────────┐                           │        │  │         │  │          │  │        │
│ WP-4 Google Ads  │──────────────────────────▶│        │  │         │  │          │  │        │
└──────────────────┘                           │        │  │         │  │          │  │        │
┌──────────────────┐                           │        │  │         │  │          │  │        │
│ WP-5 FB Ads      │ · · · · · · · · · · · · ▶│        │  │         │  │          │  │        │
│ (Manus - async)  │  (soft dep, non-blocking) └────────┘  └─────────┘  └──────────┘  └────────┘
└──────────────────┘
```

---

## 5. ACCEPTANCE CRITERIA AUDIT

All WPs have testable acceptance criteria. Minor additions:

| WP | Issue | Added/Revised |
|----|-------|---------------|
| WP-1 | "35-40 brand entries" is correct but add a minimum | **Added:** "Minimum 26 brands (the explicit list from PRD), target 35-40" |
| WP-4 | No explicit minimum for ads found | **Added:** "If zero ads found across all keywords, document the null finding and note this in the summary log" |
| WP-5 | No fallback if Facebook Ad Library is inaccessible | **Added:** "If Ad Library is blocked or inaccessible, document the failure and proceed — this is a soft dependency" |
| WP-6 | "150 element minimum" — what if collection yields fewer? | **Added:** "If fewer than 120 elements available from raw data, flag to human before proceeding — analysis may lack statistical validity" |

---

## 6. GIT STRATEGY

### 6.1 Branch Naming

```
main                                ← all waves merge here
├── swarm/wp-01-scaffolding         ← Wave 1, Agent 1
├── swarm/wp-04-google-ads          ← Wave 1, Agent 2
├── swarm/wp-05-facebook-ads        ← Wave 1, Agent 3 (Manus)
├── swarm/wp-02-web-scraper         ← Wave 2, Agent 4
├── swarm/wp-03-appstore-social     ← Wave 2, Agent 5
├── swarm/wp-06-tagging             ← Wave 3, Agent 6
├── swarm/wp-07-structural-map      ← Wave 4, Agent 7
├── swarm/wp-08-copy-generation     ← Wave 5, Agent 8
└── swarm/wp-09-kill-test           ← Wave 6, Agent 9
```

### 6.2 Wave 1 Branch Setup Script

```bash
#!/bin/bash
# SWARM Branch Setup — Wave 1
# Run ONCE before launching Wave 1 agents

set -e
DEVELOPMENT_BRANCH="main"

cd ~/quiet-thunder  # or wherever the repo is cloned
git checkout $DEVELOPMENT_BRANCH
git pull origin $DEVELOPMENT_BRANCH

# Create Wave 1 branches
git checkout -b swarm/wp-01-scaffolding $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

git checkout -b swarm/wp-04-google-ads $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

git checkout -b swarm/wp-05-facebook-ads $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

echo "✓ Wave 1 branches created. Launch agents."
```

### 6.3 Wave 1 Merge Script

```bash
#!/bin/bash
# SWARM Merge — Wave 1
# Run after ALL Wave 1 agents report completion

set -e
DEVELOPMENT_BRANCH="main"

cd ~/quiet-thunder
git checkout $DEVELOPMENT_BRANCH

echo "Merging WP-01 (scaffolding — must be first)..."
git merge --no-ff swarm/wp-01-scaffolding -m "swarm(wp-01): Project scaffolding & brand database"

echo "Merging WP-04 (Google Ads)..."
git merge --no-ff swarm/wp-04-google-ads -m "swarm(wp-04): Google Ads & search copy collector"

# WP-05 may not be done yet (Manus is async). Merge if available:
if git rev-parse --verify swarm/wp-05-facebook-ads >/dev/null 2>&1; then
  AHEAD=$(git log $DEVELOPMENT_BRANCH..swarm/wp-05-facebook-ads --oneline | wc -l)
  if [ "$AHEAD" -gt 0 ]; then
    echo "Merging WP-05 (Facebook Ads)..."
    git merge --no-ff swarm/wp-05-facebook-ads -m "swarm(wp-05): Facebook Ad Library collection"
  else
    echo "⚠ WP-05 branch exists but has no commits. Manus may still be working. Skipping."
  fi
else
  echo "⚠ WP-05 branch not found. Manus task may not have started. Proceeding without it."
fi

echo "Wave 1 merged. Creating Wave 2 branches..."

git checkout -b swarm/wp-02-web-scraper $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH
git checkout -b swarm/wp-03-appstore-social $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

echo "✓ Wave 2 branches created. Launch agents."
```

### 6.4 Wave 2 Merge Script

```bash
#!/bin/bash
# SWARM Merge — Wave 2

set -e
DEVELOPMENT_BRANCH="main"

cd ~/quiet-thunder
git checkout $DEVELOPMENT_BRANCH

echo "Merging WP-02 (Web scraper)..."
git merge --no-ff swarm/wp-02-web-scraper -m "swarm(wp-02): Web copy scraper — landing & pricing pages"

echo "Merging WP-03 (App Store & social)..."
git merge --no-ff swarm/wp-03-appstore-social -m "swarm(wp-03): App Store listing & social bio collector"

# Merge WP-05 if it arrived late
if git rev-parse --verify swarm/wp-05-facebook-ads >/dev/null 2>&1; then
  AHEAD=$(git log $DEVELOPMENT_BRANCH..swarm/wp-05-facebook-ads --oneline | wc -l)
  if [ "$AHEAD" -gt 0 ]; then
    echo "Late-merging WP-05 (Facebook Ads)..."
    git merge --no-ff swarm/wp-05-facebook-ads -m "swarm(wp-05): Facebook Ad Library collection (late merge)"
  fi
fi

echo "Wave 2 merged. Integration check..."
echo "Verifying raw/ folder population..."
ls raw/*.json 2>/dev/null | wc -l
ls raw/ads/*.json 2>/dev/null | wc -l

echo "Creating Wave 3 branch..."
git checkout -b swarm/wp-06-tagging $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

echo "✓ Wave 3 branch created. Launch agent."
```

### 6.5 Wave 3-6 Merge Scripts (pattern)

```bash
#!/bin/bash
# SWARM Merge — Wave N (template)
# Replace WAVE_N_WP, WAVE_N_SLUG, WAVE_N_MSG, NEXT_WP_SLUG with actual values

set -e
DEVELOPMENT_BRANCH="main"

cd ~/quiet-thunder
git checkout $DEVELOPMENT_BRANCH

echo "Merging WAVE_N_WP..."
git merge --no-ff swarm/WAVE_N_SLUG -m "swarm(WAVE_N_WP): WAVE_N_MSG"

echo "Creating next wave branch..."
git checkout -b swarm/NEXT_WP_SLUG $DEVELOPMENT_BRANCH
git checkout $DEVELOPMENT_BRANCH

echo "✓ Next wave branch created. Launch agent."
```

**Specific merge commands per wave:**

| Wave | Merge Command | Next Branch |
|------|--------------|-------------|
| 3 | `git merge --no-ff swarm/wp-06-tagging -m "swarm(wp-06): Copy tagging engine"` | `swarm/wp-07-structural-map` |
| 4 | `git merge --no-ff swarm/wp-07-structural-map -m "swarm(wp-07): Structural map analysis"` | `swarm/wp-08-copy-generation` |
| 5 | `git merge --no-ff swarm/wp-08-copy-generation -m "swarm(wp-08): Copy generation brief & outputs"` | `swarm/wp-09-kill-test` |
| 6 | `git merge --no-ff swarm/wp-09-kill-test -m "swarm(wp-09): Adversarial kill test materials"` | (none — done) |

---

## 7. AGENT EXECUTOR PROMPTS

---

### Agent Executor — WP-01: Project Scaffolding & Brand Database

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-01-scaffolding`
**Wave:** 1 of 6
**GitHub Issue:** #1

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-01-scaffolding`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Create the project directory structure and build `brands.json` containing 35-40 competitor brands with validated URLs, App Store search terms, and Twitter handles.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `brands.json` | Create — master brand database |
| `raw/` | Create directory |
| `raw/ads/` | Create directory |
| `data/` | Create directory |
| `analysis/` | Create directory |
| `output/` | Create directory |
| `test/` | Create directory |
| `test/comparison-cards/` | Create directory |
| `test/appstore-cards/` | Create directory |
| `test/ad-mockups/` | Create directory |
| `.gitkeep` files | Create in empty directories to ensure git tracks them |

**Files you must NOT touch:** Everything not listed above.

#### Tasks
- [ ] Create all directories listed above with `.gitkeep` files
- [ ] Research and build `brands.json` with the following structure per brand:
  ```json
  {
    "name": "Brand Name",
    "tier": "direct | adjacent | privacy",
    "website": "https://...",
    "pricing_url": "https://.../pricing",
    "appstore_search": "search term",
    "twitter_handle": "handle_without_at",
    "has_facebook_ads": true,
    "notes": ""
  }
  ```
- [ ] Include all **Tier 1 Direct Competitors** (13): Granola, Otter.ai, Fireflies.ai, Notta, Sonix, Aiko, MacWhisper, Fathom, tl;dv, Krisp, Tactiq, Read.ai, Supernormal
- [ ] Include all **Tier 2 Adjacent Productivity** (8): Obsidian, Notion, Linear, Arc, Things 3, Craft, Raycast, 1Password
- [ ] Include all **Tier 3 Privacy/Security** (5): Signal, ProtonMail, Mullvad VPN, Standard Notes, Tuta
- [ ] Research 9-14 additional relevant brands to reach 35-40 total (search "best meeting transcription tools 2025", "AI meeting notes apps", etc.)
- [ ] Validate all homepage URLs resolve (HTTP 200)
- [ ] Validate all pricing URLs resolve (or mark as `null`)
- [ ] Test App Store search terms against iTunes API: `https://itunes.apple.com/search?term={term}&entity=software&limit=3`
- [ ] Verify Twitter handles exist (or mark as `null`)
- [ ] Create a `validation-log.md` documenting all checks

#### Acceptance Criteria
- [ ] Directory structure matches the spec exactly
- [ ] `brands.json` is valid JSON with minimum 26 brands, target 35-40
- [ ] Every entry has all required fields (null is acceptable, missing fields are not)
- [ ] All homepage URLs validated as reachable
- [ ] `validation-log.md` shows pass/fail for each brand's URL, pricing, App Store, and Twitter checks

#### Implementation Notes
- Use `web_fetch` to validate URLs (check for non-error responses)
- Use Brave Search API (key: `BRAVE_API_KEY` in `.env`) to discover additional brands
- For brands without pricing pages (Aiko, MacWhisper), set `pricing_url: null`
- For brands without Twitter (some privacy tools), set `twitter_handle: null`
- The `.env` file is in the parent directory (`/Users/davemooney/_dev/marketingCopy/.env`)

#### When Done
1. Verify all acceptance criteria pass
2. Commit with message: `swarm(wp-01): Project scaffolding & brand database`
3. Push: `git push origin swarm/wp-01-scaffolding`
4. Report: "WP-01 COMPLETE — branch pushed"

#### Do NOT
- Touch files outside your ownership list
- Merge your branch into any other branch
- Start work on any other WP
- Fetch landing page content (that's WP-02's job)
- Scrape App Store listings (that's WP-03's job)

---

### Agent Executor — WP-04: Google Ads & Search Copy Collector

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-04-google-ads`
**Wave:** 1 of 6
**GitHub Issue:** #4

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-04-google-ads`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Search competitive keywords via Brave Search API to capture visible Google Ads copy and organic results from competitors, saving structured results to `raw/ads/google_ads.json`.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `raw/ads/google_ads.json` | Create — all search ad copy results |

**Files you must NOT touch:** Everything not listed above.

#### Tasks
- [ ] Create `raw/ads/` directory if it doesn't exist
- [ ] Execute Brave API searches for these keywords:
  1. "meeting transcription app"
  2. "AI meeting notes"
  3. "transcription software"
  4. "meeting recorder"
  5. "voice to text app"
  6. "best meeting transcription"
  7. "automatic meeting notes"
  8. "transcription tool for meetings"
- [ ] For each search result, identify:
  - Any paid/sponsored ad results (headline, description, display URL)
  - Organic results from these known brands: Granola, Otter.ai, Fireflies.ai, Notta, Sonix, Fathom, tl;dv, Krisp, Tactiq, Read.ai, Supernormal, Aiko, MacWhisper
- [ ] If results are thin (<10 total ad elements), expand with additional keywords: "AI notetaker", "meeting summary tool", "real-time transcription", "speech to text app mac"
- [ ] Save all results to `raw/ads/google_ads.json`

#### Output Format
```json
{
  "source": "google_ads_via_brave",
  "fetched_at": "2026-03-18T...",
  "searches": [
    {
      "keyword": "meeting transcription app",
      "ads_found": [
        {
          "brand": "Otter.ai",
          "headlines": ["..."],
          "description": "...",
          "display_url": "otter.ai"
        }
      ],
      "organic_census_brands": [
        {
          "brand": "Fireflies.ai",
          "title": "...",
          "meta_description": "..."
        }
      ]
    }
  ],
  "summary": {
    "total_searches": 8,
    "total_ads_found": 0,
    "total_organic_brand_matches": 0,
    "brands_found_in_ads": [],
    "brands_found_in_organic": []
  }
}
```

#### Acceptance Criteria
- [ ] All 8+ keyword searches executed
- [ ] Any paid ad copy found is captured with brand attribution where identifiable
- [ ] Organic results for known competitor brands are noted
- [ ] Output is valid JSON saved to `raw/ads/google_ads.json`
- [ ] Summary section includes totals and brand lists
- [ ] If zero ads found, the result is still valid with `"ads_found": []` — document the null finding

#### Implementation Notes
- Brave Search API endpoint: `https://api.search.brave.com/res/v1/web/search?q={query}`
- API key: Use `BRAVE_API_KEY` from `.env` file at `/Users/davemooney/_dev/marketingCopy/.env`
- Header: `X-Subscription-Token: {BRAVE_API_KEY}`
- Brave may not surface Google Ads directly — capture whatever ad/sponsored content appears
- Also try Tavily as a supplement if Brave results are thin: `TAVILY_API_KEY` from `.env`
- Match ads to known brands by checking display URLs against known domains
- Add 1-2 second delay between API calls to be polite

#### When Done
1. Verify `raw/ads/google_ads.json` is valid JSON
2. Commit with message: `swarm(wp-04): Google Ads & search copy collector`
3. Push: `git push origin swarm/wp-04-google-ads`
4. Report: "WP-04 COMPLETE — branch pushed. Found [N] ad elements across [N] keywords."

#### Do NOT
- Touch files outside your ownership list
- Merge your branch into any other branch
- Fetch landing pages or pricing pages (that's WP-02)
- Tag or analyse the collected copy (that's WP-06)

---

### Agent Executor — WP-05: Facebook Ad Library Collection (Manus Task)

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-05-facebook-ads`
**Wave:** 1 of 6 (async — may complete in any wave)
**GitHub Issue:** #5

#### IMPORTANT: This is a MANUS task, not a Claude Code task.

This prompt should be adapted and given to Manus (browser-based agent).

#### Manus Prompt

Go to https://www.facebook.com/ads/library

For each of these brands, search for their active ads:
1. Granola
2. Otter.ai
3. Fireflies.ai
4. Notta
5. Sonix
6. Fathom
7. tl;dv
8. Krisp
9. Tactiq
10. Read.ai
11. Supernormal
12. MacWhisper
13. Aiko

For each brand:
1. Search the brand name in the Ad Library
2. Filter: Active ads only
3. For the top 5 most recent ads per brand, extract:
   - Ad headline text
   - Ad body/description text
   - CTA button text
   - Ad format (image/video/carousel)
4. If no results for brand name, try searching their website URL instead

#### Output Format
Save to `raw/ads/facebook_ads.json`:
```json
{
  "source": "facebook_ad_library",
  "collected_by": "manus",
  "collected_at": "2026-03-18",
  "brands": [
    {
      "brand": "Granola",
      "search_query": "Granola",
      "ads_found": 3,
      "ads": [
        {
          "headline": "...",
          "body": "...",
          "cta": "Learn More",
          "format": "image",
          "status": "active"
        }
      ]
    }
  ],
  "summary": {
    "total_brands_searched": 13,
    "brands_with_ads": 0,
    "brands_without_ads": 0,
    "total_ads_collected": 0
  }
}
```

#### Acceptance Criteria
- [ ] All 13 brands searched
- [ ] Up to 5 active ads per brand extracted
- [ ] Brands with zero active ads listed with `"ads_found": 0`
- [ ] Output is valid JSON

#### When Done (for whoever handles the Manus output)
1. Place the file at `raw/ads/facebook_ads.json` in the repo
2. Commit with message: `swarm(wp-05): Facebook Ad Library collection via Manus`
3. Push: `git push origin swarm/wp-05-facebook-ads`

---

### Agent Executor — WP-02: Web Copy Scraper — Landing & Pricing Pages

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-02-web-scraper`
**Wave:** 2 of 6
**GitHub Issue:** #2

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-02-web-scraper`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Fetch homepage and pricing page HTML for all brands in `brands.json`, extract specific copy elements, and save structured JSON per brand.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `raw/{brand_slug}_landing.json` | Create — one per brand (~35-40 files) |
| `raw/{brand_slug}_pricing.json` | Create — one per brand with pricing URL (~20-30 files) |

**Files you must NOT touch:** `brands.json` (read-only), `raw/ads/*`, everything else.

#### Tasks

**For each brand in `brands.json`:**

- [ ] **Landing page extraction:**
  1. `web_fetch(brand.website)`
  2. Parse the HTML and extract:
     - `<title>` tag text
     - `<meta name="description">` content
     - `<meta property="og:description">` content
     - First `<h1>` text (hero headline)
     - Hero subheadline: first `<p>` or `<h2>` in the same section/container as the `<h1>`
     - All `<h2>` text content (section headlines / scroll narrative)
     - All CTA button text: `<button>` elements, `<a>` with class containing "btn", "cta", "button", or role="button"
     - Footer tagline (if identifiable)
  3. Save to `raw/{brand_slug}_landing.json`

- [ ] **Pricing page extraction** (if `pricing_url` exists and differs from `website`):
  1. `web_fetch(brand.pricing_url)`
  2. Extract:
     - First `<h1>` or `<h2>` (pricing headline)
     - Plan names (Free, Pro, Enterprise, etc.)
     - Plan one-liner descriptions
     - Feature list headlines per plan
     - CTA button text per plan
  3. Save to `raw/{brand_slug}_pricing.json`

- [ ] **Handle failures gracefully:**
  - If `web_fetch` returns empty/error: save a JSON with `"extraction_failed": true` and `"error": "reason"`
  - If page is JS-heavy SPA (empty `<h1>`, `<div id="root">` with no content): flag as `"js_heavy": true`
  - Add 1-2 second delay between requests

#### Output Format (Landing)
```json
{
  "brand": "Granola",
  "tier": "direct",
  "url": "https://granola.so",
  "fetched_at": "2026-03-18T...",
  "extraction_failed": false,
  "js_heavy": false,
  "elements": {
    "title": "...",
    "meta_description": "...",
    "og_description": "...",
    "h1": "...",
    "hero_subheadline": "...",
    "h2s": ["...", "..."],
    "ctas": ["Try Free", "Get Started"],
    "footer_tagline": null
  }
}
```

#### Output Format (Pricing)
```json
{
  "brand": "Granola",
  "url": "https://granola.so/pricing",
  "fetched_at": "2026-03-18T...",
  "extraction_failed": false,
  "elements": {
    "headline": "...",
    "plans": [
      {
        "name": "Free",
        "description": "...",
        "features_headline": "...",
        "cta": "Get Started"
      }
    ]
  }
}
```

#### Acceptance Criteria
- [ ] All brands with valid homepage URLs have `{brand_slug}_landing.json`
- [ ] All brands with valid pricing URLs have `{brand_slug}_pricing.json`
- [ ] Each JSON has all extractable fields; missing data is `null`, not omitted
- [ ] JS-heavy pages flagged with `"js_heavy": true`
- [ ] Failed extractions saved with `"extraction_failed": true` and error reason
- [ ] Summary log at end listing: total brands, successful extractions, failures, JS-heavy flags

#### Implementation Notes
- Read `brands.json` from repo root (it was created by WP-01 and merged in Wave 1)
- Use `web_fetch` for all HTTP fetching
- `brand_slug` = lowercase brand name, spaces replaced with hyphens, special chars removed (e.g., "Otter.ai" → "otter-ai", "tl;dv" → "tldv", "Read.ai" → "read-ai")
- If a brand's pricing URL is the same as their homepage, skip pricing extraction (already covered)

#### When Done
1. Count files: `ls raw/*_landing.json | wc -l` and `ls raw/*_pricing.json | wc -l`
2. Verify a sample of 3 JSON files are valid and contain real copy text
3. Commit with message: `swarm(wp-02): Web copy scraper — landing & pricing pages`
4. Push: `git push origin swarm/wp-02-web-scraper`
5. Report: "WP-02 COMPLETE — [N] landing pages, [M] pricing pages extracted. [K] failed/JS-heavy."

#### Do NOT
- Touch `brands.json` (read-only)
- Touch `raw/ads/*` (owned by WP-04 and WP-05)
- Tag or analyse extracted copy (that's WP-06)
- Modify directory structure

---

### Agent Executor — WP-03: App Store Listing & Social Bio Collector

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-03-appstore-social`
**Wave:** 2 of 6
**GitHub Issue:** #3

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-03-appstore-social`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Collect App Store listings via iTunes Search API and social bios from Twitter/X profiles for all brands in `brands.json`.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `raw/{brand_slug}_appstore.json` | Create — one per brand with App Store presence |
| `raw/{brand_slug}_social.json` | Create — one per brand with Twitter presence |

**Files you must NOT touch:** `brands.json` (read-only), `raw/*_landing.json`, `raw/*_pricing.json`, `raw/ads/*`, everything else.

#### Tasks

**App Store Collection — for each brand with `appstore_search` in brands.json:**
- [ ] Call iTunes Search API:
  ```
  https://itunes.apple.com/search?term={appstore_search}&entity=macSoftware&limit=5
  ```
  Also try iOS: `entity=software`
- [ ] Match the correct app from results (by brand name in `trackName` or `sellerName`)
- [ ] Extract: `trackName`, `subtitle` (if present), `description` (first 500 characters)
- [ ] Save to `raw/{brand_slug}_appstore.json`

**Social Bio Collection — for each brand with `twitter_handle` in brands.json:**
- [ ] Try `web_fetch("https://nitter.net/{handle}")` first
- [ ] If Nitter fails, try alternative Nitter instances: `nitter.poast.org`, `nitter.privacydev.net`
- [ ] If all Nitter instances fail, try Brave search for "{brand name} twitter bio"
- [ ] Extract bio text
- [ ] Save to `raw/{brand_slug}_social.json`

#### Output Format (App Store)
```json
{
  "brand": "Granola",
  "source": "appstore",
  "platform": "macOS",
  "fetched_at": "2026-03-18T...",
  "found": true,
  "trackName": "Granola - AI Meeting Notes",
  "subtitle": "The AI notepad for meetings",
  "description_first_500": "..."
}
```

#### Output Format (Social)
```json
{
  "brand": "Granola",
  "source": "twitter",
  "handle": "granaborlabs",
  "fetched_at": "2026-03-18T...",
  "found": true,
  "bio_text": "The AI notepad for people in back-to-back meetings."
}
```

#### Acceptance Criteria
- [ ] All brands with `appstore_search` have `{brand_slug}_appstore.json` (with `"found": true/false`)
- [ ] Both macOS and iOS searches attempted; best match used
- [ ] `subtitle` field is `null` (not omitted) when unavailable
- [ ] All brands with `twitter_handle` have `{brand_slug}_social.json` (with `"found": true/false`)
- [ ] Summary log: brands processed, App Store hits/misses, social bio hits/misses

#### Implementation Notes
- iTunes API is free, no auth needed
- If `appstore_search` returns ambiguous results (e.g., "otter" returns many apps), match on the brand's known domain or seller name
- For brands without `appstore_search` or `twitter_handle` (null values), skip gracefully
- Nitter instances go down frequently — have 3+ fallbacks ready
- `brand_slug` convention: lowercase, hyphens for spaces, strip special chars

#### When Done
1. Count: `ls raw/*_appstore.json | wc -l` and `ls raw/*_social.json | wc -l`
2. Verify sample JSON files contain real data
3. Commit with message: `swarm(wp-03): App Store listing & social bio collector`
4. Push: `git push origin swarm/wp-03-appstore-social`
5. Report: "WP-03 COMPLETE — [N] App Store listings, [M] social bios collected."

#### Do NOT
- Touch `brands.json` (read-only)
- Touch `raw/*_landing.json` or `raw/*_pricing.json` (WP-02 owns those)
- Touch `raw/ads/*` (WP-04/05 own those)
- Analyse or tag any collected data

---

### Agent Executor — WP-06: Copy Tagging Engine

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-06-tagging`
**Wave:** 3 of 6
**GitHub Issue:** #6

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-06-tagging`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Load all raw extracted copy from `raw/`, flatten into individual elements, batch-tag each element against the full schema, and output a unified `data/tagged-copy.json` with 150-200 tagged elements.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `data/tagged-copy.json` | Create — the unified tagged dataset |

**Files you must NOT touch:** Everything in `raw/` (read-only), `brands.json` (read-only), everything else.

#### Tasks

**Step 1: Ingest all raw data**
- [ ] Load all `raw/{brand}_landing.json` files
- [ ] Load all `raw/{brand}_pricing.json` files
- [ ] Load all `raw/{brand}_appstore.json` files
- [ ] Load all `raw/{brand}_social.json` files
- [ ] Load `raw/ads/google_ads.json`
- [ ] Load `raw/ads/facebook_ads.json` (if it exists — soft dependency, proceed without it)
- [ ] Flatten into individual copy elements: each distinct text string becomes one element
- [ ] Skip any elements where text is null, empty, or extraction failed
- [ ] Log: total elements found, by source type, by brand

**Step 2: Tag in batches**
- [ ] Group elements into batches of 10
- [ ] For each batch, tag against the full schema (see below)
- [ ] Include 3 pre-tagged calibration examples in each prompt for consistency
- [ ] Validate each response is valid JSON with all schema fields
- [ ] Retry any batch that fails validation (up to 2 retries)
- [ ] Assign sequential IDs: `copy_001`, `copy_002`, etc.

**Step 3: Assemble and save**
- [ ] Combine all tagged elements into a single JSON array
- [ ] Save to `data/tagged-copy.json`
- [ ] Generate summary statistics

#### Tagging Schema
Each element gets tagged with this full schema:
```json
{
  "id": "copy_001",
  "brand": "string",
  "tier": "direct_competitor | adjacent_productivity | privacy_security",
  "source_type": "landing_h1 | landing_h2 | landing_sub | meta_desc | appstore_title | appstore_subtitle | appstore_desc | pricing_headline | cta_button | social_bio | ad_headline | ad_body",
  "url": "string",
  "text": "string",
  "word_count": 0,
  "structure": {
    "pattern": "the_X_for_Y | verb_command | question | plain_statement | metaphor | social_proof | statistic | list",
    "opens_with": "article | verb | pronoun | noun | question | number | brand_name",
    "mentions_product_category": false,
    "category_words_used": [],
    "mentions_audience": false,
    "audience_referenced": ""
  },
  "appeal": {
    "primary": "productivity | privacy | convenience | intelligence | simplicity | power | cost | trust | speed | craft",
    "framing": "feature | benefit | outcome | identity | problem | contrast",
    "specificity": "generic | segment_specific | use_case_specific"
  },
  "tone": {
    "register": "corporate | startup | confident | casual | technical | aspirational | editorial | minimal | warm | urgent | mysterious",
    "energy": "high | medium | low | calm",
    "personality": "authoritative | friendly | playful | serious | understated | matter_of_fact | bold"
  },
  "language_flags": {
    "uses_AI_language": false,
    "ai_words_used": [],
    "uses_superlative": false,
    "superlatives_used": [],
    "uses_jargon": false,
    "uses_metaphor": false,
    "uses_numbers": false,
    "cliche_phrases": [],
    "power_words": []
  },
  "privacy_position": {
    "mentions_privacy": false,
    "where_mentioned": "headline | subheadline | section_header | feature_bullet | footer | pricing | absent",
    "privacy_language_used": []
  }
}
```

#### Overused Phrases Watchlist — flag these in `cliche_phrases`:
"AI-powered", "Never miss a detail", "Never miss a moment", "Automatic meeting notes", "Your AI assistant", "Your AI companion", "Powered by AI", "Revolutionize your meetings", "Transform your meetings", "All-in-one", "Seamlessly", "Effortlessly", "Supercharge your productivity", "10x your", "The future of", "Built for teams", "Stay focused", "Stay present", "Capture every word", "Smart notes", "Trusted by", "Join [X] professionals", "Try free", "Get started free", "No credit card required", "Works where you work"

#### Calibration Examples (include in every batch prompt)
```
Example 1:
  Brand: Granola | Source: landing_h1 | Text: "The AI notepad for people in back-to-back meetings"
  → pattern: the_X_for_Y, opens_with: article, appeal: productivity/benefit/segment_specific
    tone: confident/medium/matter_of_fact, uses_AI_language: true ["AI"]

Example 2:
  Brand: Signal | Source: landing_h1 | Text: "Speak Freely"
  → pattern: verb_command, opens_with: verb, appeal: privacy/outcome/generic
    tone: minimal/calm/understated, privacy: mentions_privacy: true (implicit)

Example 3:
  Brand: Otter.ai | Source: cta_button | Text: "Try Otter for Free"
  → pattern: verb_command, opens_with: verb, appeal: convenience/feature/generic
    tone: startup/medium/friendly, cliche_phrases: ["Try free"]
```

#### Acceptance Criteria
- [ ] `data/tagged-copy.json` is valid JSON containing an array of tagged elements
- [ ] Minimum 150 elements tagged (flag to human if fewer than 120 available)
- [ ] Every element has ALL schema fields — no missing keys
- [ ] `cliche_phrases` populated where watchlist matches found
- [ ] Summary stats logged: total tagged, by tier breakdown, by source_type breakdown, by brand count
- [ ] At least 3 tiers represented in the data

#### Implementation Notes
- Use Claude (yourself) to do the tagging — read each batch of raw copy, apply the schema, output JSON
- Process in batches of 10 for efficiency
- If a text string is very short (e.g., a CTA button "Try Free"), still tag it fully
- Deduplicate: if the same text appears as both `meta_description` and `og_description` for the same brand, tag both but note similarity

#### When Done
1. Validate: `python3 -c "import json; d=json.load(open('data/tagged-copy.json')); print(f'{len(d)} elements tagged')"`
2. Commit with message: `swarm(wp-06): Copy tagging engine — {N} elements tagged`
3. Push: `git push origin swarm/wp-06-tagging`
4. Report: "WP-06 COMPLETE — [N] elements tagged. Breakdown: [N] direct, [N] adjacent, [N] privacy."

#### Do NOT
- Modify any files in `raw/` (read-only input)
- Analyse or draw conclusions from the tags (that's WP-07)
- Generate copy (that's WP-08)
- Touch any files outside `data/tagged-copy.json`

---

### Agent Executor — WP-07: Structural Map Analysis

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-07-structural-map`
**Wave:** 4 of 6
**GitHub Issue:** #7

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-07-structural-map`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Analyse `data/tagged-copy.json` to produce a comprehensive structural map that quantifies messaging patterns, identifies saturated territories, and pinpoints whitespace opportunities for Capsule.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `analysis/COPY-STRUCTURAL-MAP.md` | Create — the master whitespace analysis document |

**Files you must NOT touch:** `data/tagged-copy.json` (read-only), everything in `raw/`, everything else.

#### Tasks

Load `data/tagged-copy.json` and produce `analysis/COPY-STRUCTURAL-MAP.md` answering ALL 8 sections below. Every claim must cite specific data (counts and percentages with N).

- [ ] **Section 1: HEADLINE PATTERN DISTRIBUTION**
  - % using "The X for Y" structure
  - % using verb commands, questions, plain statements, metaphors, statistics/social proof
  - Most common opening word distribution
  - Top 10 headline structures with specific examples from the dataset
  - **HEADLINE WHITESPACE** — what patterns nobody is using

- [ ] **Section 2: APPEAL TYPE DISTRIBUTION**
  - % leading with features vs. benefits vs. outcomes vs. identity
  - % leading with productivity, privacy, convenience, cost, etc.
  - % generic vs. segment-specific vs. use-case-specific
  - **APPEAL WHITESPACE** — what appeal types are untouched

- [ ] **Section 3: TONE DISTRIBUTION**
  - % corporate vs. startup vs. confident vs. casual vs. minimal
  - % high-energy vs. calm
  - % authoritative vs. friendly vs. understated
  - **TONE WHITESPACE** — what tones nobody uses

- [ ] **Section 4: LANGUAGE SATURATION**
  - % mentioning "AI" in headlines
  - % using superlatives
  - Top 20 most repeated words across headlines
  - Top 10 most repeated phrases across all copy
  - Complete confirmed saturated phrases list
  - **LANGUAGE WHITESPACE** — what words/phrases nobody uses

- [ ] **Section 5: PRIVACY POSITIONING**
  - % mentioning privacy in H1, H2, section headers, feature bullets, or not at all
  - Specific privacy words used
  - **Key analysis: How do privacy-first brands (Signal, Proton, Mullvad) talk about privacy differently from transcription tools?**

- [ ] **Section 6: PRICING PAGE PATTERNS**
  - How competitors frame the money conversation
  - % leading with "Free" vs. feature comparison vs. value proposition
  - Dominant CTA language
  - **PRICING WHITESPACE**

- [ ] **Section 7: APP STORE PATTERNS**
  - % of titles containing "AI"
  - % of subtitles describing category literally
  - First-line patterns before "Read More"
  - **APP STORE WHITESPACE**

- [ ] **Section 8: THE WHITESPACE SUMMARY**
  - Top 5 SATURATED territories with specific examples from data
  - Top 5 EMPTY territories
  - How Capsule's positioning (privacy-first, local-first, cost-transparent, dark glass aesthetic) maps to whitespace
  - Specific phrases/structures Capsule SHOULD use
  - Specific phrases/structures Capsule must NEVER use
  - For each whitespace gap: "Why might this gap exist?" (honest assessment)

#### Capsule Brand DNA (reference for Section 8)
| Element | Value |
|---------|-------|
| Core positioning | "The transcription app that never sees your audio" |
| Primary attack | Cost transparency — exposing competitor markup |
| Secondary attack | Bot-free capture — invisible to meeting participants |
| Emotional territory | Quiet confidence, not corporate hype |
| Visual language | Dark glass / liquid metal aesthetic |
| Target segments | Journalists, researchers, privacy-conscious professionals, ADHD power users |
| Price anchors | Free local forever, Pro €9.99/mo, credits at cost+10% |
| Brand personality | The product that doesn't shout. Competence shown, not claimed. |

#### Acceptance Criteria
- [ ] All 8 sections completed with quantitative data
- [ ] Every percentage includes the raw count (e.g., "43% (3 of 7)")
- [ ] Findings with <10 data points flagged as "indicative, not conclusive"
- [ ] At least 5 saturated territories identified with data evidence
- [ ] At least 5 whitespace territories identified with data evidence
- [ ] Capsule's positioning explicitly mapped to identified whitespace
- [ ] Cross-tier analysis included (direct competitors vs. privacy brands vs. adjacent tools)
- [ ] "Use this" / "Never use this" recommendations are specific and actionable
- [ ] Output saved to `analysis/COPY-STRUCTURAL-MAP.md`

#### Implementation Notes
- Report findings BOTH overall AND by tier — Tier 1 (direct competitors) matters most
- Always cite specific copy examples alongside statistics
- Actively look for data that CONTRADICTS the hypothesised whitespace — be honest, not confirmatory
- For small categories, use "N of M" format rather than misleading percentages

#### When Done
1. Verify document has all 8 sections with data
2. Commit with message: `swarm(wp-07): Structural map analysis — whitespace territories identified`
3. Push: `git push origin swarm/wp-07-structural-map`
4. Report: "WP-07 COMPLETE. Key findings: [top 3 whitespace territories]. [N] saturated, [N] empty territories identified."

#### Do NOT
- Modify `data/tagged-copy.json` (read-only)
- Generate copy or briefs (that's WP-08)
- Touch any files outside `analysis/COPY-STRUCTURAL-MAP.md`
- Inject opinions not grounded in the census data

---

### Agent Executor — WP-08: Copy Generation Brief & All Channel Outputs

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-08-copy-generation`
**Wave:** 5 of 6
**GitHub Issue:** #8

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-08-copy-generation`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Synthesise the structural map with Capsule's brand DNA to produce a copy brief, then generate all deliverable outputs: HTML page, raw copy document, and video scripts.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `analysis/COPY-BRIEF.md` | Create — voice rules, anti-patterns, channel briefs |
| `output/copy-system.html` | Create — comprehensive HTML page for Figma import |
| `output/COPY-SYSTEM.md` | Create — all copy variants in markdown |
| `output/VIDEO-SCRIPTS.md` | Create — 15s, 30s, 60s storyboard scripts |

**Files you must NOT touch:** `analysis/COPY-STRUCTURAL-MAP.md` (read-only), `data/*` (read-only), `raw/*` (read-only), everything else.

#### Tasks

**Part A — Copy Brief (`analysis/COPY-BRIEF.md`)**
- [ ] Read `analysis/COPY-STRUCTURAL-MAP.md` thoroughly
- [ ] Cross-reference with Capsule brand DNA (below)
- [ ] Write **Voice Rules** derived from census whitespace — each rule cites the data that supports it
- [ ] Write **Anti-Pattern List** — confirmed saturated phrases with competitor counts, confirmed overused structures with usage %
- [ ] Write **Channel-Specific Briefs** for each channel:
  - Landing Page H1: whitespace target, max 10 words, generate 10 options
  - Landing Page Scroll Narrative: 6 section headlines in narrative order
  - App Store Title + Subtitle: 30-char constraints, 5 options
  - Pricing Page: headline + plan descriptions
  - Ad Headlines: 15-char and 30-char variants, 10 options per length
  - Social Bio: 160-char max, 5 options

**Part B — HTML Copy System Page (`output/copy-system.html`)**
- [ ] Create single comprehensive HTML page with 7 sections:
  1. **Landing Page Hero Options** — 3-5 hero layouts at 1440×900 with H1, subheadline, CTA
  2. **Landing Page Scroll Sections** — 6-8 section headline + body pairs
  3. **App Store Listing Preview** — 3 variants side by side (icon placeholder, title, subtitle, description)
  4. **Pricing Page** — full section with headline, plan cards (Free/Pro), prices, CTAs, markup comparison table
  5. **Ad Card Variants** — FB feed (1200×628), IG story (1080×1920), Google search text preview
  6. **Social Headers & Bios** — Twitter profile mockup, OG share card
  7. **Video Ad Text Overlays** — storyboard frames with text and timing
- [ ] Use Capsule's aesthetic: dark backgrounds (#0a0a0a to #1a1a1a), glass effects (backdrop-filter where possible, with solid fallbacks), subtle gradients, sans-serif typography
- [ ] Page must be servable via `python3 -m http.server 3000`

**Part C — Raw Copy Document (`output/COPY-SYSTEM.md`)**
- [ ] All copy variants organised by channel
- [ ] Character counts included for constrained copy (App Store, ads, social)
- [ ] Each variant annotated with which whitespace gap it targets
- [ ] Ranked by whitespace differentiation strength

**Part D — Video Scripts (`output/VIDEO-SCRIPTS.md`)**
- [ ] 15-second spot (4-5 frames): `[Timing] Text: "..." | Visual: [description]`
- [ ] 30-second spot (6-8 frames)
- [ ] 60-second spot (10-15 frames)
- [ ] Keep visual descriptions achievable with screen recordings + text overlays (no cinematic production)

#### Capsule Brand DNA
| Element | Value |
|---------|-------|
| Core positioning | "The transcription app that never sees your audio" |
| Primary attack | Cost transparency — exposing competitor markup |
| Secondary attack | Bot-free capture — invisible to meeting participants |
| Emotional territory | Quiet confidence, not corporate hype |
| Visual language | Dark glass / liquid metal aesthetic |
| Target segments | Journalists, researchers, privacy-conscious professionals, ADHD power users |
| Price anchors | Free local forever, Pro €9.99/mo, credits at cost+10% |
| Brand personality | The product that doesn't shout. Competence shown, not claimed. |
| Copy tone | Must feel like the app looks. Dark glass, not bright bubbly corporate. |

#### Acceptance Criteria
- [ ] `COPY-BRIEF.md` has voice rules, anti-patterns, and channel briefs — all citing census data
- [ ] `copy-system.html` renders in browser with all 7 sections visible and styled
- [ ] HTML uses dark aesthetic — no bright/white corporate styling
- [ ] `COPY-SYSTEM.md` has variants for all channels with character counts
- [ ] ALL generated headlines are structurally different from competitor H1s in the census
- [ ] NO copy uses any phrase from the confirmed saturated list
- [ ] `VIDEO-SCRIPTS.md` has 15s, 30s, 60s scripts with frame breakdowns
- [ ] Every piece of copy passes a "can a stranger tell what this product does?" clarity test

#### Implementation Notes
- Generate 3-5x more variants than needed, then curate down to the best
- For the HTML page, use self-contained CSS (no external dependencies)
- Include CSS `@media print` or at minimum ensure the page is screenshot-friendly
- The anti-pattern list from the brief should be cross-checked against every generated copy line

#### When Done
1. Open `output/copy-system.html` in browser, verify all sections render
2. Spot-check 5 headlines against the anti-pattern list
3. Verify character counts on constrained copy
4. Commit with message: `swarm(wp-08): Copy generation brief & all channel outputs`
5. Push: `git push origin swarm/wp-08-copy-generation`
6. Report: "WP-08 COMPLETE — Brief generated, [N] H1 variants, HTML system page with 7 sections, video scripts for 3 spots."

#### Do NOT
- Modify the structural map (read-only)
- Create test materials (that's WP-09)
- Use any phrase from the saturated list
- Touch files outside your ownership list

---

### Agent Executor — WP-09: Adversarial Kill Test Materials & Protocol

#### Context
**Project:** Quiet Thunder (Marketing Copy Census)
**Branch:** `swarm/wp-09-kill-test`
**Wave:** 6 of 6
**GitHub Issue:** #9

#### CRITICAL: Branch First
Before writing ANY code:
1. `git checkout swarm/wp-09-kill-test`
2. Confirm you are on the correct branch: `git branch --show-current`
3. If the branch doesn't exist, STOP and report to human

#### Your Task

**Objective:** Create all materials for the 5-human adversarial kill test: anonymised comparison cards, App Store card mockups, ad mockups in simulated feed, test protocol, and results template.

**Files you OWN (only touch these):**
| File | Action |
|------|--------|
| `test/comparison-cards/*.html` | Create — 3-5 anonymised A/B hero comparison cards |
| `test/appstore-cards/*.html` | Create — 3-4 anonymised App Store card displays |
| `test/ad-mockups/*.html` | Create — 3-4 ad mockups in simulated social feed |
| `test/TEST-PROTOCOL.md` | Create — complete test protocol with questions and kill criteria |
| `test/test_results.md` | Create — pre-formatted results template |

**Files you must NOT touch:** Everything in `output/` (read-only), `analysis/` (read-only), `data/` (read-only), everything else.

#### Tasks

- [ ] **Read inputs:**
  - `output/COPY-SYSTEM.md` — to get Capsule's best copy variants
  - `data/tagged-copy.json` — to identify strongest competitor copy for comparison
  - `analysis/COPY-STRUCTURAL-MAP.md` — to identify which competitors have the best copy

- [ ] **Comparison Cards** (`test/comparison-cards/`):
  - Create 3-5 HTML files, each showing two hero sections side by side
  - One side: Capsule's copy (H1 + subheadline + CTA)
  - Other side: strongest competitor's copy
  - **Fully anonymised**: "Product A" vs "Product B", randomise which side is Capsule
  - Use neutral dark styling for both — NO brand-specific visuals
  - Each card tests a different Capsule H1 variant

- [ ] **App Store Cards** (`test/appstore-cards/`):
  - Create 3-4 HTML files showing App Store listing cards side by side
  - Include: grey icon placeholder, title, subtitle, first 3 lines of description
  - Capsule + 2-3 strongest competitors
  - Anonymised: no brand names or real icons

- [ ] **Ad Mockups** (`test/ad-mockups/`):
  - Create 3-4 HTML files simulating a social media feed scroll
  - Mix of Capsule ads and competitor ads
  - Facebook feed format (1200×628 cards with headline, body, CTA)
  - Create 2-3 ordering variants to counter position bias

- [ ] **Test Protocol** (`test/TEST-PROTOCOL.md`):
  Write the complete protocol including:
  - Tester recruitment criteria (journalists, researchers, privacy-conscious professionals, ADHD power users)
  - Test setup instructions
  - All 8 questions with their measurement goals
  - Kill criteria (non-negotiable)
  - Timing guidance

- [ ] **Results Template** (`test/test_results.md`):
  - Pre-formatted grid: rows = questions, columns = 5 testers
  - Aggregate score section
  - Kill/survive decision section per copy variant
  - Notes field for qualitative feedback

#### Questions & Kill Criteria (embed in protocol)

| # | Material | Question | Measures | Kill If |
|---|----------|----------|----------|---------|
| 1 | Comparison | "Which costs more?" | Premium perception | Capsule loses |
| 2 | Comparison | "Which would you trust with confidential recording?" | Trust | Capsule loses |
| 3 | Comparison | "What does Product A do? Product B?" | Clarity | Can't describe Capsule |
| 4 | Comparison | "Which would you click?" | Engagement | Capsule loses consistently |
| 5 | App Store | "Which would you download first?" | Conversion | <3 of 5 pick Capsule |
| 6 | App Store | "Which description are you most curious about?" | Hook | <3 of 5 pick Capsule |
| 7 | Ads | "Would you stop scrolling?" | Thumb-stop | Nobody stops for Capsule |
| 8 | Ads | "Does this feel like every other app ad?" | Differentiation | "Yes" for Capsule |

#### Acceptance Criteria
- [ ] 3-5 comparison card HTML files in `test/comparison-cards/`
- [ ] 3-4 App Store card HTML files in `test/appstore-cards/`
- [ ] 3-4 ad mockup HTML files in `test/ad-mockups/`
- [ ] All materials fully anonymised — zero brand leaks
- [ ] Neutral styling — no visual advantage to either product
- [ ] `TEST-PROTOCOL.md` contains all 8 questions, kill criteria, and setup instructions
- [ ] `test_results.md` is a ready-to-fill template
- [ ] Materials openable in browser and look realistic

#### Implementation Notes
- Use self-contained HTML/CSS (no external dependencies)
- Neutral dark theme for all materials (dark grey background, white text, no brand colours)
- Randomise Capsule's position (left/right, first/second) across different cards
- Keep mockups realistic — don't make them too polished

#### When Done
1. Open each HTML file in browser, verify rendering
2. Check for brand leaks (search for "Capsule" in all test/ files)
3. Commit with message: `swarm(wp-09): Adversarial kill test materials & protocol`
4. Push: `git push origin swarm/wp-09-kill-test`
5. Report: "WP-09 COMPLETE — [N] comparison cards, [N] App Store cards, [N] ad mockups, protocol and results template ready."

#### Do NOT
- Modify any files in `output/`, `analysis/`, or `data/` (read-only)
- Include real brand names or logos in test materials
- Actually run the test (requires humans)
- Touch files outside the `test/` directory

---

## 8. QUICK-START COMMANDS

```bash
# 0. Clone the repo (if not already)
cd /Users/davemooney/_dev/marketingCopy/quiet-thunder

# 1. Create Wave 1 branches
git checkout main
git checkout -b swarm/wp-01-scaffolding main && git checkout main
git checkout -b swarm/wp-04-google-ads main && git checkout main
git checkout -b swarm/wp-05-facebook-ads main && git checkout main

# 2. Launch Wave 1 agents (one terminal per agent)
# Agent 1: WP-01 scaffolding — paste WP-01 executor prompt
# Agent 2: WP-04 google ads — paste WP-04 executor prompt
# Agent 3: WP-05 facebook ads — give Manus prompt to Manus

# 3. After Wave 1 agents complete:
git checkout main
git merge --no-ff swarm/wp-01-scaffolding -m "swarm(wp-01): scaffolding"
git merge --no-ff swarm/wp-04-google-ads -m "swarm(wp-04): google ads"
# merge wp-05 if ready, otherwise proceed

# 4. Create + launch Wave 2
git checkout -b swarm/wp-02-web-scraper main && git checkout main
git checkout -b swarm/wp-03-appstore-social main && git checkout main
# Launch 2 agents with WP-02 and WP-03 prompts

# 5. Continue pattern for Waves 3-6 (one agent each)

# 6. After final wave, verify everything:
ls raw/*.json | wc -l
python3 -c "import json; print(len(json.load(open('data/tagged-copy.json'))))"
open output/copy-system.html
# Close all issues:
for i in $(seq 1 9); do gh issue close $i; done
```

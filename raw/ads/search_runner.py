#!/usr/bin/env python3
"""
WP-04: Search competitive keywords via Brave and Tavily APIs.
Captures ad copy and organic results from competitors in meeting transcription / AI notes space.
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

BRAVE_API_KEY = "BSAXzJR4kk0izRdPn7kspjiWL09lAPy"
TAVILY_API_KEY = "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"

KEYWORDS = [
    "meeting transcription app",
    "AI meeting notes",
    "transcription software",
    "meeting recorder",
    "voice to text app",
    "best meeting transcription",
    "automatic meeting notes",
    "transcription tool for meetings",
]

EXTRA_KEYWORDS = [
    "AI notetaker",
    "meeting summary tool",
    "real-time transcription",
    "speech to text app mac",
]

# Known brand domains to match
BRAND_DOMAINS = {
    "granola.so": "Granola",
    "granola.ai": "Granola",
    "otter.ai": "Otter.ai",
    "fireflies.ai": "Fireflies.ai",
    "notta.ai": "Notta",
    "sonix.ai": "Sonix",
    "fathom.video": "Fathom",
    "tldv.io": "tl;dv",
    "krisp.ai": "Krisp",
    "tactiq.io": "Tactiq",
    "read.ai": "Read.ai",
    "supernormal.com": "Supernormal",
    "aiko.app": "Aiko",
    "macwhisper.com": "MacWhisper",
    "goodsnooze.gumroad.com": "MacWhisper",
    # Secondary brands to note
    "obsidian.md": "Obsidian",
    "notion.so": "Notion",
    "notion.com": "Notion",
    "linear.app": "Linear",
    "arc.net": "Arc",
    "culturedcode.com": "Things 3",
    "craft.do": "Craft",
    "raycast.com": "Raycast",
    "1password.com": "1Password",
    "signal.org": "Signal",
    "protonmail.com": "ProtonMail",
    "proton.me": "ProtonMail",
    "mullvad.net": "Mullvad",
    "standardnotes.com": "Standard Notes",
    "tuta.com": "Tuta",
    "tutanota.com": "Tuta",
}


def match_brand(url):
    """Check if a URL belongs to a known brand."""
    if not url:
        return None
    url_lower = url.lower()
    for domain, brand in BRAND_DOMAINS.items():
        if domain in url_lower:
            return brand
    return None


def brave_search(query):
    """Search via Brave Search API."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_q}&count=20"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("Accept-Encoding", "identity")
    req.add_header("X-Subscription-Token", BRAVE_API_KEY)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data
    except Exception as e:
        print(f"  [Brave ERROR] {query}: {e}")
        return {"error": str(e)}


def tavily_search(query):
    """Search via Tavily Search API."""
    url = "https://api.tavily.com/search"
    payload = json.dumps({
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": False,
        "max_results": 20,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data
    except Exception as e:
        print(f"  [Tavily ERROR] {query}: {e}")
        return {"error": str(e)}


def extract_brave_results(keyword, data):
    """Extract ads and organic brand matches from Brave response."""
    ads_found = []
    organic_brands = []
    errors = []

    if "error" in data:
        errors.append(data["error"])
        return ads_found, organic_brands, errors

    # Check for sponsored/ad results
    # Brave may return ads in "ads" or "sponsored" fields
    for ad_key in ["ads", "sponsored"]:
        if ad_key in data and data[ad_key]:
            ad_results = data[ad_key].get("results", []) if isinstance(data[ad_key], dict) else data[ad_key]
            for ad in ad_results:
                ad_entry = {
                    "headline": ad.get("title", ""),
                    "description": ad.get("description", ""),
                    "display_url": ad.get("url", ""),
                    "brand": match_brand(ad.get("url", "")),
                }
                ads_found.append(ad_entry)

    # Check organic web results
    web_results = []
    if "web" in data and isinstance(data["web"], dict):
        web_results = data["web"].get("results", [])
    elif "results" in data:
        web_results = data["results"]

    for result in web_results:
        url = result.get("url", "")
        brand = match_brand(url)
        if brand:
            organic_brands.append({
                "brand": brand,
                "title": result.get("title", ""),
                "url": url,
                "description": result.get("description", ""),
            })

    return ads_found, organic_brands, errors


def extract_tavily_results(keyword, data):
    """Extract brand matches from Tavily response."""
    ads_found = []  # Tavily doesn't distinguish ads
    organic_brands = []
    errors = []

    if "error" in data:
        errors.append(data["error"])
        return ads_found, organic_brands, errors

    results = data.get("results", [])
    for result in results:
        url = result.get("url", "")
        brand = match_brand(url)
        if brand:
            organic_brands.append({
                "brand": brand,
                "title": result.get("title", ""),
                "url": url,
                "description": result.get("content", ""),
            })

    return ads_found, organic_brands, errors


def main():
    all_searches = []
    all_brands_in_ads = set()
    all_brands_in_organic = set()
    total_ads = 0
    total_organic = 0
    total_brand_mentions = 0

    # Start with primary keywords
    keywords_to_search = list(KEYWORDS)

    print(f"Starting searches at {datetime.now(timezone.utc).isoformat()}")
    print(f"Primary keywords: {len(keywords_to_search)}")

    for i, keyword in enumerate(keywords_to_search):
        print(f"\n[{i+1}/{len(keywords_to_search)}] Searching: '{keyword}'")

        # Brave search
        print(f"  -> Brave...")
        brave_data = brave_search(keyword)
        time.sleep(2)

        brave_ads, brave_organic, brave_errors = extract_brave_results(keyword, brave_data)

        search_entry_brave = {
            "keyword": keyword,
            "search_engine": "brave",
            "ads_found": brave_ads,
            "organic_census_brands": brave_organic,
        }
        if brave_errors:
            search_entry_brave["errors"] = brave_errors
        all_searches.append(search_entry_brave)

        total_ads += len(brave_ads)
        total_organic += len(brave_organic)
        for ad in brave_ads:
            if ad.get("brand"):
                all_brands_in_ads.add(ad["brand"])
        for org in brave_organic:
            all_brands_in_organic.add(org["brand"])

        print(f"     Brave: {len(brave_ads)} ads, {len(brave_organic)} brand matches")

        # Tavily search
        print(f"  -> Tavily...")
        tavily_data = tavily_search(keyword)
        time.sleep(2)

        tavily_ads, tavily_organic, tavily_errors = extract_tavily_results(keyword, tavily_data)

        search_entry_tavily = {
            "keyword": keyword,
            "search_engine": "tavily",
            "ads_found": tavily_ads,
            "organic_census_brands": tavily_organic,
        }
        if tavily_errors:
            search_entry_tavily["errors"] = tavily_errors
        all_searches.append(search_entry_tavily)

        total_ads += len(tavily_ads)
        total_organic += len(tavily_organic)
        for ad in tavily_ads:
            if ad.get("brand"):
                all_brands_in_ads.add(ad["brand"])
        for org in tavily_organic:
            all_brands_in_organic.add(org["brand"])

        print(f"     Tavily: {len(tavily_ads)} ads, {len(tavily_organic)} brand matches")

        total_brand_mentions += len(brave_organic) + len(tavily_organic)

    # Check if we need extra keywords (fewer than 10 brand mentions total)
    if total_brand_mentions < 10:
        print(f"\n--- Only {total_brand_mentions} brand mentions so far. Adding extra keywords. ---")
        keywords_to_search_extra = EXTRA_KEYWORDS
    else:
        print(f"\n--- {total_brand_mentions} brand mentions found. Skipping extra keywords. ---")
        keywords_to_search_extra = []

    for i, keyword in enumerate(keywords_to_search_extra):
        print(f"\n[EXTRA {i+1}/{len(keywords_to_search_extra)}] Searching: '{keyword}'")

        # Brave
        print(f"  -> Brave...")
        brave_data = brave_search(keyword)
        time.sleep(2)

        brave_ads, brave_organic, brave_errors = extract_brave_results(keyword, brave_data)
        search_entry_brave = {
            "keyword": keyword,
            "search_engine": "brave",
            "ads_found": brave_ads,
            "organic_census_brands": brave_organic,
        }
        if brave_errors:
            search_entry_brave["errors"] = brave_errors
        all_searches.append(search_entry_brave)
        total_ads += len(brave_ads)
        total_organic += len(brave_organic)
        for ad in brave_ads:
            if ad.get("brand"):
                all_brands_in_ads.add(ad["brand"])
        for org in brave_organic:
            all_brands_in_organic.add(org["brand"])
        print(f"     Brave: {len(brave_ads)} ads, {len(brave_organic)} brand matches")

        # Tavily
        print(f"  -> Tavily...")
        tavily_data = tavily_search(keyword)
        time.sleep(2)

        tavily_ads, tavily_organic, tavily_errors = extract_tavily_results(keyword, tavily_data)
        search_entry_tavily = {
            "keyword": keyword,
            "search_engine": "tavily",
            "ads_found": tavily_ads,
            "organic_census_brands": tavily_organic,
        }
        if tavily_errors:
            search_entry_tavily["errors"] = tavily_errors
        all_searches.append(search_entry_tavily)
        total_ads += len(tavily_ads)
        total_organic += len(tavily_organic)
        for ad in tavily_ads:
            if ad.get("brand"):
                all_brands_in_ads.add(ad["brand"])
        for org in tavily_organic:
            all_brands_in_organic.add(org["brand"])
        print(f"     Tavily: {len(tavily_ads)} ads, {len(tavily_organic)} brand matches")

    # Calculate total searches
    total_keywords = len(KEYWORDS) + len(keywords_to_search_extra)
    total_search_calls = total_keywords * 2  # brave + tavily for each

    # Build final output
    output = {
        "source": "search_ads_via_brave_and_tavily",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "searches": all_searches,
        "summary": {
            "total_keywords_searched": total_keywords,
            "total_search_api_calls": total_search_calls,
            "total_ads_found": total_ads,
            "total_organic_brand_matches": total_organic,
            "brands_found_in_ads": sorted(list(all_brands_in_ads)),
            "brands_found_in_organic": sorted(list(all_brands_in_organic)),
        },
    }

    output_path = "/Users/davemooney/_dev/marketingCopy/quiet-thunder/raw/ads/google_ads.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"DONE. Results saved to {output_path}")
    print(f"Total keywords searched: {total_keywords}")
    print(f"Total API calls: {total_search_calls}")
    print(f"Total ads found: {total_ads}")
    print(f"Total organic brand matches: {total_organic}")
    print(f"Brands in ads: {sorted(list(all_brands_in_ads))}")
    print(f"Brands in organic: {sorted(list(all_brands_in_organic))}")


if __name__ == "__main__":
    main()

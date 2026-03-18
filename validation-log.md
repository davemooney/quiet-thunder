# Brand Database Validation Log

**Date:** 2026-03-18
**Task:** WP-01 — Project scaffolding & brand database
**Validator:** Claude (automated)

---

## Summary

| Check Type | Pass | Fail | N/A |
|---|---|---|---|
| Homepage URL | 23 | 1 | 2 |
| Pricing URL | 19 | 2 | 5 |
| Twitter Handle | 26 | 0 | 0 |
| App Store Search | 18 | 6 | 2 |

---

## Tier 1 — Direct Competitors (13)

### 1. Granola
| Check | Result | Notes |
|---|---|---|
| Homepage (granola.so) | REDIRECT | 308 -> https://www.granola.ai/ |
| Pricing (granola.so/pricing) | REDIRECT | 308 -> https://www.granola.ai/pricing (loads OK) |
| Twitter (@meetgranola) | PASS | Found in footer of granola.ai |
| App Store ("granola meeting notes") | PASS | Top result: "Granola - AI Meeting Notes" |

### 2. Otter.ai
| Check | Result | Notes |
|---|---|---|
| Homepage (otter.ai) | PASS | Title: "Otter Meeting Agent - AI Notetaker, Transcription, Insights" |
| Pricing (otter.ai/pricing) | PASS | 4 tiers displayed |
| Twitter (@otter_ai) | PASS | Found in footer |
| App Store ("otter ai meeting") | PASS | Top result: "Otter Transcribe Voice Notes" |

### 3. Fireflies.ai
| Check | Result | Notes |
|---|---|---|
| Homepage (fireflies.ai) | PASS | Title: "Fireflies.ai | The #1 AI Notetaker" |
| Pricing (fireflies.ai/pricing) | PASS | 4 tiers displayed |
| Twitter (@firefliesai) | PASS | Found in footer |
| App Store ("fireflies ai") | PASS | Top result: "Fireflies: AI notetaker" |

### 4. Notta
| Check | Result | Notes |
|---|---|---|
| Homepage (notta.ai) | PASS | Page loads (title not extractable from CSS-heavy render) |
| Pricing (notta.ai/pricing) | PASS | Page loads with pricing elements |
| Twitter (@NottaOfficial) | PASS | Found via web search; confirmed on x.com |
| App Store ("notta transcription") | PASS | Top result: "Notta Transcribe Voice to Text" |

### 5. Sonix
| Check | Result | Notes |
|---|---|---|
| Homepage (sonix.ai) | PASS | Title: "Automatically convert audio to text | Sonix" |
| Pricing (sonix.ai/pricing) | PASS | 3 tiers displayed |
| Twitter (@trysonix) | PASS | Found in footer |
| App Store ("sonix transcription") | FAIL | No Sonix-branded result returned; Sonix may not have an iOS app |

### 6. Aiko
| Check | Result | Notes |
|---|---|---|
| Homepage | N/A | App Store only (developer page: sindresorhus.com/aiko) |
| Pricing | N/A | Priced on App Store |
| Twitter (@sindresorhus) | PASS | Developer's personal handle; found via web search |
| App Store ("aiko transcription") | PASS | Top result: "Aiko" |

### 7. MacWhisper
| Check | Result | Notes |
|---|---|---|
| Homepage (goodsnooze.gumroad.com) | PASS | Loads; shows Jordi Bruin's Gumroad page |
| Pricing | N/A | Sold via Gumroad/App Store; no dedicated pricing page |
| Twitter (@jordibruin) | PASS | Developer's personal handle; found via web search |
| App Store ("macwhisper") | PASS | Top result: "Macwhisper - Text To Speech" |

### 8. Fathom
| Check | Result | Notes |
|---|---|---|
| Homepage (fathom.video) | REDIRECT | 301 -> https://fathom.ai/ (loads OK) |
| Pricing (fathom.video/pricing) | REDIRECT | 301 -> https://fathom.ai/pricing (loads OK with 4 tiers) |
| Twitter (@FathomDotVideo) | PASS | Found via web search |
| App Store ("fathom meeting") | FAIL | No Fathom-branded result; may be desktop/web only |

### 9. tl;dv
| Check | Result | Notes |
|---|---|---|
| Homepage (tldv.io) | PASS | Title: "AI meeting notes you can actually use | tl;dv" |
| Pricing (tldv.io/pricing) | FAIL | Returns 404. Correct URL: tldv.io/app/pricing/ |
| Twitter (@tldview) | PASS | Found in footer |
| App Store ("tldv meeting") | FAIL | No tl;dv result returned |

### 10. Krisp
| Check | Result | Notes |
|---|---|---|
| Homepage (krisp.ai) | PASS | Title: "Voice AI for Meetings" |
| Pricing (krisp.ai/pricing) | PASS | Multiple product tiers displayed |
| Twitter (@krispHQ) | PASS | Found in footer |
| App Store ("krisp noise") | PASS | Result #2: "Krisp AI Meeting Note Taker" |

### 11. Tactiq
| Check | Result | Notes |
|---|---|---|
| Homepage (tactiq.io) | PASS | Title: "Tactiq.io - AI Meeting Transcripts" |
| Pricing (tactiq.io/pricing) | PASS | 5 tiers displayed |
| Twitter (@tactiqHQ) | PASS | Found in footer |
| App Store ("tactiq transcription") | FAIL | No Tactiq result; likely Chrome extension/web only |

### 12. Read.ai
| Check | Result | Notes |
|---|---|---|
| Homepage (read.ai) | PASS | Title: "Meeting Summaries, Transcripts, AI Notetaker" |
| Pricing (read.ai/pricing) | PASS | 4 tiers displayed |
| Twitter (@ReadAI_) | PASS | Found in footer |
| App Store ("read ai meeting") | FAIL | No Read.ai result; generic meeting apps returned |

### 13. Supernormal
| Check | Result | Notes |
|---|---|---|
| Homepage (supernormal.com) | FAIL | HTTP 403 (may require browser JS rendering) |
| Pricing (supernormal.com/pricing) | FAIL | HTTP 403 (confirmed exists via web search) |
| Twitter (@supernormalapp) | PASS | Found via web search |
| App Store ("supernormal meeting") | FAIL | No Supernormal result returned |

---

## Tier 2 — Adjacent Productivity (8)

### 14. Obsidian
| Check | Result | Notes |
|---|---|---|
| Homepage (obsidian.md) | PASS | Title: "Obsidian - Sharpen your thinking" |
| Pricing (obsidian.md/pricing) | PASS | Sync, Publish, Catalyst tiers |
| Twitter (@obsdmd) | PASS | Found in footer |
| App Store ("obsidian notes") | PASS | Top result: "Obsidian - Connected Notes" |

### 15. Notion
| Check | Result | Notes |
|---|---|---|
| Homepage (notion.so) | REDIRECT | 301 -> https://www.notion.com/ (loads OK) |
| Pricing (notion.so/pricing) | REDIRECT | 301 -> https://www.notion.com/pricing (loads OK) |
| Twitter (@NotionHQ) | PASS | Found in footer |
| App Store ("notion") | PASS | Top result: "Notion: Notes, Tasks, AI" |

### 16. Linear
| Check | Result | Notes |
|---|---|---|
| Homepage (linear.app) | PASS | Title: "Linear - The system for product development" |
| Pricing (linear.app/pricing) | PASS | 4 tiers displayed |
| Twitter (@linear) | PASS | Found via web search |
| App Store | N/A | No App Store search term specified (null) |

### 17. Arc
| Check | Result | Notes |
|---|---|---|
| Homepage (arc.net) | PASS | Title: "Arc from The Browser Company" |
| Pricing | N/A | Free product; no pricing page |
| Twitter (@arcinternet) | PASS | Found via web search; also @browsercompany |
| App Store ("arc browser") | PASS | Top result: "Arc Search - Find it, Faster" |

### 18. Things 3
| Check | Result | Notes |
|---|---|---|
| Homepage (culturedcode.com/things) | REDIRECT | 301 -> culturedcode.com/things/ (trailing slash, loads OK) |
| Pricing | N/A | App Store pricing only |
| Twitter (@culturedcode) | PASS | Found via web search |
| App Store ("things 3") | PASS | Top result: "Things 3" |

### 19. Craft
| Check | Result | Notes |
|---|---|---|
| Homepage (craft.do) | PASS | Title: "Craft - Docs and Notes Editor" |
| Pricing (craft.do/pricing) | PASS | 4 tiers displayed |
| Twitter (@craftdocs) | PASS | Found in footer |
| App Store ("craft docs") | PASS | Top result: "Craft: Notes, Documents, AI" |

### 20. Raycast
| Check | Result | Notes |
|---|---|---|
| Homepage (raycast.com) | PASS | Title: "Raycast - Your shortcut to everything" |
| Pricing (raycast.com/pricing) | PASS | 5 tiers displayed |
| Twitter (@raycast) | PASS | Found in footer |
| App Store ("raycast") | PASS | Top result: "Raycast: AI, Notes and more" |

### 21. 1Password
| Check | Result | Notes |
|---|---|---|
| Homepage (1password.com) | PASS | Title: "Passwords, Secrets, and Access Management" |
| Pricing (1password.com/pricing) | PASS | 4 tiers displayed |
| Twitter (@1Password) | PASS | Found in footer and via web search |
| App Store ("1password") | PASS | Top result: "1Password: Password Manager" |

---

## Tier 3 — Privacy/Security (5)

### 22. Signal
| Check | Result | Notes |
|---|---|---|
| Homepage (signal.org) | PASS | Title: "Signal >> Home" |
| Pricing | N/A | Free/donation-funded |
| Twitter (@signalapp) | PASS | Found in footer |
| App Store ("signal messenger") | PASS | Top result: "Signal - Private Messenger" |

### 23. ProtonMail
| Check | Result | Notes |
|---|---|---|
| Homepage (proton.me) | PASS | Title: "Proton: Privacy by default" |
| Pricing (proton.me/pricing) | PASS | Page loads; prices rendered via JS |
| Twitter (@ProtonPrivacy) | PASS | Found in footer |
| App Store ("proton mail") | PASS | Top result: "Proton Mail - Encrypted Email" |

### 24. Mullvad VPN
| Check | Result | Notes |
|---|---|---|
| Homepage (mullvad.net) | PASS | Title: "Mullvad VPN - Privacy is for the people" |
| Pricing (mullvad.net/pricing) | PASS | Flat rate displayed |
| Twitter (@mullvadnet) | PASS | Found in footer |
| App Store ("mullvad vpn") | PASS | Top result: "Mullvad VPN" |

### 25. Standard Notes
| Check | Result | Notes |
|---|---|---|
| Homepage (standardnotes.com) | PASS | Title: "Standard Notes | End-To-End Encrypted Notes App" |
| Pricing (standardnotes.com/plans) | PASS | Note: /pricing returns 404; correct URL is /plans |
| Twitter (@StandardNotes) | PASS | Found in footer |
| App Store ("standard notes") | PASS | Top result: "Standard Notes" |

### 26. Tuta
| Check | Result | Notes |
|---|---|---|
| Homepage (tuta.com) | PASS | Title: "Tuta: Turn ON privacy for free" |
| Pricing (tuta.com/pricing) | PASS | 3 tiers displayed |
| Twitter (@TutaPrivacy) | PASS | Found via web search; not linked from homepage (uses Mastodon/Bluesky) |
| App Store ("tuta mail") | PASS | Top result: "Tuta: Encrypted Private Email" |

---

## Known Issues & Action Items

1. **Granola domain migration**: granola.so -> granola.ai (308 permanent). Consider updating primary URLs.
2. **Fathom domain migration**: fathom.video -> fathom.ai (301). Consider updating primary URLs.
3. **Notion domain migration**: notion.so -> notion.com (301). Consider updating primary URLs.
4. **tl;dv pricing URL**: /pricing returns 404; actual pricing is at /app/pricing/.
5. **Standard Notes pricing URL**: /pricing returns 404; actual pricing is at /plans.
6. **Supernormal homepage**: Returns 403 (anti-bot protection). URL confirmed valid via web search.
7. **App Store misses**: Sonix, Fathom, tl;dv, Tactiq, Read.ai, and Supernormal did not return branded results in App Store search. These may be web/desktop-only or use different App Store names.
8. **Aiko & MacWhisper Twitter**: Using developer personal handles (Sindre Sorhus, Jordi Bruin) since these are indie apps without brand accounts.
9. **Tuta Twitter**: @TutaPrivacy exists on X but is not linked from their website (they prefer Mastodon/Bluesky).

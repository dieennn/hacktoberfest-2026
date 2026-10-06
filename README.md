# 🎃 Hacktoberfest 2026 — DEV Challenges Monorepo

> Repository containing project submissions for the **Hacktoberfest 2026 DEV Challenges** ("AI belongs to everyone").  
> Built by [@dieennn](https://github.com/dieennn).

---

## 📁 Repository Structure

| Round | Challenge Theme | Folder / Project | Status |
|---|---|---|---|
| **Launch Weekend** (Oct 2 - Oct 5) | Build for a Friend | [`00-weekend-allergy-guard`](./00-weekend-allergy-guard) | ✅ Completed |
| **Week 1** (Oct 5 - Oct 12) | Touch Grass | [`01-week-1`](./01-week-1) | ✅ Completed |
| **Week 2** (Oct 12 - Oct 19) | Announced Oct 12 | [`02-week-2`](./02-week-2) | ⏳ Upcoming |
| **Week 3** (Oct 19 - Oct 26) | Announced Oct 19 | [`03-week-3`](./03-week-3) | ⏳ Upcoming |
| **Week 4** (Oct 26 - Nov 1) | Announced Oct 26 | [`04-week-4`](./04-week-4) | ⏳ Upcoming |

---

## 🚀 Projects Overview

### [00-weekend-allergy-guard](./00-weekend-allergy-guard) — Allergy & Diet Guard (SafeBite AI)
- **Theme**: Build for a Friend
- **Problem**: Protect friend Sarah (severe peanut allergy, celiac disease, and lactose intolerance) from hidden allergens (*arachis oil*, *seitan*, *casein*) and cross-contamination when eating out.
- **Tech**: Local Python 3 standard library server (zero dependencies), open-source clinical allergen taxonomy, and local open-weight model integration (Ollama / Llama 3.2).
- **DEV Article**: See [SUBMISSION_DRAFT.md](./00-weekend-allergy-guard/SUBMISSION_DRAFT.md).

### [01-week-1](./01-week-1) — TrailFlora & Garden AI
- **Theme**: Touch Grass (Get people off screens and into the world)
- **Problem**: Screen addiction and digital fatigue keep people indoors. When outdoors or gardening, hikers lack reliable offline identification for toxic weeds (poison ivy, deadly nightshade) and autumn frost calendars.
- **Tech**: Pure Python standard library, offline botanical safety rule matrix, Google Gemma open-weight LLM bridge via Ollama, and high-contrast mobile outdoor UI.
- **DEV Article**: See [SUBMISSION_DRAFT.md](./01-week-1/SUBMISSION_DRAFT.md).

---

## 🚀 Unified Deployment (Render Free Tier)

All 5 challenge applications are unified under a single root gateway (`main.py`) to run permanently on Render's free tier without exceeding service hour limits.

- **Start Command**: `python main.py`
- **Root URL (`/`)**: Central Challenge Hub Portal
- **Weekend App (`/weekend/`)**: Allergy & Diet Guard App
- **Upcoming Apps (`/week-1/` ... `/week-4/`)**: Automatically routed as rounds unlock

---

## 📋 Hacktoberfest 2026 Roadmap
See [BACKLOG.md](./BACKLOG.md) for full tracking of all 24 virtual stickers and milestone progress.

## 📄 License
MIT License

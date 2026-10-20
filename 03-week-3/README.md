# 🦥 SlothDigest AI (Week 3: Slow and Steady)

> Hacktoberfest 2026 DEV Challenge — Week 3 Project  
> Theme: **Slow and Steady** (Built in honor of International Sloth Day, Oct 20 — Open-source AI that rewards healthy laziness)

---

## 📖 Overview

**SlothDigest AI** is a local-first, zero-dependency intelligence companion for developers and creators who are overwhelmed by digital noise, 500-message chat threads, and dreadful procrastinated tasks. It channels the wisdom of sloths: conserve energy, move deliberately, and automate the busywork.

### Core Modules
1. **💬 Chat & Thread Distiller:** Parses chaotic group chats, Slack channels, and long email chains. Filters out 90% conversational noise, highlights critical action items for you, calculates reading effort saved, and generates a 2-line summary.
2. **🌙 Sloth Mode & Ambient Brown Noise:** Prescribes offline decompression checklists for screen burnout and decision fatigue, complete with an in-browser Web Audio brown noise synthesizer that works with zero external files or network calls.
3. **⚡ 2-Minute Task Shrinker:** Breaks down dreaded chores ("file taxes", "clean 1,000 files", "refactor monolithic module") into an embarrassingly small, friction-free 2-minute starter step.

---

## 🛠️ Architecture

- **Runtime:** Python 3 Standard Library only (0 external pip dependencies).
- **AI Core:** Google Gemma open-weight model (`gemma2:2b`) with deterministic offline heuristic fallback.
- **Frontend:** Responsive, calming olive/dark-tone UI (`static/index.html`) featuring client-side Web Audio API ambient noise generator.
- **Unified Gateway:** Served through `../main.py` under `/week-3/`.

---

## 🚀 Running Standalone

```bash
cd 03-week-3
python app.py
# Open http://localhost:8083
```

Or run through the monorepo hub:
```bash
python main.py
# Open http://localhost:8080/week-3/
```

## 🧪 Testing

```bash
python test_engine.py
```

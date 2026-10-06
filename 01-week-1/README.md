# 🌱 TrailFlora & Garden AI (Week 1: Touch Grass)

> Hacktoberfest 2026 DEV Challenge — Week 1 Project  
> Theme: **Touch Grass** (Open-source AI that gets people off screens and into the wild)

---

## 📖 Overview

**TrailFlora & Garden AI** is an offline-first botanical companion and outdoor garden planner designed to break digital screen fatigue.

### Core Modules
1. **🌿 Trail Plant & Toxic Weed Sentinel:** Scans physical observations (leaves of three, berries, stems) to detect contact hazards (Poison Ivy, Poison Oak) and lethal plants (Deadly Nightshade).
2. **🥕 Backyard Garden & Frost Planner:** Calculates USDA hardiness zone planting schedules for autumn crops and alerts when cold dips require frost blankets.
3. **☀️ Outdoor Sunlight Scout:** Computes outdoor vitality and trail walking windows to reset circadian rhythm and eye strain.

---

## 🛠️ Architecture

- **Runtime:** Python 3 Standard Library only (0 external dependencies).
- **AI Core:** Google Gemma open-weight model (`gemma2:2b`) via local Ollama bridge, with instant deterministic offline fallback.
- **Frontend:** Responsive, high-contrast, outdoor-readable mobile UI (`static/index.html`).
- **Unified Gateway:** Served through `../main.py` under `/week-1/`.

---

## 🚀 Running Standalone

```bash
cd 01-week-1
python app.py
# Open http://localhost:8081
```

Or run through the monorepo hub:
```bash
python main.py
# Open http://localhost:8080/week-1/
```

## 🧪 Testing

```bash
python test_engine.py
```

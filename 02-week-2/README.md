# 💼 HustleLedger AI (Week 2: Side Hustle)

> Hacktoberfest 2026 DEV Challenge — Week 2 Project  
> Theme: **Side Hustle** (Practical open-source AI tools for freelancers, solopreneurs, and micro-agencies)

---

## 📖 Overview

**HustleLedger AI** is a local-first financial sentinel, tax write-off categorizer, and client communication defender built specifically for side hustlers who refuse to hand their private financial books or client details to expensive third-party cloud trackers.

### Core Modules
1. **🧾 Expense & Tax Shield:** Automatically classifies raw expense receipts against freelance tax deduction rules (Schedule C: software subscriptions, hardware, meals, utilities) and calculates estimated cash saved.
2. **📄 Instant Invoice Builder:** Compiles clean, verified client invoices with net-payment terms without bloated invoice SaaS fees.
3. **🛡️ Scope & Overdue Defender:** Bridges to Google Gemma open-weight AI via Ollama to generate polite yet firm overdue reminder emails and scope-creep boundaries.

---

## 🛠️ Architecture

- **Runtime:** Python 3 Standard Library only (0 pip dependencies).
- **AI Core:** Google Gemma open-weight model (`gemma2:2b`) with instant deterministic offline fallback.
- **Frontend:** Responsive, modern dark UI (`static/index.html`).
- **Unified Gateway:** Served through `../main.py` under `/week-2/`.

---

## 🚀 Running Standalone

```bash
cd 02-week-2
python app.py
# Open http://localhost:8082
```

Or run through the monorepo hub:
```bash
python main.py
# Open http://localhost:8080/week-2/
```

## 🧪 Testing

```bash
python test_engine.py
```

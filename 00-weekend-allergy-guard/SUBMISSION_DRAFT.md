---
title: Allergy & Diet Guard — Protecting My Friend with Local Open-Source AI
published: true
tags: devchallenge, weekendchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

---

## What I Built

I built **Allergy & Diet Guard (SafeBite)** for my friend **Sarah**, who lives with an unforgiving combination of dietary hazards:
- **Severe Peanut Allergy** (life-threatening anaphylactic shock)
- **Celiac Disease** (strict gluten-free requirement)
- **Lactose Intolerance** (no dairy)

Eating out at local restaurants, street food stalls, or night markets with Sarah is usually stressful. Menus and product labels rarely say *"Peanut"* or *"Wheat"*; they list obscure culinary terms like **"arachis oil"**, **"seitan"**, **"malt extract"**, **"casein"**, or **"modified starch"**. A single contaminated bite can mean an emergency hospital visit.

**Allergy & Diet Guard** is a local, privacy-first food safety sentinel. It takes any food description, ingredients list, or menu item and runs a dual-layer open-source safety analysis to:
1. Detect both direct allergens and obscure hidden derivatives (e.g. flagging *arachis oil* as a peanut risk).
2. Highlight high-risk kitchen cross-contamination vectors (shared fryers, woks, cutting boards).
3. Issue an unmistakable verdict: **🔴 DANGER**, **🟡 WARNING**, or **🟢 SAFE**.
4. Generate a one-click, bilingual (English & Indonesian) **Chef Safety Card** that Sarah can show directly to the waiter or kitchen staff.

When I showed the prototype to Sarah, she breathed a huge sigh of relief:  
> *"Finally, something I can use in the basement food court without needing an internet signal or wondering if my medical details are being tracked by an ad network!"*

---

## Demo

The app runs as a lightweight, clean local web dashboard at `http://localhost:8080`.

### Real-world Test Scenarios:

1. **Test 1: Pad Thai with hidden Peanut oil**
   - **Input:** *"Pad thai noodles with fried egg, bean sprouts, crushed peanuts, scallions, cooked with arachis oil and fish sauce."*
   - **Verdict:** `🔴 DANGER: DO NOT CONSUME`
   - **Detected Hazards:** Direct peanuts + obscure alias `arachis oil`.
   - **Kitchen Risks:** Shared woks and cold-pressed peanut oils.

2. **Test 2: Vegan Stew with hidden Gluten**
   - **Input:** *"Vegetarian plant-based BBQ bowl with roasted seitan chunks, malt extract sauce, steamed corn, and barley pearls."*
   - **Verdict:** `🔴 DANGER: Celiac / Gluten Violation`
   - **Detected Hazards:** `seitan`, `malt extract`, and `barley pearls`.

3. **Test 3: Clean Atlantic Salmon**
   - **Input:** *"Pan-seared Atlantic salmon fillet with extra virgin olive oil, sea salt, cracked black pepper, steamed broccoli, and jasmine rice."*
   - **Verdict:** `🟢 SAFE`

4. **Chef Safety Card Output (English & Indonesian):**
```text
⚠️ ALLERGY NOTICE FOR THE CHEF:
Hello, I am ordering for my friend Sarah.
STRICT ALLERGIES: Peanut / Groundnut, Gluten / Wheat / Celiac Risk, Dairy / Milk / Casein
DIETARY PREFERENCES: None
Please ensure food contains NO traces of these ingredients and clean cookware/utensils are used to avoid cross-contamination. Thank you!
```

---

## Code

The code is completely open-source and structured for immediate zero-dependency execution:

- **Repository:** [github.com/dieennn/hacktoberfest-2026/tree/main/00-weekend-allergy-guard](https://github.com/dieennn/hacktoberfest-2026/tree/main/00-weekend-allergy-guard)

### Project Architecture:
- `app.py`: Standalone Python web server & REST API using purely Python 3 standard library (`http.server` & `socketserver`). Zero `pip install` required.
- `analyzer.py`: Open clinical taxonomy engine mapping FDA Big 9 and EU 14 allergens, cross-contamination rules, and local inference bridge.
- `static/index.html`: Responsive, accessible web UI with friend profile presets and instant safety feedback.
- `test_analyzer.py`: Self-contained assert-based automated test suite.

---

## How I Built It

The core engine is built on a **hybrid open-source AI architecture**:

1. **Embedded Clinical Semantic Ontology (100% Offline & Deterministic):**
   We codified FDA Big 9 and EU 14 allergens into an open clinical knowledge base with dozens of obscure culinary aliases (e.g. *arachis*, *valencias*, *seitan*, *farro*, *spelt*, *caseinate*, *surimi*, *albumen*) and cross-contact risk patterns.
2. **Local Open-Weights LLM Integration (Ollama):**
   When Ollama is running locally (`llama3.2`, `gemma2`, or `qwen2.5`), the system passes the matched hazards to the local open model to generate tailored culinary advice and allergen-free ingredient swaps.
3. **Failsafe Design Ladder:**
   Safety cannot rely on probabilistic guesswork. If either the deterministic clinical rules or the local open model identifies a risk, the system escalates to **DANGER**.

---

## Why Does Open Innovation Matter?

Why not just use a closed proprietary API like ChatGPT or Claude?

1. **Works Completely Offline in Low-Connectivity Environments:**
   Food courts, basement restaurants, rural markets, and international travel frequently suffer from poor or zero internet connectivity. Closed APIs fail completely. Open-source local inference works everywhere, every time.
2. **Health Data Privacy & Sovereignty:**
   A person's medical allergies and health conditions are strictly sensitive personal data. Running open-source models locally guarantees zero data telemetry and zero tracking.
3. **Zero Cost & Zero Rate Limits:**
   Friends shouldn't have to pay subscription fees or worry about API token credits just to know if their dinner is safe to eat.
4. **Deterministic Failsafe Control:**
   Closed AI models change behind closed doors and frequently suffer from hallucinations on complex ingredient derivatives. With open code and local weights, we enforce strict verification and safety boundaries.

---

## My Agent Session

This project was built and validated during our Hacktoberfest 2026 preparation session using the DevRelay harness.

---

## Prize Categories

- **Hacktoberfest Open-Source AI Challenge**
- **Build for a Friend Theme**

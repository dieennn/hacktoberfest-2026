# 🛡️ Allergy & Diet Guard (SafeBite AI)
> **Open-Source AI Food Safety & Allergen Sentinel for Friends with Severe Allergies.**  
> *Submission for Hacktoberfest 2026 Weekend DEV Challenge: "Build for a Friend"*.

---

## 🎯 The Story: Why I Built This for a Friend

Eating out or ordering food should be enjoyable, but for my friend **Sarah**, it is an anxiety-inducing minefield. Sarah suffers from:
1. **Severe Peanut Allergy** (risk of anaphylactic shock)
2. **Celiac Disease** (strict gluten-free requirement)
3. **Lactose Intolerance** (no dairy)

In restaurants and takeout menus, ingredients rarely list plain words like *"Peanut"* or *"Wheat"*. Instead, they hide behind obscure culinary and industrial terms like **"arachis oil"**, **"seitan"**, **"malt extract"**, **"casein"**, or **"modified food starch"**.

A single mistake can mean an emergency room visit.

When we are hanging out at a food stall, a crowded night market, or in a basement restaurant with zero cellular reception, closed cloud AI apps (like ChatGPT or proprietary APIs) fail completely:
- **No Internet connection** = No analysis.
- **Privacy risk** = Sending sensitive personal medical and dietary restrictions to third-party corporate servers.
- **Hallucination danger** = Generic cloud LLMs often falsely classify derivative allergens as safe.

I built **Allergy & Diet Guard** so Sarah (and anyone caring for a loved one) can inspect ingredients, menus, and food labels in real-time, **100% locally and offline**.

---

## 💡 Why Open Innovation & Open-Source AI Matter Here

1. **Zero-Latency & Works Completely Offline**: Runs on a laptop or local device without an active internet connection. Perfect for restaurants, supermarkets, or overseas travel.
2. **Health Data Privacy by Design**: Personal allergen profiles and medical sensitivities never leave your local machine.
3. **Open-Weights & Failsafe Rule Hybrid**:
   - Uses an embedded open-source clinical taxonomy (FDA Big 9 + EU 14 allergens, cross-contact matrices, E-numbers, and Indonesian/English synonyms).
   - Integrates seamlessly with local open-weights LLMs via **Ollama** (`llama3.2`, `gemma2`, `qwen2.5`) for deep semantic context and substitution advice.
   - Built with a deterministic failsafe ladder: if either the rule engine or the local model detects a risk, it immediately triggers a safety warning. Never guess on allergy safety.
4. **Instant Actionable Output**: Generates bilingual (English & Bahasa Indonesia) **Chef Cards** to show directly to the kitchen staff or waiter to prevent cross-contamination.

---

## 🚀 Quick Start (Zero External Dependencies)

The core server is built purely on **Python 3 standard library**. You don't even need `pip install`!

### 1. Run the App
```bash
cd allergy-guard
python app.py
```

Open your browser at **`http://localhost:8080`**.

### 2. (Optional) Enable Local Open-Weight LLM Inference with Ollama
If you have Ollama installed on your machine:
```bash
ollama run llama3.2
```
Allergy & Diet Guard will automatically communicate with `http://localhost:11434` to provide additional culinary insights and allergen-free recipe substitutions. If Ollama is not running, the built-in deterministic offline engine handles all safety analysis seamlessly.

### 3. Run Self-Checks / Unit Tests
```bash
python test_analyzer.py
```
*Outputs: `All 4 safety verification tests PASSED successfully!`*

---

## 📸 Key Features

- **Quick Friend Presets**: One-click switch between profiles (e.g. *Sarah's Profile*, *Budi's Shellfish & Halal*, or custom allergens).
- **Hidden Derivative Detection**: Catches obscure terms like *arachis oil* (peanut), *seitan/malt* (gluten), *casein/whey* (dairy), and *surimi* (shellfish).
- **Cross-Contamination Risk Alerts**: Flags shared fryers, woks, cutting boards, and baking lines.
- **Chef Safety Card**: One-click bilingual card ready to show restaurant waiters or chefs.

---

## 📄 License
MIT License. Open-source for everyone. Built for Hacktoberfest 2026.

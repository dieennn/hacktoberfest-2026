"""
HustleLedger AI Engine (Hacktoberfest 2026 Week 2: Side Hustle)
Local-first financial sentinel, expense tax-categorizer, and client invoice defender.
Zero pip dependencies. Offline rule engine with Google Gemma open-weight LLM bridge.
"""

import json
import os
import re
import urllib.request
import urllib.error

# Tax Deductible Business Expense Categories (Standard Schedule C / Freelance tax rules)
EXPENSE_TAXONOMY = {
    "software_saas": {
        "label": "Software & Digital Tools",
        "deductible_pct": 100,
        "keywords": ["github", "aws", "render", "digitalocean", "domain", "hosting", "figma", "openai", "jetbrains", "subscription", "zoom", "canva", "software"],
        "tax_advice": "Fully 100% tax-deductible ordinary business operating expense."
    },
    "office_hardware": {
        "label": "Hardware & Equipment",
        "deductible_pct": 100,
        "keywords": ["laptop", "monitor", "keyboard", "mouse", "desk", "chair", "macbook", "headset", "printer", "hard drive", "ssd", "ram"],
        "tax_advice": "100% deductible via Section 179 depreciation or direct operational expense."
    },
    "home_utilities": {
        "label": "Home Office Utilities & Internet",
        "deductible_pct": 50,
        "keywords": ["internet", "wifi", "broadband", "electricity", "fiber", "phone bill", "mobile data"],
        "tax_advice": "Deductible based on business-use ratio (typically 30% to 50% for home offices)."
    },
    "client_meals": {
        "label": "Client Meetings & Business Meals",
        "deductible_pct": 50,
        "keywords": ["coffee meeting", "client lunch", "dinner with client", "restaurant", "cafe", "starbucks"],
        "tax_advice": "50% tax-deductible when discussing legitimate business with a prospect/client."
    },
    "contractor_fees": {
        "label": "Contractor & Subcontracting Services",
        "deductible_pct": 100,
        "keywords": ["designer fee", "freelance writer", "subcontractor", "fiverr", "upwork fee", "accountant", "legal"],
        "tax_advice": "100% deductible; ensure you keep invoice records or 1099/tax IDs on file."
    },
    "education_books": {
        "label": "Professional Education & Courses",
        "deductible_pct": 100,
        "keywords": ["course", "udemy", "book", "tutorial", "conference ticket", "workshop", "certification"],
        "tax_advice": "100% deductible if maintaining or improving skills required for your current business."
    }
}

class HustleLedgerEngine:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = os.environ.get("OLLAMA_URL", ollama_url)
        self.model = os.environ.get("GEMMA_MODEL", "gemma2:2b")

    def categorize_expense(self, description, amount):
        """Parse raw expense text, classify business tax category, and calculate deductible savings."""
        desc = (description or "").lower()
        matched_category = None
        matched_rule = None

        for cat_id, data in EXPENSE_TAXONOMY.items():
            if any(kw in desc for kw in data["keywords"]):
                matched_category = cat_id
                matched_rule = data
                break

        if not matched_rule:
            category_id = "general_misc"
            category_label = "General Miscellaneous Business"
            deductible_pct = 80
            advice = "Review receipt details. Keep invoice copy to justify business necessity during tax review."
        else:
            category_id = matched_category
            category_label = matched_rule["label"]
            deductible_pct = matched_rule["deductible_pct"]
            advice = matched_rule["tax_advice"]

        deductible_amount = round(amount * (deductible_pct / 100.0), 2)
        # Assuming typical 20% self-employment/income marginal tax bracket
        estimated_tax_savings = round(deductible_amount * 0.20, 2)

        return {
            "description": description,
            "raw_amount": round(amount, 2),
            "category_id": category_id,
            "category_label": category_label,
            "deductible_pct": deductible_pct,
            "deductible_amount": deductible_amount,
            "estimated_tax_savings": estimated_tax_savings,
            "tax_note": advice
        }

    def generate_invoice(self, client_name, project_title, items, payment_terms_days=14):
        """Generate structured client invoice with automatic totals and due dates."""
        subtotal = 0.0
        item_list = []
        for it in items:
            name = it.get("name", "Service Item")
            qty = float(it.get("qty", 1))
            rate = float(it.get("rate", 0))
            line_total = round(qty * rate, 2)
            subtotal += line_total
            item_list.append({
                "name": name,
                "qty": qty,
                "rate": rate,
                "total": line_total
            })

        subtotal = round(subtotal, 2)
        return {
            "client_name": client_name or "Valued Client",
            "project_title": project_title or "Freelance Consulting Services",
            "payment_terms_days": payment_terms_days,
            "items": item_list,
            "subtotal": subtotal,
            "total_due": subtotal,
            "invoice_status": "PENDING_PAYMENT",
            "offline_validated": True
        }

    def draft_client_communication(self, comm_type, client_name, invoice_amount, context_note=""):
        """Draft polite overdue payment reminders or scope-creep boundaries using Gemma."""
        # ponytail: Deterministic fallback if local Gemma / Ollama is offline
        if comm_type == "overdue_reminder":
            inv_ref = context_note if context_note else "INV-001"
            fallback = (
                f"Hi {client_name}, I hope your week is going smoothly! "
                f"This is a gentle reminder regarding Invoice #{inv_ref} (${invoice_amount:.2f}), "
                f"which is now past due. Could you please confirm when payment is scheduled? "
                f"Thank you for your prompt help!"
            )
        elif comm_type == "scope_creep":
            fallback = (
                f"Hi {client_name}, thanks for reaching out! Regarding the additional requests: "
                f"these fall outside our agreed project scope. I would love to tackle them! "
                f"I can prepare a separate mini-estimate for this work so we keep our current delivery on schedule. "
                f"Let me know if you would like me to put together a quote."
            )
        else:
            fallback = (
                f"Hi {client_name}, thank you for partnering on this project. "
                f"Please let me know if you need any additional invoice adjustments or deliverables."
            )

        # Attempt inference with Google Gemma via Ollama
        prompt_instruction = (
            f"You are a professional business advisor for freelancers. Draft a courteous, firm, 2-3 sentence email to "
            f"client '{client_name}' regarding '{comm_type}' (Amount: ${invoice_amount:.2f}, Extra context: {context_note}). "
            f"Keep it polished, respectful, and direct."
        )

        payload = {
            "model": self.model,
            "prompt": prompt_instruction,
            "stream": False
        }

        try:
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=1.8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                gemma_text = data.get("response", "").strip()
                if gemma_text:
                    return gemma_text
        except Exception:
            pass

        return fallback

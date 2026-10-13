"""
Verification tests for HustleLedger AI Engine.
Zero-dependency assert test suite.
"""

from engine import HustleLedgerEngine, EXPENSE_TAXONOMY

def test_expense_categorization():
    engine = HustleLedgerEngine()

    # 1. 100% deductible SaaS
    res = engine.categorize_expense("Render Web Service hosting and domain", 35.0)
    assert res["category_id"] == "software_saas"
    assert res["deductible_pct"] == 100
    assert res["deductible_amount"] == 35.0
    assert res["estimated_tax_savings"] == 7.0

    # 2. 50% deductible client coffee meeting
    res_meal = engine.categorize_expense("Coffee meeting with design client at Starbucks", 18.0)
    assert res_meal["category_id"] == "client_meals"
    assert res_meal["deductible_pct"] == 50
    assert res_meal["deductible_amount"] == 9.0

    # 3. Hardware equipment
    res_hw = engine.categorize_expense("Ergonomic mechanical keyboard for coding", 120.0)
    assert res_hw["category_id"] == "office_hardware"
    assert res_hw["deductible_pct"] == 100

def test_invoice_generation():
    engine = HustleLedgerEngine()
    items = [
        {"name": "Landing Page Redesign", "qty": 1, "rate": 600.0},
        {"name": "SEO & Performance Optimization", "qty": 4, "rate": 75.0}
    ]
    inv = engine.generate_invoice("Acme Corp", "Website Revamp", items, payment_terms_days=14)
    assert inv["client_name"] == "Acme Corp"
    assert inv["subtotal"] == 900.0
    assert inv["total_due"] == 900.0
    assert len(inv["items"]) == 2

def test_client_communication():
    engine = HustleLedgerEngine()
    draft = engine.draft_client_communication("overdue_reminder", "Alex", 900.0, "INV-2026")
    assert "Alex" in draft
    assert "900.00" in draft

    creep = engine.draft_client_communication("scope_creep", "Sarah", 500.0)
    assert "scope" in creep.lower()

if __name__ == "__main__":
    test_expense_categorization()
    test_invoice_generation()
    test_client_communication()
    print("[PASS] All HustleLedger AI Engine tests passed.")

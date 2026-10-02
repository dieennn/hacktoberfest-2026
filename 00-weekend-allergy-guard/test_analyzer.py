"""
Runnable assert-based unit tests for Allergy & Diet Guard analyzer.
Run directly with: python test_analyzer.py
"""

from analyzer import SafetyAnalyzer

def test_peanut_allergy_detection():
    analyzer = SafetyAnalyzer()
    profile = {
        "friend_name": "Budi",
        "allergens": ["peanut"],
        "dietary_restrictions": []
    }

    # Direct mention
    res = analyzer.analyze("Contains satay sauce with roasted peanuts and sugar", profile)
    assert res["verdict"] == "DANGER", f"Expected DANGER, got {res['verdict']}"
    assert len(res["hazards"]) == 1
    assert any("peanut" in term for term in res["hazards"][0]["matched_terms"])

    # Hidden alias mention (arachis oil)
    res2 = analyzer.analyze("Fried using pure arachis oil and salt", profile)
    assert res2["verdict"] == "DANGER", f"Expected DANGER for arachis oil, got {res2['verdict']}"
    assert "arachis oil" in res2["hazards"][0]["matched_terms"]

def test_celiac_gluten_detection():
    analyzer = SafetyAnalyzer()
    profile = {
        "friend_name": "Sarah",
        "allergens": ["gluten"],
        "dietary_restrictions": []
    }

    # Obscure gluten derivative (seitan, malt)
    res = analyzer.analyze("Vegan stew with seitan, malt extract, and carrots", profile)
    assert res["verdict"] == "DANGER"
    matched = [term for h in res["hazards"] for term in h["matched_terms"]]
    assert "seitan" in matched or "malt extract" in matched

def test_safe_ingredients():
    analyzer = SafetyAnalyzer()
    profile = {
        "friend_name": "Sarah",
        "allergens": ["peanut", "gluten", "dairy"],
        "dietary_restrictions": ["halal"]
    }

    res = analyzer.analyze("Fresh steamed jasmine rice, grilled chicken breast, olive oil, sea salt, black pepper", profile)
    assert res["verdict"] == "SAFE", f"Expected SAFE, got {res['verdict']}"
    assert len(res["hazards"]) == 0

def test_chef_card_generation():
    analyzer = SafetyAnalyzer()
    profile = {
        "friend_name": "Sarah",
        "allergens": ["peanut", "shellfish"],
        "dietary_restrictions": ["halal"]
    }
    cards = analyzer.generate_chef_card("Sarah", profile)
    assert "Sarah" in cards["en"]
    assert "Peanut" in cards["en"]
    assert "Shellfish" in cards["en"]
    assert "ALERGI BERBAHAYA" in cards["id"]

if __name__ == "__main__":
    test_peanut_allergy_detection()
    test_celiac_gluten_detection()
    test_safe_ingredients()
    test_chef_card_generation()
    print("All 4 safety verification tests PASSED successfully!")

"""
Runnable verification tests for TrailFlora & Garden AI Engine
Zero-dependency assert test suite.
"""

from engine import TrailFloraEngine, PLANT_TAXONOMY, GARDEN_SCHEDULES

def test_toxic_detection():
    engine = TrailFloraEngine()
    
    # 1. Poison Ivy detection
    res = engine.identify_plant("Saw a vine with three leaves and shiny green leaves near the trail path")
    assert res["verdict"] == "TOXIC_HAZARD", f"Expected TOXIC_HAZARD, got {res['verdict']}"
    assert any(m["id"] == "poison_ivy" for m in res["matches"])
    assert res["safety_score"] == 20

    # 2. Belladonna / Lethal nightshade detection
    res_lethal = engine.identify_plant("A bush with shiny black berries and purple bell flowers")
    assert res_lethal["verdict"] == "LETHAL_ALERT", f"Expected LETHAL_ALERT, got {res_lethal['verdict']}"
    assert any(m["id"] == "deadly_nightshade" for m in res_lethal["matches"])
    assert res_lethal["safety_score"] == 0

    # 3. Edible wild mint
    res_mint = engine.identify_plant("Square stem herb with peppermint scent growing by the creek")
    assert res_mint["verdict"] == "SAFE_FORAGING", f"Expected SAFE_FORAGING, got {res_mint['verdict']}"
    assert any(m["id"] == "wild_mint" for m in res_mint["matches"])

    # 4. Unknown plant
    res_unknown = engine.identify_plant("Blue spotted fungus on a rock")
    assert res_unknown["verdict"] == "UNKNOWN_CAUTION"

def test_garden_planner():
    engine = TrailFloraEngine()
    
    # Test zone 5-6 autumn frost plan
    plan = engine.plan_garden("zone_5_6", frost_temp_c=4)
    assert plan["zone"] == "zone_5_6"
    assert "LIGHT FROST WATCH" in plan["frost_alert"]
    assert len(plan["crops"]) >= 3
    assert any(c["crop"] == "Hardneck Garlic" for c in plan["crops"])

def test_outdoor_window():
    engine = TrailFloraEngine()
    
    window = engine.scout_outdoor_window(cloud_pct=15, temp_c=20, trail_minutes=40)
    assert window["vitality_score"] >= 80
    assert window["touch_grass_verdict"] == "PERFECT TIME TO GO OUTSIDE"
    assert "40" in window["mental_reset_quote"]

if __name__ == "__main__":
    test_toxic_detection()
    test_garden_planner()
    test_outdoor_window()
    print("[PASS] All TrailFlora & Garden AI Engine tests passed successfully.")

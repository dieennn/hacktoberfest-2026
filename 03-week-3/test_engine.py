"""
Zero-dependency test suite for SlothDigest AI Engine (Week 3)
"""

from sloth_engine import SlothDigestEngine

def test_thread_distillation():
    engine = SlothDigestEngine()
    sample_chat = """
    Alice: Good morning team! Semangat pagi!
    Bob: Pagi all!
    Charlie: wkwk lol mantap
    David: @me please review the PR for auth gateway before 5 PM today, urgent bug in prod!
    Eve: Noted, thanks.
    Frank: Sip!
    David: Also check the database migration script.
    """
    res = engine.distill_thread(sample_chat, user_alias="me")
    assert res["filtered_noise_lines"] >= 4
    assert res["laziness_score_pct"] > 0
    assert len(res["action_items"]) >= 1
    assert any("PR" in item or "migration" in item for item in res["action_items"])
    assert res["sloth_verdict"] == "2 QUICK ACTIONS NEEDED"

def test_wind_down_planner():
    engine = SlothDigestEngine()
    res = engine.generate_wind_down(minutes=25, fatigue_type="mental_overload")
    assert res["target_duration_mins"] == 25
    assert len(res["sloth_steps"]) == 4
    assert "Theta" in res["recommended_soundscape"]

def test_simplify_task():
    engine = SlothDigestEngine()
    res = engine.simplify_task("Reorganize 500 messy downloads and file tax reports")
    assert "two_minute_starter" in res
    assert len(res["two_minute_starter"]) > 0

if __name__ == "__main__":
    test_thread_distillation()
    test_wind_down_planner()
    test_simplify_task()
    print("[PASS] All SlothDigest AI Engine tests passed.")

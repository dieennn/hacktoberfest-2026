"""
TrailFlora & Garden AI Engine (Hacktoberfest 2026 Week 1: Touch Grass)
Zero-dependency plant safety, foraging sentinel, and frost/garden planner.
Built for offline trail use. Bridges to local Google Gemma model if available.
"""

import json
import os
import re
import urllib.request
import urllib.error

# Trail Flora & Toxic Plant Taxonomy
PLANT_TAXONOMY = {
    "poison_ivy": {
        "common_name": "Poison Ivy (Toxicodendron radicans)",
        "toxicity": "HIGH",
        "danger_type": "Severe contact dermatitis (urushiol rash)",
        "leaf_pattern": "Clusters of three leaflets ('leaves of three, let it be')",
        "edible": False,
        "keywords": ["three leaves", "clusters of three", "pointed leaflets", "vine with aerial rootlets", "shiny green leaves", "red stem"]
    },
    "poison_oak": {
        "common_name": "Poison Oak (Toxicodendron diversilobum)",
        "toxicity": "HIGH",
        "danger_type": "Contact rash and blistering",
        "leaf_pattern": "Scalloped or lobed edges resembling oak leaves, groups of three",
        "edible": False,
        "keywords": ["oak-like leaves", "three leaflets", "lobed leaflets", "fuzzy surface", "dull green leaves"]
    },
    "stinging_nettle": {
        "common_name": "Stinging Nettle (Urtica dioica)",
        "toxicity": "MODERATE",
        "danger_type": "Formic acid sting; edible only when boiled/cooked",
        "leaf_pattern": "Serrated paired opposite leaves, fine stinging hairs",
        "edible": True,
        "prep_required": "Must be blanched or boiled before touching bare skin or eating",
        "keywords": ["stinging hairs", "serrated leaves", "opposite leaf pairs", "fuzzy stem", "burning sting"]
    },
    "deadly_nightshade": {
        "common_name": "Deadly Nightshade / Belladonna (Atropa belladonna)",
        "toxicity": "LETHAL",
        "danger_type": "Tropane alkaloids (atropine, scopolamine) - fatal ingestion risk",
        "leaf_pattern": "Dull dark green oval leaves, purple bell flowers, shiny black berries",
        "edible": False,
        "keywords": ["shiny black berries", "purple bell flowers", "green calyx star", "solitary berries", "dark oval leaves"]
    },
    "wild_blackberry": {
        "common_name": "Wild Blackberry / Bramble (Rubus fruticosus)",
        "toxicity": "NONE",
        "danger_type": "Sharp thorns only; fruit is nutritious",
        "leaf_pattern": "Palmate compound leaves, thorny canes, aggregate dark berries",
        "edible": True,
        "prep_required": "Wash thoroughly; check for mold/insects",
        "keywords": ["compound berries", "thorny bramble", "serrated leaflets", "aggregate fruit", "black fruit cluster"]
    },
    "dandelion": {
        "common_name": "Common Dandelion (Taraxacum officinale)",
        "toxicity": "NONE",
        "danger_type": "Non-toxic, fully edible",
        "leaf_pattern": "Deeply toothed basal rosette, hollow flower stalk, bright yellow flower",
        "edible": True,
        "prep_required": "Ensure harvested away from pesticide-sprayed roadsides",
        "keywords": ["toothed leaves", "yellow flower head", "hollow stem", "milky sap", "basal rosette"]
    },
    "wild_mint": {
        "common_name": "Wild Field Mint (Mentha arvensis)",
        "toxicity": "NONE",
        "danger_type": "Fragrant edible herb",
        "leaf_pattern": "Square stems, serrated opposite aromatic leaves",
        "edible": True,
        "prep_required": "Rinse clean; great for outdoor trail tea",
        "keywords": ["square stem", "aromatic smell", "peppermint scent", "opposite leaves", "serrated mint leaves"]
    }
}

# Garden Planting Almanac by Zone & Temperature (Tabular rule engine)
GARDEN_SCHEDULES = {
    "zone_3_4": {
        "label": "Cold Northern (USDA Zones 3-4)",
        "fall_frost_window": "Late September - Early October",
        "current_recommendations": [
            {"crop": "Garlic", "action": "Plant cloves 3 inches deep before ground freezes", "days_to_harvest": 240},
            {"crop": "Winter Rye (Cover)", "action": "Broadcast seed now to protect topsoil", "days_to_harvest": 180},
            {"crop": "Spinach (Cold Frame)", "action": "Sow under insulated plastic cloche", "days_to_harvest": 50}
        ]
    },
    "zone_5_6": {
        "label": "Temperate Mid-Latitude (USDA Zones 5-6)",
        "fall_frost_window": "Mid to Late October",
        "current_recommendations": [
            {"crop": "Hardneck Garlic", "action": "Ideal planting window this week", "days_to_harvest": 220},
            {"crop": "Kale & Collards", "action": "Harvest leaves after first light frost (sweeter taste)", "days_to_harvest": 30},
            {"crop": "Radishes & Asian Greens", "action": "Direct sow quick-maturing varieties", "days_to_harvest": 28},
            {"crop": "Spring Bulbs (Tulips/Daffodils)", "action": "Plant bulbs in cool, workable soil", "days_to_harvest": 150}
        ]
    },
    "zone_7_8": {
        "label": "Mild Transitional (USDA Zones 7-8)",
        "fall_frost_window": "Early to Mid November",
        "current_recommendations": [
            {"crop": "Spinach & Arugula", "action": "Sow succession crops directly in ground", "days_to_harvest": 35},
            {"crop": "Carrots & Beets", "action": "Thin seedlings and mulch heavily for winter harvest", "days_to_harvest": 60},
            {"crop": "Shallots & Softneck Garlic", "action": "Plant bulbs in rich composted beds", "days_to_harvest": 210},
            {"crop": "Fava Beans", "action": "Sow now for overwinter nitrogen fixation", "days_to_harvest": 120}
        ]
    },
    "zone_9_10": {
        "label": "Warm Southern (USDA Zones 9-10)",
        "fall_frost_window": "December or Rare Frost",
        "current_recommendations": [
            {"crop": "Bush & Pole Beans", "action": "Second planting season begins now", "days_to_harvest": 55},
            {"crop": "Broccoli & Cauliflower", "action": "Transplant seedlings into sunny garden beds", "days_to_harvest": 70},
            {"crop": "Lettuce & Salad Greens", "action": "Sow freely without bolting risk", "days_to_harvest": 40},
            {"crop": "Strawberries", "action": "Set bare-root crowns for winter/spring crops", "days_to_harvest": 90}
        ]
    }
}

class TrailFloraEngine:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = os.environ.get("OLLAMA_URL", ollama_url)
        self.model = os.environ.get("GEMMA_MODEL", "gemma2:2b")

    def identify_plant(self, query_text):
        """Analyze plant description, leaf patterns, and foraging risks."""
        text = (query_text or "").lower()
        matches = []

        for plant_id, data in PLANT_TAXONOMY.items():
            matched_terms = [kw for kw in data["keywords"] if kw in text]
            if matched_terms:
                matches.append({
                    "id": plant_id,
                    "name": data["common_name"],
                    "toxicity": data["toxicity"],
                    "danger_type": data["danger_type"],
                    "leaf_pattern": data["leaf_pattern"],
                    "edible": data["edible"],
                    "prep_required": data.get("prep_required", "Not edible - do not consume"),
                    "matched_indicators": matched_terms
                })

        # Determine overall safety assessment
        if not matches:
            verdict = "UNKNOWN_CAUTION"
            headline = "No verified plant signature matched. When in doubt on the trail, NEVER touch or ingest."
            safety_score = 50
        elif any(m["toxicity"] == "LETHAL" for m in matches):
            verdict = "LETHAL_ALERT"
            headline = "CRITICAL WARNING: Plant matches lethal wild species (e.g. Belladonna/Nightshade). Do not touch, ingest, or let pets approach!"
            safety_score = 0
        elif any(m["toxicity"] == "HIGH" for m in matches):
            verdict = "TOXIC_HAZARD"
            headline = "CONTACT WARNING: High likelihood of dermatitis/rash-inducing plant (e.g. Poison Ivy/Oak). Avoid bare skin contact."
            safety_score = 20
        elif any(m["toxicity"] == "MODERATE" for m in matches):
            verdict = "IRRITANT_CAUTION"
            headline = "CAUTION: Plant possesses irritant hairs (e.g. Stinging Nettle). Wear gloves if foraging."
            safety_score = 60
        else:
            verdict = "SAFE_FORAGING"
            headline = "SAFE OBSERVATION: Matched recognized benign or edible outdoor wild species."
            safety_score = 95

        llm_guidance = self._query_gemma_outdoor_tips(query_text, verdict, matches)

        return {
            "verdict": verdict,
            "headline": headline,
            "safety_score": safety_score,
            "matches": matches,
            "trail_advice": llm_guidance,
            "offline_mode": True
        }

    def plan_garden(self, zone_key, frost_temp_c=10):
        """Tabular garden calendar planner based on hardiness zone and ambient temperature."""
        zone_data = GARDEN_SCHEDULES.get(zone_key, GARDEN_SCHEDULES["zone_5_6"])
        
        # Calculate urgency index
        if frost_temp_c <= 2:
            frost_alert = "CRITICAL: Hard freeze imminent (< 2°C). Cover sensitive plants tonight with burlap or frost blankets."
            outdoor_action = "Emergency Harvest / Protective Mulch"
        elif frost_temp_c <= 7:
            frost_alert = "LIGHT FROST WATCH: Cold night dips expected. Cold-hardy root crops and greens will thrive and sweeten."
            outdoor_action = "Sow cold-hardy varieties & prepare mulch beds"
        else:
            frost_alert = "MODERATE: Soil retains daytime warmth. Prime planting window for autumn garden work."
            outdoor_action = "Optimal autumn planting & bed prep"

        return {
            "zone": zone_key,
            "zone_label": zone_data["label"],
            "fall_frost_window": zone_data["fall_frost_window"],
            "ambient_temp_c": frost_temp_c,
            "frost_alert": frost_alert,
            "action_header": outdoor_action,
            "crops": zone_data["current_recommendations"]
        }

    def scout_outdoor_window(self, cloud_pct=20, temp_c=18, trail_minutes=45):
        """Calculate optimal outdoor time window to break screen addiction and touch grass."""
        # Heuristic outdoor vitality score
        vitality = 100
        reasons = []

        if temp_c < 5:
            vitality -= 20
            reasons.append("Chilly air: Wear windproof layers and gloves.")
        elif temp_c > 30:
            vitality -= 25
            reasons.append("High heat: Carry hydration and seek tree-shaded woodland trails.")
        else:
            reasons.append(f"Comfortable temperature ({temp_c}°C): Ideal for brisk walking and deep breathing.")

        if cloud_pct < 40:
            reasons.append("Good natural sunlight: 20 minutes outside delivers your daily Vitamin D synthesis.")
        else:
            reasons.append("Overcast sky: Perfect low-glare lighting for autumn leaf-spotting and macro photography.")

        screen_break_benefit = (
            f"Taking this {trail_minutes}-minute outdoor walk cuts digital eye fatigue, lowers resting heart rate, "
            f"and resets circadian rhythms before sunset."
        )

        return {
            "vitality_score": max(20, min(100, vitality)),
            "suggested_duration_mins": trail_minutes,
            "conditions_summary": f"{temp_c}°C, {cloud_pct}% cloud cover",
            "trail_benefits": reasons,
            "touch_grass_verdict": "PERFECT TIME TO GO OUTSIDE" if vitality >= 70 else "GO OUT WITH APPROPRIATE GEAR",
            "mental_reset_quote": screen_break_benefit
        }

    def _query_gemma_outdoor_tips(self, text, verdict, matches):
        """Bridge to local Google Gemma open-weight model via Ollama."""
        # ponytail: Deterministic fallback if Ollama/Gemma not running locally
        if not matches:
            fallback = "Outdoor Trail Rule #1: Take photos, leave no trace. If you can't identify a plant with 100% certainty, leave it wild."
        elif verdict in ("LETHAL_ALERT", "TOXIC_HAZARD"):
            fallback = "Safety protocol: Mark the spot on your offline map, wash any exposed skin with cool soapy water immediately if brushed against, and educate hiking partners."
        else:
            fallback = "Forager's code: Never harvest more than 1/3 of any healthy wild plant patch. Always ensure soil is free of roadway runoff."

        # Attempt local Gemma inference
        payload = {
            "model": self.model,
            "prompt": f"You are an outdoor botanical trail ranger. Briefly in 2 short sentences provide safety tips for a hiker who spotted: '{text}'. Verdict is {verdict}.",
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
                response_text = data.get("response", "").strip()
                if response_text:
                    return response_text
        except Exception:
            pass

        return fallback

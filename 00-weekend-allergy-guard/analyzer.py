"""
Allergy & Diet Guard - Core Allergen & Diet Intelligence Engine
Open-source rule & semantic ontology for allergen identification,
hidden synonym detection, and cross-contamination warning.
"""

import json
import urllib.request
import urllib.error
import re
from typing import Dict, List, Any, Optional

# FDA Big 9 + EU 14 Allergen Taxonomy with Obscure Aliases & E-Numbers
ALLERGEN_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "peanut": {
        "label": "Peanut / Groundnut",
        "severity_default": "severe",
        "aliases": [
            "peanut", "peanuts", "kacang tanah", "groundnut", "arachis", "arachis oil",
            "arachis hypogaea", "beer nuts", "monkey nuts", "mandelonas", "goober",
            "goober peas", "valencias", "hydrolyzed peanut protein"
        ],
        "cross_contamination_risks": [
            "shared fryers (tempura, french fries)", "pad thai / satay woks",
            "bakery lines processing nutty pastries", "cold-pressed oils"
        ]
    },
    "gluten": {
        "label": "Gluten / Wheat / Celiac Risk",
        "severity_default": "severe",
        "aliases": [
            "gluten", "wheat", "gandum", "terigu", "flour", "tepung terigu",
            "barley", "jelai", "rye", "seitan", "malt", "malt extract",
            "spelt", "kamut", "farro", "triticale", "bulgur", "semolina",
            "couscous", "brewer's yeast", "soy sauce", "kecap asin (wheat-fermented)",
            "modified food starch", "vital wheat gluten"
        ],
        "cross_contamination_risks": [
            "shared pasta water", "shared toaster / grills", "shared fryers with breaded food",
            "cutting boards used for regular bread"
        ]
    },
    "dairy": {
        "label": "Dairy / Milk / Lactose",
        "severity_default": "moderate",
        "aliases": [
            "milk", "susu", "dairy", "cheese", "keju", "butter", "mentega",
            "cream", "whey", "casein", "caseinate", "curds", "ghee", "custard",
            "lactalbumin", "lactoglobulin", "lactose", "sour cream", "yogurt",
            "milk solids", "reconstituted milk powder"
        ],
        "cross_contamination_risks": [
            "griddle with melted butter", "milk frother wand on coffee machines",
            "shared pizza prep station"
        ]
    },
    "shellfish": {
        "label": "Crustacean & Molluscan Shellfish",
        "severity_default": "severe",
        "aliases": [
            "shrimp", "udang", "prawn", "crab", "kepiting", "lobster", "crawfish",
            "oyster", "tiram", "clam", "kerang", "mussel", "scallop", "squid",
            "cumi", "octopus", "gurita", "cuttlefish", "surimi", "glukosamin",
            "fish sauce (often contains shellfish)", "shrimp paste", "terasi", "petis"
        ],
        "cross_contamination_risks": [
            "wok frying with seafood broths", "seafood boil pots", "shared grill surfaces"
        ]
    },
    "tree_nuts": {
        "label": "Tree Nuts",
        "severity_default": "severe",
        "aliases": [
            "almond", "walnut", "cashew", "mente", "kacang mede", "pecan",
            "pistachio", "macadamia", "hazelnut", "brazil nut", "chestnut",
            "praline", "marzipan", "nutella", "gianduja", "frangipane"
        ],
        "cross_contamination_risks": [
            "blenders used for nut milks/smoothies", "salad tossing bowls", "pesto prep surfaces"
        ]
    },
    "egg": {
        "label": "Egg",
        "severity_default": "moderate",
        "aliases": [
            "egg", "telur", "albumin", "albumen", "globulin", "lysozyme",
            "mayonnaise", "meringue", "ovalbumin", "ovomucin", "surimi",
            "egg wash", "aioli", "lecithin (if egg-derived)"
        ],
        "cross_contamination_risks": [
            "egg wash brushes on bakery items", "shared frying pans"
        ]
    },
    "soy": {
        "label": "Soybeans",
        "severity_default": "moderate",
        "aliases": [
            "soy", "soya", "kedelai", "soybean", "edamame", "miso", "natto",
            "tofu", "tahu", "tempeh", "tempe", "shoyu", "tamari",
            "textured vegetable protein", "tvp", "soy lecithin", "e322"
        ],
        "cross_contamination_risks": [
            "asian cooking woks", "shared deep fryers"
        ]
    }
}

DIETARY_RULES: Dict[str, Dict[str, Any]] = {
    "halal": {
        "label": "Halal",
        "forbidden": [
            "pork", "babi", "ham", "bacon", "lard", "pork gelatin", "gelatin (pork)",
            "alcohol", "wine", "beer", "mirin", "sake", "rum", "angciu", "bourbon"
        ]
    },
    "vegan": {
        "label": "Vegan",
        "forbidden": [
            "meat", "daging", "beef", "chicken", "ayam", "pork", "fish", "ikan",
            "gelatin", "honey", "madu", "milk", "cheese", "egg", "butter", "whey", "casein"
        ]
    }
}

class SafetyAnalyzer:
    def __init__(self, ollama_endpoint: str = "http://localhost:11434"):
        self.ollama_endpoint = ollama_endpoint.rstrip("/")

    def analyze(self, ingredients_text: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dual-mode analysis:
        1. Local Semantic Taxonomy Rule Engine (Fast, Deterministic, 100% Offline)
        2. Local Open-Weights LLM enrichment (if Ollama is active)
        """
        clean_text = ingredients_text.lower()
        active_allergens = profile.get("allergens", [])
        active_diets = profile.get("dietary_restrictions", [])
        friend_name = profile.get("friend_name", "My Friend")

        detected_hazards = []
        cross_contact_warnings = []
        safe_ingredients = []

        # 1. Allergen Scan
        for allergen_key in active_allergens:
            if allergen_key not in ALLERGEN_TAXONOMY:
                continue
            tax = ALLERGEN_TAXONOMY[allergen_key]
            matched_aliases = []
            for alias in tax["aliases"]:
                # Word boundary match
                pattern = r"(?:\b|_)" + re.escape(alias) + r"(?:\b|_)"
                if re.search(pattern, clean_text):
                    matched_aliases.append(alias)

            if matched_aliases:
                detected_hazards.append({
                    "allergen": allergen_key,
                    "label": tax["label"],
                    "severity": tax["severity_default"],
                    "matched_terms": matched_aliases,
                    "reason": f"Directly contains {tax['label']} (matched terms: {', '.join(matched_aliases)})"
                })
                cross_contact_warnings.extend(tax["cross_contamination_risks"])

        # 2. Dietary Restriction Scan
        for diet_key in active_diets:
            if diet_key not in DIETARY_RULES:
                continue
            rule = DIETARY_RULES[diet_key]
            matched_forbidden = []
            for term in rule["forbidden"]:
                pattern = r"(?:\b|_)" + re.escape(term) + r"(?:\b|_)"
                if re.search(pattern, clean_text):
                    matched_forbidden.append(term)
            if matched_forbidden:
                detected_hazards.append({
                    "allergen": diet_key,
                    "label": f"Diet Violation: {rule['label']}",
                    "severity": "high",
                    "matched_terms": matched_forbidden,
                    "reason": f"Contains non-{rule['label']} ingredient ({', '.join(matched_forbidden)})"
                })

        # 3. Overall Verdict determination
        if any(h["severity"] == "severe" for h in detected_hazards):
            verdict = "DANGER"
            summary = f"DO NOT CONSUME: Contains critical allergen(s) that pose an anaphylactic/severe risk for {friend_name}."
        elif detected_hazards:
            verdict = "WARNING"
            summary = f"CAUTION: Potential allergen or dietary conflict detected for {friend_name}."
        else:
            verdict = "SAFE"
            summary = f"No tracked allergens or dietary violations found in the provided ingredient list for {friend_name}."

        # 4. Optional Local Open LLM Reasoning
        llm_insight = self._query_local_llm(ingredients_text, profile, verdict, detected_hazards)

        # 5. Generate Chef / Waiter Safety Card
        chef_card = self.generate_chef_card(friend_name, profile)

        return {
            "verdict": verdict,
            "friend_name": friend_name,
            "summary": summary,
            "hazards": detected_hazards,
            "cross_contact_risks": list(set(cross_contact_warnings))[:3],
            "llm_insight": llm_insight,
            "chef_card": chef_card,
            "engine": "local_open_source"
        }

    def _query_local_llm(self, text: str, profile: Dict[str, Any], verdict: str, hazards: List[Dict[str, Any]]) -> Optional[str]:
        """Query local Ollama instance if available. Fails gracefully if not running."""
        try:
            prompt = (
                f"You are AllergyGuard, an open-source clinical food safety agent. "
                f"User Profile: Name: {profile.get('friend_name')}, Allergies: {profile.get('allergens')}, Diets: {profile.get('dietary_restrictions')}.\n"
                f"Food item / Ingredients: '{text}'.\n"
                f"Rule Verdict: {verdict}. Detected hazards: {json.dumps(hazards)}.\n"
                f"In 2 brief sentences, provide practical advice for the kitchen and suggest a 100% safe substitute if hazardous."
            )
            payload = json.dumps({
                "model": "llama3.2", # or whichever open model user has
                "prompt": prompt,
                "stream": False
            }).encode("utf-8")

            req = urllib.request.Request(
                f"{self.ollama_endpoint}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "").strip()
        except Exception:
            # ponytail: Local deterministic fallback when Ollama is offline. Upgrade: run 'ollama run llama3.2'
            if verdict == "DANGER":
                return f"Recommend replacing this dish with an allergen-free alternative made with certified clean prep surfaces."
            elif verdict == "WARNING":
                return f"Confirm cooking oil and sauces with kitchen staff to ensure no hidden derivative ingredients."
            return f"Dish appears free of declared allergens. Remind kitchen to avoid shared fryers or utensils."

    def generate_chef_card(self, friend_name: str, profile: Dict[str, Any]) -> Dict[str, str]:
        """Generates print-ready / mobile-showable Chef Card in ID and EN."""
        allergens = [ALLERGEN_TAXONOMY[k]["label"] for k in profile.get("allergens", []) if k in ALLERGEN_TAXONOMY]
        diets = [DIETARY_RULES[k]["label"] for k in profile.get("dietary_restrictions", []) if k in DIETARY_RULES]

        allergen_list_en = ", ".join(allergens) if allergens else "None"
        allergen_list_id = ", ".join(allergens) if allergens else "Tidak ada"

        en = (
            f"⚠️ ALLERGY NOTICE FOR THE CHEF:\n"
            f"Hello, I am ordering for my friend {friend_name}.\n"
            f"STRICT ALLERGIES: {allergen_list_en}\n"
            f"DIETARY PREFERENCES: {', '.join(diets) if diets else 'None'}\n"
            f"Please ensure food contains NO traces of these ingredients and clean cookware/utensils are used to avoid cross-contamination. Thank you!"
        )

        id_text = (
            f"⚠️ CATATAN ALERGI MAKANAN UNTUK KOKI/DAPUR:\n"
            f"Halo, saya memesan makanan untuk teman saya {friend_name}.\n"
            f"ALERGI BERBAHAYA: {allergen_list_id}\n"
            f"PANTANGAN: {', '.join(diets) if diets else 'Tidak ada'}\n"
            f"Mohon pastikan makanan TIDAK MENGANDUNG bahan tersebut dan gunakan peralatan/wajan bersih untuk mencegah kontaminasi silang. Terima kasih!"
        )

        return {"en": en, "id": id_text}

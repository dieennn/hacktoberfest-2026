"""
SlothDigest AI Engine (Hacktoberfest 2026 Week 3: Slow and Steady)
Zero-dependency lazy triage assistant for chats, emails, and dreadful tasks.
Built for International Sloth Day. Bridges to local Google Gemma via Ollama.
"""

import json
import os
import re
import urllib.request
import urllib.error

# Heuristic patterns for noisy chat/email filtering
NOISE_PATTERNS = [
    r"\b(ok|k|sip|siap|noted|thanks|thank you|makasih|terima kasih|haha|wkwk|lol|lmao|pagi|halo|semangat|good morning|ping)\b"
]

URGENT_KEYWORDS = ["urgent", "asap", "deadline", "today", "hari ini", "segera", "blocked", "broken", "critical", "error", "bayar", "invoice", "tolong"]
ACTION_VERBS = ["review", "merge", "send", "kirim", "bikin", "check", "fix", "update", "baca", "approve", "deploy", "call", "jadwalkan"]

class SlothDigestEngine:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = os.environ.get("OLLAMA_URL", ollama_url)
        self.model = os.environ.get("GEMMA_MODEL", "gemma2:2b")

    def distill_thread(self, raw_text, user_alias="me"):
        """Distill overwhelming chats or bloated email threads into lazy actionable highlights."""
        lines = [line.strip() for line in (raw_text or "").split("\n") if line.strip()]
        total_words = sum(len(line.split()) for line in lines)

        clean_lines = []
        action_items = []
        urgent_items = []

        alias = user_alias.lower()

        for line in lines:
            line_lower = line.lower()
            msg_content = re.sub(r"^[a-zA-Z0-9_\s]+:\s*", "", line_lower).strip()

            has_urgent = any(w in line_lower for w in URGENT_KEYWORDS)
            has_action = f"@{alias}" in line_lower or any(v in line_lower for v in ACTION_VERBS)

            # Filter noise if matches noise patterns and lacks concrete actions/urgency
            is_noise = any(re.search(pat, msg_content) for pat in NOISE_PATTERNS)
            if is_noise and not has_urgent and not has_action and len(msg_content.split()) <= 6:
                continue

            clean_lines.append(line)

            if has_urgent:
                urgent_items.append(line)

            if has_action and line not in action_items:
                action_items.append(line)

        # Calculate sloth laziness yield (reading time saved)
        distilled_count = len(action_items) * 10 + 20
        effort_saved_pct = max(10, min(95, round((1 - (distilled_count / max(total_words, 1))) * 100)))

        # Summary generation
        summary = self._query_gemma_summary(raw_text, action_items, urgent_items)

        return {
            "original_word_count": total_words,
            "filtered_noise_lines": len(lines) - len(clean_lines),
            "laziness_score_pct": effort_saved_pct,
            "reading_time_saved_minutes": max(1, round(total_words / 180, 1)),
            "sloth_verdict": "SAFE TO IGNORE 90%" if not urgent_items else "2 QUICK ACTIONS NEEDED",
            "action_items": action_items[:5],
            "urgent_flags": urgent_items[:3],
            "two_line_summary": summary,
            "offline_mode": True
        }

    def generate_wind_down(self, minutes=20, fatigue_type="screen_eye_strain"):
        """Generate offline ambient relaxation routine and brown-noise soundscape prescription."""
        routines = {
            "screen_eye_strain": {
                "label": "Digital Screen Burnout & Eye Fatigue",
                "soundscape": "432Hz Ambient Forest Rain + Soft Brown Noise",
                "steps": [
                    "Close eyes and palm warm hands over eye sockets for 60 seconds (20-20-20 reset).",
                    "Put phone into grayscale / airplane mode across the room.",
                    "Sip chamomile or warm water without touching any keyboard.",
                    "Slow 4-7-8 breathing count for 3 cycles."
                ]
            },
            "mental_overload": {
                "label": "Code Cognitive Overload & Decision Fatigue",
                "soundscape": "Theta Binaural Waves (6Hz) + Distant Ocean Surf",
                "steps": [
                    "Brain dump: write remaining worries on scrap paper, then close the notebook.",
                    "Dim lighting below 2700K warm incandescent tone.",
                    "Lie flat on floor or bed with knees bent to release lower back tension.",
                    "Give yourself full permission: the world functions fine without you until tomorrow."
                ]
            }
        }

        selected = routines.get(fatigue_type, routines["screen_eye_strain"])
        return {
            "target_duration_mins": minutes,
            "fatigue_category": selected["label"],
            "recommended_soundscape": selected["soundscape"],
            "sloth_steps": selected["steps"],
            "sloth_mantra": "A sloth survives 60 million years by not rushing. Slow down."
        }

    def simplify_task(self, dreadful_task):
        """Break down an avoided dreadful task into an embarrassingly small 2-minute sloth starter."""
        task_str = (dreadful_task or "").strip()
        # ponytail: Deterministic rule-based task shrinker fallback
        starter_step = f"Open the relevant window/doc for '{task_str}', write ONE line or delete ONE file, then pause."

        prompt = (
            f"You are a master of behavioral micro-habits and healthy laziness. "
            f"The user is dreading this task: '{task_str}'. "
            f"Give exactly ONE 2-minute ridiculously easy starter step so they get started without effort. "
            f"Under 20 words total."
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
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
                res_txt = data.get("response", "").strip()
                if res_txt:
                    starter_step = res_txt
        except Exception:
            pass

        return {
            "original_task": task_str,
            "two_minute_starter": starter_step,
            "sloth_rule": "Doing 1% beats 0%. Once the 2 minutes pass, feel free to stop guilt-free."
        }

    def _query_gemma_summary(self, raw_text, actions, urgent):
        """Bridge to local Google Gemma open-weight model for lazy 2-line summary."""
        # Fallback summary
        if urgent:
            fallback = f"Discussion has {len(urgent)} time-sensitive items needing quick acknowledgment. Remainder is team chit-chat."
        elif actions:
            fallback = f"Team aligned on ongoing tasks. Only {len(actions)} concrete action items noted; safe to review at your own pace."
        else:
            fallback = "Routine check-ins, acknowledgments, and banter. No blockers or urgent actions required from you."

        payload = {
            "model": self.model,
            "prompt": f"Summarize this conversation into exactly two concise sentences for a busy lazy person: '{raw_text[:800]}'.",
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
                gemma_res = data.get("response", "").strip()
                if gemma_res:
                    return gemma_res
        except Exception:
            pass

        return fallback

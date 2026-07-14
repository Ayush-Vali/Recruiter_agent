import json
from models import AgentState
from nodes.analysis import model8B   # reuse same LLM

import re

TITLE_PATTERNS = [
    r"hiring (?:a|an|for a|for an)\s+([\w\s]+?)(?:\s+for|\s+to|\s+in|\s+at|\.|,|$)",
    r"role\s*[:\-]?\s*([\w\s]+?)(?:\s+at|\s+in|\s+for|\.|,|$)",
    r"position\s*[:\-]?\s*([\w\s]+?)(?:\s+at|\s+in|\.|,|$)",
    r"opening\s+(?:for\s+)?(?:a\s+)?([\w\s]+?)(?:\s+role|\s+position|\.|,|$)",
]

# only for india since, any arabian country has high prority, but for india only hyderabad has prior..
INDIA_CITIES = [
    "hyderabad", "bangalore", "bengaluru", "mumbai",
    "delhi", "pune", "chennai", "noida", "gurgaon", "gurugram"
]

# roles are limited mentioned but can be handled by llm if not found
TITLE_VARIANTS = {
    "product manager":     ["Product Manager", "Senior Product Manager", "Sr. PM",
                            "Head of Product", "VP Product", "Lead PM"],
    "engineering manager": ["Engineering Manager", "Senior Engineering Manager",
                            "Head of Engineering", "VP Engineering"],
    "software engineer":   ["Software Engineer", "Senior Software Engineer",
                            "SDE", "SDE-2", "Staff Engineer"],
    "data scientist":      ["Data Scientist", "Senior Data Scientist",
                            "Lead Data Scientist", "ML Engineer"],
}


def _regex_extract_title(jd: str) -> str:
    '''It will be in 'parse_jd func' to return 'raw title'.
    And the raw title is passed to 'get_title_variants' which checks 
    (if words like 'product manager' is in 'raw title list') '''
    jd_lower = jd.lower()
    for pattern in TITLE_PATTERNS:
        m = re.search(pattern, jd_lower)
        if m:
            raw = m.group(1).strip().title()
            if len(raw.split()) <= 5:   # sanity check
                return raw
    return ""


def _llm_extract_title(jd: str, model) -> str:
    prompt = f"""Extract only the job title from this job description.
Return ONLY the title, nothing else. If you cannot find one, return "Unknown".

Job Description:
{jd[:1000]}

Job Title:"""
    response = model8B.invoke(prompt)
    title = response.content.strip().strip('"').strip("'")
    return title if title.lower() != "unknown" else ""


def get_title_variants(title: str) -> list[str]:
    '''Returns list of title variants after taking raw from _regex_extract'''
    title_lower = title.lower()
    for key, variants in TITLE_VARIANTS.items():
        if key in title_lower:
            return variants
    # when Not in map as key — build generic variants
    # eg. in cases of AI Engineer, etc
    last_word = title.split()[-1]
    return [title, f"Senior {title}", f"Lead {title}", f"Head of {last_word}"]


def parse_jd(state: AgentState) -> AgentState:
    jd_lower = state.jd.lower()

    # ── Region detection ─────────────────────────────────────────────

    if any(w in jd_lower for w in ["saudi", "riyadh", "jeddah", "ksa", "gcc"]):
        state.region = "saudi"
    elif any(w in jd_lower for w in ["india", "hyderabad", "bangalore",
                                      "bengaluru", "mumbai", "delhi", "pune"]):
        state.region = "india"

    # ── Location hint (India only — drives scoring tier) ─────────────
    if state.region == "india":
        if "hyderabad" in jd_lower:
            state.jd_location_hint = "hyderabad"
        else:
            for city in INDIA_CITIES:
                if city in jd_lower:
                    state.jd_location_hint = city
                    break
            else:
                state.jd_location_hint = "india"

    # ── Title: regex first, then LLM fallback ─────────────────────────────
    title = _regex_extract_title(state.jd)
    if not title:
        title = _llm_extract_title(state.jd, model8B)  # model imported from ana.py

    state.jd_title = title
    return state

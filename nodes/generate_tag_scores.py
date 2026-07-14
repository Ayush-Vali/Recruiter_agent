import json
from models import AgentState
from nodes.analysis import model

TAG_SCORES_PROMPT = """
You are an expert recruiter designing an automated candidate scoring system.

Convert this Job Description into structured scoring rules.

Return ONLY valid JSON (no explanation, no markdown):

{{
  "rules": [
    {{
      "tag": "unique_tag_name",
      "label": "Human readable label",
      "weight": 1-5,
      "match_type": "keyword | location | semantic",
      "keywords": ["list", "of", "relevant", "terms"]
    }}
  ]
}}

Rules:
- 5 to 8 total rules
- weight must be 1-5
- tag must be short snake_case
- Prefer keyword match_type when possible
- Include location, experience, skills, and cultural signals

Job Description:
{jd}

JSON only:
"""

def generate_tag_scores(state: AgentState) -> AgentState:
    prompt = TAG_SCORES_PROMPT.format(jd=state.jd[:2500])
    response = model.invoke(prompt)
    content = response.content.strip()

        # Save to a JSON file
    with open("extra/tagcontent.json", "w") as json_file:
        json.dump(content, json_file, indent=4)
    # Save to the specified file
    with open("extra/tagcontent.txt", "w") as file:
        file.write(content)
        
    try:
        data = json.loads(content)
        state.tag_rules = data.get("rules", [])
    except Exception:
        # Safe fallback
        state.tag_rules = [
            {"tag": "relevant_experience", "label": "Relevant experience", "weight": 5, "match_type": "keyword", "keywords": ["experience", "worked", "led"]},
            {"tag": "location_match",      "label": "Location match",      "weight": 3, "match_type": "location", "keywords": ["india", "usa", "uk"]},
        ]
    return state
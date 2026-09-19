import json
from models import AgentState
from nodes.analysis import model,parse_model_output

APIFY_EXTRACTION_PROMPT = """
You are an expert LinkedIn recruiter. Extract the BEST parameters for the Apify LinkedIn Profile Search actor.

Return ONLY valid JSON with these exact keys:
- searchQuery: job title + city/country + one strong preferred keyword from the JD (e.g. "vision2030", "fintech", "AI-first", "remote", "scale", etc.)
- locations: list of country names (e.g. ["Saudi Arabia"], ["India"], ["United States"])
- currentJobTitles: 3-5 similar/senior job titles

Do NOT include markdown formatting like ```json or ```
Do NOT include any explanation, prefix, or suffix.

Job Description:
{jd}

Return only JSON:
{{
  "searchQuery": "...",
  "locations": ["..."],
  "currentJobTitles": ["...", "...", "..."]
}}
"""

def extract_apify_params(state: AgentState) -> AgentState:
    prompt = APIFY_EXTRACTION_PROMPT.format(jd=state.jd[:2500])
    response = model.invoke(prompt)

    ## IF NEED TO SAVE AND USE FOR LATER
    # content_sv = response.content.strip()
    # # Save to a JSON file
    # with open("extra/paramcontent.json", "w") as json_file:
    #     json.dump(content_sv, json_file, indent=4)
    # # Save to the specified file
    # with open("extra/paramcontent.txt", "w") as file:
    #     file.write(content_sv)
        
    


    # with open("extra/paramcontent.txt", "r") as f: # TEST
    #     raw = f.read()   # TEST
    try:
        # data =parse_model_output(raw)  # TEST
        data =parse_model_output(response.content)
        state.search_params = data
    except Exception:
        # safe fallback
        state.search_params = {
            "searchQuery": state.jd.split()[0] + " ",
            "locations": ["United States"],
            "currentJobTitles": ["Product Manager", "Senior Product Manager"]
        }
    return state

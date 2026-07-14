import os
from models import AgentState
from apify_client import ApifyClient
from nodes.parse_jd import get_title_variants
import json


def fetch_candidates(state: AgentState) -> AgentState:
    client = ApifyClient(os.getenv("APIFY_TOKEN"))

    if state.mode == "generic" and state.search_params:
        # LLM-generated params
        params = state.search_params
        search_query = params.get("searchQuery", "")
        locations = params.get("locations", ["United States"])
        job_titles = params.get("currentJobTitles", ["Product Manager"])
    else:
        # specialized path 
        job_titles = get_title_variants(state.jd_title) if state.jd_title else [
            "Product Manager", "Senior Product Manager", "Head of Product"
        ]
        if state.region == "saudi":
            search_query = f"{state.jd_title or 'product manager'} riyadh vision 2030"
            locations = ["Saudi Arabia"]
        else:
            city = state.jd_location_hint if state.jd_location_hint != "india" else "hyderabad"
            search_query = f"{state.jd_title or 'product manager'} {city} startup"
            locations = ["India"]

    run_input = {
        "profileScraperMode": "Full",
        "searchQuery": search_query,
        "maxItems": 10,
        "locations": locations,
        "currentJobTitles": job_titles,
        "startPage": 1,
    }

    run   = client.actor("harvestapi/linkedin-profile-search").call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    state.raw_profiles = items
    return state


from pydantic import BaseModel, field_validator, Field
from typing import List, Optional, Dict, Tuple

class Candidate(BaseModel):
    name: str
    linkedin_url: Optional[str] = ""
    headline: Optional[str] = ""
    location: Optional[str] = ""
    about: Optional[str] = ""
    experience: Optional[str] = ""   # flattened from experience[] list
    skills: Optional[List[str]] = []
    full_text: str = ""              # lowercased concat — used for tag detection
    tags: List[str] = Field(default_factory=list)  # for dynamic - Field(default_factory=list)

    @field_validator("experience", "about", "location", "headline", "linkedin_url", mode="before")
    @classmethod
    def coerce_none(cls, v):
        return v or ""
# fieldvalidator runs below code for 'about','location',etc if v=None, 0, []... and return "" for them

class ScoreCard(BaseModel):
    name: str
    linkedin_url: str = "" 
    region: str           # "saudi" | "india"
    score: float          # 0–10 normalised
    signals: List[str]    # human-readable matched tag labels
    llm_reasoning: str    # filled by cultural_analysis node
    fit: str              # "strong" | "moderate" | "weak"


class AgentState(BaseModel):
    jd: str
    region: str = ""
    jd_title: str = ""           # extracted by parse_jd
    jd_location_hint: str = ""   # "hyderabad" / "bangalore" / "india" / "riyadh"
    raw_profiles: List[dict] = []
    candidates: List[Candidate] = []
    scored_candidates: List[ScoreCard] = []
    search_params: Optional[Dict] = None         # LLM-generated Apify params for generic mode
    tag_rules: List[Dict] = Field(default_factory=list)   # ← NEW: dynamic rules for generic
    mode: str = "specialized"                    # "specialized" or "generic"
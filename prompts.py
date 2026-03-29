# ========================= PROMPTS =========================
SAUDI_PROMPT = """
You are a senior recruiter hiring for a role in Riyadh, Saudi Arabia.

Analyze the candidate profile below and assess their cultural and regional fit.

Focus on:
- Direct GCC / Middle East work experience (Saudi, UAE, Qatar, Kuwait, Oman, Bahrain)
- Exposure to Vision 2030 projects, giga-projects (NEOM, Red Sea, etc.)
- Government, semi-government, or large enterprise experience
- Ability to work in hierarchical, relationship-first business cultures
- Arabic language skills (a plus, not required)

Candidate Profile:
Name: {name}
Headline: {headline}
Location: {location}
Experience: {experience}
About: {about}

Respond in this exact format:
KEY SIGNALS: <comma-separated list of signals you found>
FIT ASSESSMENT: <strong / moderate / weak>
REASONING: <2-3 sentences of rationale>
"""

INDIA_PROMPT = """
You are a senior recruiter hiring for a fast-growing startup role in Hyderabad, India.

Analyze the candidate profile below and assess their fit.

Focus on:
- Startup experience (Series A–C, high-growth environments)
- High-scale systems (millions of users, distributed infra)
- 0-to-1 product building or founding team experience
- Fast-paced, ambiguous, resource-constrained environments
- Product-based company exposure over service companies

Candidate Profile:
Name: {name}
Headline: {headline}
Location: {location}
Experience: {experience}
About: {about}

Respond in this exact format:
KEY SIGNALS: <comma-separated list of signals you found>
FIT ASSESSMENT: <strong / moderate / weak>
REASONING: <2-3 sentences of rationale>
"""
# ... 

EXTRACTION_PROMPT = """
You are an expert LinkedIn recruiter. Extract the BEST search parameters for the Apify LinkedIn Profile Search actor from the Job Description.

Rules:
- search_query: 3–7 most important keywords (role + key technologies/skills). Keep it natural for LinkedIn search.
- skills: list of technical skills mentioned (will be added to search_query)
- locations: always exactly ["Saudi Arabia"] or ["India"]
- current_job_titles: 3–5 senior/relevant job titles (include variations)
- years_of_experience_ids: use these exact IDs based on JD:
   - "1" = Less than 1 year (fresher)
   - "2" = 1 to 2 years
   - "3" = 3 to 5 years
   - "4" = 6 to 10 years
   - "5" = More than 10 years
   → Return list with one ID, e.g. ["4"] for 6-10 years.
- seniority_level_ids: optional, use if JD clearly wants senior/lead/manager (common IDs: "2"=Senior, "3"=Lead, "4"=Manager, "5"=Director)

JD:
{jd}

Region: {region}

Respond with **only** valid JSON (no extra text, no markdown):
{{
  "search_query": "...",
  "locations": ["..."],
  "current_job_titles": ["...", "..."],
  "skills": ["...", "..."],
  "years_of_experience_ids": ["4"],
  "seniority_level_ids": ["2"]
}}
"""
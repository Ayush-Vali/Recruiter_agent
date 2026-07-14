from models import AgentState, Candidate
'''Helpful for scoring profiles as per client'''


VISION2030_TERMS = [
    "vision 2030",
    "neom", "the line", "trojena", "oxagon", "sindalah",
    "red sea global", "red sea project", "amaala", "qiddiya",
    "diriyah", "roshn", "king salman park", "new murabba",
    "jeddah central", "saudi green initiative", "green riyadh",
    "made in saudi", "saudi genome",
    "qic", "qiddiya investment", "diriyah company",
    "soudah development", "al-ula development", "alula development",
    "saudi downtown", "jeddah central development",
]

GCC_COUNTRIES = [
    "saudi", "riyadh", "jeddah", "mecca", "medina",
    "uae", "dubai", "abu dhabi", "qatar", "doha",
    "kuwait", "oman", "muscat", "bahrain", "manama", "gcc"
]

INDIA_UNICORNS = [
    "swiggy", "dunzo", "darwinbox", "sprinklr", "freshworks",
    "flipkart", "meesho", "razorpay", "zepto", "blinkit",
    "phonepe", "paytm", "ola", "rapido", "udaan", "moglix",
    "groww", "zerodha", "cred", "slice", "jupiter",
    "unacademy", "byju", "vedantu", "upgrad",
    "practo", "mfine", "pristyn", "nykaa", "mamaearth",
    "lenskart", "zomato", "bigbasket", "chargebee",
    "browserstack", "postman", "hasura", "setu", "sarvam",
]

INDIA_CITIES_OTHER = [
    "bangalore", "bengaluru", "mumbai", "delhi",
    "pune", "chennai", "noida", "gurgaon", "gurugram"
]

'''(i downloaded json raw_profiles to understand the how to get values from 
it and use in normalize.py)'''

def normalize_data(state: AgentState) -> AgentState:
    candidates = []
    
    for profile in state.raw_profiles:
        try:
            # ── Name ────────────────────────────────────────────────────
            first = profile.get("firstName", "") or "" 
            # even if firstName key returns '' due to or the '' will be succesfullly returnd
            last  = profile.get("lastName",  "") or ""
            name  = f"{first} {last}".strip() or "Unknown"

            # ── Location (nested dict) ───────────────────────────────────
            loc_obj  = profile.get("location") or {}
            parsed   = loc_obj.get("parsed") or {}
            city     = parsed.get("city",    "") or ""
            country  = parsed.get("country", "") or ""
            location = f"{city}, {country}".strip(", ")

            # ── Headline / About ─────────────────────────────────────────
            headline = profile.get("headline", "") or ""
            about    = profile.get("about",    "") or ""

            # ── Experience: list of dicts → flat string ─────────────────
            exp_list  = profile.get("experience") or []
            exp_parts = []
            for exp in exp_list:
                # returns dict for each position user worked at
                position    = exp.get("position",    "") or ""
                company     = exp.get("companyName", "") or ""
                description = exp.get("description", "") or ""
                exp_loc     = exp.get("location",    "") or ""
                exp_parts.append(
                    f"{position} at {company} {exp_loc}: {description}".strip()
                )
            experience = " | ".join(exp_parts)

            # ── Skills ──────────────────────────────────────────────────
            skills_raw = profile.get("skills") or []
            skills = [s.get("name", "") for s in skills_raw if s.get("name")]

            # ── full_text (lowercased, used for all tag detection) ───────
            full_text = f"{headline} {experience} {about} {location}".lower().strip()



            # =====================================================
            tags = []
            # ── SPECIALIZED MODE (your original rich logic) ─────────────────────
            if state.mode == "specialized":
                    
                # ── GCC: check full_text AND per-experience location/company ─
                # Covers India-based candidates who worked for/in GCC
                gcc_hit = any(w in full_text for w in GCC_COUNTRIES)
                if not gcc_hit: 
                    # to chk again 
                    for exp in exp_list: 
                        el = (exp.get("location",    "") or "").lower()
                        ec = (exp.get("companyName", "") or "").lower()
                        if any(w in el or w in ec for w in GCC_COUNTRIES):
                            gcc_hit = True
                            break
                if gcc_hit:
                    tags.append("gcc")

                # ── Vision 2030: phrase + all project/company names ──────────
                vision_hit = any(t in full_text for t in VISION2030_TERMS)
                if not vision_hit:
                    for exp in exp_list:
                        co = (exp.get("companyName", "") or "").lower()
                        if any(t in co for t in VISION2030_TERMS):
                            vision_hit = True
                            break
                if vision_hit:
                    tags.append("vision2030")

                # These two above had to be dble made sure, but can be written as below
                # ── Other Saudi signals ──────────────────────────────────────
                if any(w in full_text for w in ["aramco", "sabic", "saudi telecom",
                                                "stc", "al rajhi", "maaden"]):
                    tags.append("gcc_enterprise")
                if "arabic" in full_text:
                    tags.append("arabic")
                if any(w in full_text for w in ["government", "public sector", "ministry"]):
                    tags.append("government")


                # ── India signals ────────────────────────────────────────────
                if any(u in full_text for u in INDIA_UNICORNS):
                    tags.append("known_unicorn")

                if any(w in full_text for w in ["series b", "series c", "series d",
                                                "unicorn", "ipo", "acquired by",
                                                "raised $", "valued at"]):
                    tags.append("funded_startup")

                if any(w in full_text for w in ["0 to 1", "zero to one", "0-to-1",
                                                "founding engineer", "founding product",
                                                "co-founder", "cofounder"]):
                    tags.append("zero_to_one")

                if any(w in full_text for w in ["millions of users", "million users",
                                                "crore users", "hypergrowth",
                                                "hyper-growth", "scaled from", "scaled to"]):
                    tags.append("high_scale")

                if any(w in full_text for w in ["saas", "b2c", "b2b", "d2c",
                                                "marketplace", "platform"]):
                    tags.append("product_type")

                if "startup" in full_text:
                    tags.append("startup")


                # ── India location tier ──────────────────────────────────────
                # Check profile city + all experience locations
                all_exp_locs = " ".join(
                    (exp.get("location", "") or "").lower() for exp in exp_list
                )
                combined_loc = f"{location.lower()} {all_exp_locs}"

                if "hyderabad" in combined_loc:
                    tags.append("india_hyderabad")
                elif any(c in combined_loc for c in INDIA_CITIES_OTHER):
                    tags.append("india_other")
            # ── GENERIC MODE (new dynamic rules) ───────────────────────────────
            else:
                full_text_lower = full_text
                location_lower = location.lower()

                for rule in state.tag_rules:
                    match_type = rule.get("match_type", "keyword")
                    keywords = rule.get("keywords", [])

                    if match_type == "keyword":
                        if any(k.lower() in full_text_lower for k in keywords):
                            tags.append(rule["tag"])

                    elif match_type == "location":
                        if any(k.lower() in location_lower for k in keywords):
                            tags.append(rule["tag"])
                    elif match_type == "semantic":
                        if any(k.lower() in full_text_lower for k in keywords):
                            tags.append(rule["tag"])
            

            c = Candidate(
                name=name,
                linkedin_url=profile.get("linkedinUrl", "") or "",
                headline=headline,
                location=location,
                about=about,
                experience=experience,
                skills=skills,
                full_text=full_text,
                tags=tags,
            )
            candidates.append(c)

        except Exception:
            continue

    state.candidates = candidates
    return state
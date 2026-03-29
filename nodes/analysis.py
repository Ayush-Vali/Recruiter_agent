import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from models import AgentState 
from prompts import SAUDI_PROMPT, INDIA_PROMPT

load_dotenv()

llm = HuggingFaceEndpoint(
    # repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",  
    # repo_id = "Qwen/Qwen2.5-32B-Instruct",
    # repo_id="deepseek-ai/DeepSeek-V3.2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    repo_id="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0.7,         
)
model = ChatHuggingFace(llm=llm)

def safe_text(text, limit: int) -> str:
    return (text or "").strip()[:limit]

SAUDI_PROMPT = """
You are a senior recruiter hiring for a role in Riyadh, Saudi Arabia.
Analyze the candidate and assess cultural/regional fit.

Focus on: GCC experience, Vision 2030 / giga-project involvement,
government or enterprise exposure, Arabic language, relationship-first culture fit.

Candidate:
Name: {name}
Headline: {headline}
Location: {location}
Experience: {experience}
About: {about}

Respond in this exact format:
KEY SIGNALS: <comma-separated>
FIT ASSESSMENT: <strong / moderate / weak>
REASONING: <2-3 sentences>
"""

INDIA_PROMPT = """
You are a senior recruiter hiring for a fast-growing startup role in India.
Analyze the candidate and assess fit.

Focus on: startup experience, high-scale systems, 0-to-1 building,
funding stage of past companies, product-based vs service companies.

Candidate:
Name: {name}
Headline: {headline}
Location: {location}
Experience: {experience}
About: {about}

Respond in this exact format:
KEY SIGNALS: <comma-separated>
FIT ASSESSMENT: <strong / moderate / weak>
REASONING: <2-3 sentences>
"""

def cultural_analysis(state: AgentState) -> AgentState:
    prompt_template = SAUDI_PROMPT if state.region == "saudi" else INDIA_PROMPT

    updated_scores = []
    for c in state.candidates:
        prompt = prompt_template.format(
            name=       safe_text(c.name,       100),
            headline=   safe_text(c.headline,   200),
            location=   safe_text(c.location,   100),
            experience= safe_text(c.experience, 1500),
            about=      safe_text(c.about,       500),
        )
        response  = model.invoke(prompt)
        reasoning = response.content.strip()

        scorecard = next((s for s in state.scored_candidates if s.name == c.name), None)
        if scorecard:
            scorecard.llm_reasoning = reasoning
            updated_scores.append(scorecard)

    state.scored_candidates = updated_scores
    return state
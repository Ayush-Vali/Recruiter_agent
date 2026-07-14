import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from models import AgentState 
from prompts import SAUDI_PROMPT, INDIA_PROMPT

ll=HuggingFaceEndpoint(repo_id="", )

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
llm2 = HuggingFaceEndpoint(
    # repo_id="meta-llama/Llama-3.3-70B-Instruct",  
    # repo_id = "Qwen/Qwen2.5-32B-Instruct",
    # repo_id="deepseek-ai/DeepSeek-V3.2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
    temperature=0.7,         
)
model8B = ChatHuggingFace(llm=llm2)

def safe_text(text, limit: int) -> str:
    return (text or "").strip()[:limit]

SAUDI_PROMPT = """
You are a senior recruiter hiring for a role in Riyadh, Saudi Arabia.
Your goal:
- Provide a concise and professional overall reasoning for the candidate’s score
- Treat the given score as final and correct
- Do NOT question or contradict the score
- Highlight the candidate’s strengths and positive aspects from their experience
- If the experience appears limited, focus on the most relevant or promising parts

Candidate:
Name: {name}
Experience: {experience}

Score:
{score}/10

Respond with only 2-3 sentences of reasoning.
Keep the tone professional and balanced.
Do not include any labels or prefixes.
"""

INDIA_PROMPT = """
You are a senior recruiter hiring for a fast-growing startup role in India.

Your goal:
- Provide a concise and professional overall reasoning for the candidate’s score
- Treat the given score as final and correct
- Do NOT question or contradict the score
- Highlight the candidate’s strengths and positive aspects from their experience
- If the experience appears limited, focus on the most relevant or promising parts

Candidate:
Name: {name}
Experience: {experience}

Score:
{score}/10

Respond with only 2-3 sentences of reasoning.
Keep the tone professional and balanced.
Do not include any labels or prefixes.
"""

GENERIC_PROMPT = """
You are an expert recruiter evaluating a candidate.

Your goal:
- Provide a concise and professional overall reasoning for the candidate’s score
- Treat the given score as final and correct
- Do NOT question or contradict the score
- Highlight the candidate’s strengths and positive aspects from their experience
- If the experience appears limited, focus on the most relevant or promising parts

Candidate:
Name: {name}
Experience: {experience}

Score:
{score}/10

Respond with only 2-3 sentences of reasoning.
Keep the tone professional and balanced.
Do not include any labels or prefixes.
"""

def cultural_analysis(state: AgentState) -> AgentState:
    # ── SPECIALIZED MODE (your original rich logic) ─────────────────────
    if state.mode == "specialized":
        prompt_template = SAUDI_PROMPT if state.region == "saudi" else INDIA_PROMPT
    else:
        prompt_template = GENERIC_PROMPT
    ## updated_scores = []
    for c, sc in zip(state.candidates, state.scored_candidates):
        prompt = prompt_template.format(
            name=safe_text(c.name, 100),
            experience=safe_text(c.experience, 1500),
            signals=sc.signals
        )
        response  = model8B.invoke(prompt)
        reasoning = response.content.strip()

        sc.llm_reasoning = reasoning

    return state

## GOAL of this - sc.llm_reasoning = reasoning
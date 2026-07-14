from models import AgentState
from nodes.analysis import model   # reuse existing LLM

DECIDE_PROMPT = """
You are an expert recruiter. Decide the best processing mode for this Job Description.

- "specialized" → if the JD is clearly for Saudi Arabia, or mentions Vision 2030 / GCC / India Hyderabad startup-heavy role .
- "generic"     → for any other country or company (USA, UK, Singapore, Europe, remote, etc.)

Return ONLY one word: specialized or generic

Job Description:
{jd}

Mode:"""

def decide_mode(state: AgentState) -> AgentState:
    prompt = DECIDE_PROMPT.format(jd=state.jd[:2000])
    # response = model.invoke(prompt)
    # decision = response.content.strip().lower()
    decision = "generic"

    state.mode = "specialized" if "specialized" in decision else "generic"
    return state

from models import AgentState

# Return 5 candidate objects only
def rank_candidates(state: AgentState) -> AgentState:
    state.scored_candidates.sort(key=lambda x: x.score, reverse=True)
    state.scored_candidates = state.scored_candidates[:5]
    return state


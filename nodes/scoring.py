from models import AgentState, ScoreCard, Candidate

from tag_scores import SAUDI_TAG_SCORES, INDIA_TAG_SCORES

def score_candidate(candidate: Candidate, region: str) -> ScoreCard:
    tag_map = SAUDI_TAG_SCORES if region == "saudi" else INDIA_TAG_SCORES

    score   = 0.0
    signals = []

    for tag, (label, points) in tag_map.items():
        if tag in candidate.tags:
            score   += points
            signals.append(f"{label} (+{points})")

    max_possible = sum(pts for _, pts in tag_map.values())
    normalised   = round((score / max_possible) * 10, 2)
    fit          = "strong" if normalised >= 6 else "moderate" if normalised >= 3 else "weak"

    return ScoreCard(
        name=candidate.name,
        linkedin_url=candidate.linkedin_url,
        region=region,
        score=normalised,
        signals=signals,
        llm_reasoning="",
        fit=fit,
    )


def scoring_node(state: AgentState) -> AgentState:
    state.scored_candidates = [
        score_candidate(c, state.region) for c in state.candidates
    ]
    return state
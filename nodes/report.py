from models import AgentState

def generate_report(state: AgentState) -> AgentState:
    print(f"\n{'='*60}")
    print(f"  TOP CANDIDATES — {state.region.upper()} ROLE")
    print(f"{'='*60}")
    for i, sc in enumerate(state.scored_candidates, 1):
        print(f"\n{i}. {sc.name}")
        print(f"   Score  : {sc.score}/10  |  Fit: {sc.fit.upper()}")
        print(f"   Signals: {', '.join(sc.signals) or 'none'}")
        print(f"   LLM    : {sc.llm_reasoning[:200]}...")
        
    return state
from flask import Flask, render_template, request
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from models import AgentState
from nodes.parse_jd import parse_jd
from nodes.fetch import fetch_candidates
from nodes.normalize import normalize_data
from nodes.scoring import scoring_node
from nodes.analysis import cultural_analysis
from nodes.rank import rank_candidates
from nodes.report import generate_report
from nodes.decide_mode import decide_mode
from nodes.extract_apify_params import extract_apify_params
from nodes.generate_tag_scores import generate_tag_scores


load_dotenv()

app = Flask(__name__)


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("decide_mode", decide_mode)
    builder.add_node("parse_jd", parse_jd)
    builder.add_node("extract_apify_params", extract_apify_params)
    builder.add_node("generate_tag_scores", generate_tag_scores)
    builder.add_node("fetch", fetch_candidates)
    builder.add_node("normalize", normalize_data)
    builder.add_node("score", scoring_node)
    builder.add_node("analyze", cultural_analysis)
    builder.add_node("rank", rank_candidates)
    builder.add_node("report", generate_report)

    builder.set_entry_point("decide_mode")

    # Conditional routing based on LLM decision
    builder.add_conditional_edges(
        "decide_mode",
        lambda state: state.mode,
        {
            "specialized": "parse_jd",
            "generic": "extract_apify_params"
        }
    )

    # Specialized path
    builder.add_edge("parse_jd",  "fetch")
    
    # Generic path
    builder.add_edge("extract_apify_params", "generate_tag_scores")
    builder.add_edge("generate_tag_scores", "fetch")
    
    # Common path
    builder.add_edge("fetch",     "normalize")
    builder.add_edge("normalize", "score")
    builder.add_edge("score",     "analyze")
    builder.add_edge("analyze",   "rank")
    builder.add_edge("rank",    "report")
    builder.add_edge("report",    END)

    return builder.compile()


graph = build_graph()

# to show graph
@app.route("/graph")
def show_graph():
    png_bytes = graph.get_graph().draw_mermaid_png()
    return png_bytes, 200, {'Content-Type': 'image/png'}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jd = request.form.get("jd", "").strip()
        if not jd:
            return render_template("index.html", error="Please enter a Job Description")

        final_state = graph.invoke(AgentState(jd=jd))

        # graph.invoke returns a dict — pull what the template needs
        return render_template(
            "index.html",
            candidates=final_state["scored_candidates"],
            region=final_state["region"].upper() if final_state.get("region") else "GLOBAL",
            jd=jd,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    

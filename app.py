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

load_dotenv()

app = Flask(__name__)


def detect_region(state: AgentState) -> AgentState:
    jd_lower = state.jd.lower()
    if not state.region:
        if any(w in jd_lower for w in ["saudi", "riyadh", "gcc"]):
            state.region = "saudi"
        else:
            state.region = "india"
    return state


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("parse_jd",  parse_jd)
    builder.add_node("fetch",     fetch_candidates)
    builder.add_node("normalize", normalize_data)
    builder.add_node("detect",    detect_region)
    builder.add_node("score",     scoring_node)
    builder.add_node("analyze",   cultural_analysis)
    builder.add_node("rank",      rank_candidates)
    builder.add_node("report",    generate_report)

    builder.set_entry_point("parse_jd")
    builder.add_edge("parse_jd",  "fetch")
    builder.add_edge("fetch",     "normalize")
    builder.add_edge("normalize", "detect")
    builder.add_edge("detect",    "score")
    builder.add_edge("score",     "analyze")
    builder.add_edge("analyze",   "rank")
    builder.add_edge("report",    END)

    return builder.compile()


graph = build_graph()


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
            region=final_state["region"].upper(),
            jd=jd,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
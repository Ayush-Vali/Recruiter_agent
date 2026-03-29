# 🚀 Cross-Border Recruiter Agent

**Intelligent AI Recruiter for Saudi Arabia & India**

An autonomous LangGraph agent that takes any Job Description (JD), intelligently extracts the job title and region, scrapes relevant LinkedIn profiles via Apify, applies rich region-specific tagging, scores candidates, adds cultural LLM reasoning, and returns the **Top 5 best-fit candidates** with LinkedIn URLs and detailed Fit ScoreCards.

Built for the "Cross-Border Recruiter Agent" assignment.

---

## ✨ Features

- Paste **any** full Job Description
- Smart JD parsing (`parse_jd` node): regex + LLM fallback for job title, region detection, and location hint (Hyderabad priority, etc.)
- Dynamic LinkedIn sourcing via Apify with title variants
- Rich tagging system in `normalize`:
  - Saudi: Vision 2030 projects, NEOM, GCC experience, Aramco/SABIC, Arabic, government
  - India: Known unicorns, funded startups, 0-to-1, high-scale, Hyderabad-specific, product-type companies
- Tag-based scoring (0–10) with human-readable signals
- Llama-3.3-70B cultural fit reasoning (region-specific prompts)
- Clean ScoreCard: Name, LinkedIn URL, Score, Signals, LLM Reasoning, Fit level
- Simple Flask web UI + CLI version

---

## 🛠️ Tech Stack

- **Agent Framework**: LangGraph
- **Data Models**: Pydantic (`AgentState`, `Candidate`, `ScoreCard`)
- **Scraping**: Apify LinkedIn Profile Search Actor
- **LLM**: meta-llama/Llama-3.3-70B-Instruct (Hugging Face)
- **Web**: Flask
- **State**: `jd_title` + `jd_location_hint` for smarter fetching/scoring

---

## 🚀 Getting Started

1. Install dependencies
```bash
pip install flask pydantic apify-client langgraph langchain-huggingface python-dotenv
```
---
## 📌 Environment Variables
2. Create a `.env` file and configure:
```ini
APIFY_TOKEN=your_apify_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

---
## Run the web app

3. Run 
```
python app.py
```
---

# 🧩 How It Works (Node Flow)

| Node      | What It Does                                                       |
|-----------|--------------------------------------------------------------------|
| parse_jd  | Regex + LLM extracts job title, detects region, sets location hint |
| fetch     | Builds smart Apify query using title variants + region keywords    |
| normalize | Cleans raw JSON, flattens experience, computes rich tags           |
| detect    | Fallback region confirmation                                       |
| score     | Tag-based scoring (0–10) + signals                                 |
| analyze   | LLM adds cultural/regional fit reasoning                           |
| rank      | Sorts and keeps Top 5                                              |
| report    | Outputs final ScoreCards                                           |

---
# 📁 Project Structure
```
recruiter_agent/
├── app.py
├── models.py
├── tag_scores.py
├── prompts.py
├── nodes/
│   ├── parse_jd.py
│   ├── fetch.py
│   ├── normalize.py
│   ├── scoring.py
│   ├── analysis.py
│   ├── rank.py
│   └── report.py
├── templates/index.html
└── .env
```



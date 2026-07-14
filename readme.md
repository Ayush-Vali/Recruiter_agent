# 🚀 Cross-Border Recruiter Agent

**Universal AI Recruiter Agent — Works for Any Country & Company**

An intelligent **LangGraph agent** that takes **any Job Description (JD)**, intelligently decides the best processing strategy, dynamically extracts Apify search parameters, scrapes LinkedIn profiles, applies either rich region-specific tagging (for Saudi Arabia & India) **or LLM-generated scoring rules** (for any other country/company), performs cultural/technical analysis, and returns the **Top 5 best-fit candidates** with LinkedIn URLs and detailed Fit ScoreCards.

Built for the "Cross-Border Recruiter Agent" assignment with strong emphasis on scalability and universality.

---

## ✨ Features

- **Universal JD Support**: Works with JDs from **any country or company** (Saudi, India, USA, UK, Europe, Remote, etc.)
- **Hybrid Agentic Design**: LLM decides between **Specialized Mode** (rich hardcoded logic for Saudi/India) and **Generic Mode** (fully dynamic LLM-generated rules)
- **Smart Parameter Extraction**: LLM dynamically builds optimal Apify search parameters (`searchQuery`, `locations`, `currentJobTitles`)
- **Dynamic Scoring System**: For generic JDs, LLM creates custom scoring rules + tags tailored to the specific JD
- **Rich Specialized Logic** (Saudi & India):
  - Vision 2030 / NEOM / GCC projects
  - Hyderabad priority, Indian unicorns, 0-to-1, high-scale, funded startups
- **Cultural Fit Analysis** using Llama-3.3-70B with region-aware prompts
- **Clean Output**: Top 5 candidates with LinkedIn URLs, normalized 0–10 scores, human-readable signals, and LLM reasoning
- **Simple Flask Web UI** for real-time interaction

---

## 🛠️ Tech Stack

- **Agent Framework**: LangGraph (structured agentic workflow)
- **Data Models**: Pydantic
- **Scraping**: Apify LinkedIn Profile Search Actor
- **LLM**: meta-llama/Llama-3.3-70B-Instruct via Hugging Face
- **Web Interface**: Flask
- **Dynamic Reasoning**: LLM for mode selection, parameter extraction, and custom scoring rules

---

## 🚀 Getting Started

1. **Install dependencies**
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
Open http://127.0.0.1:5000
---

# 🧩 How It Works (Node Flow)

|         Node         |                             What It Does                             |
|:--------------------:|:--------------------------------------------------------------------:|
| decide_mode          | LLM decides: Specialized (Saudi/India) vs Generic (any other)        |
| parse_jd             | Extracts job title, region, and location hint (Specialized path)     |
| extract_apify_params | LLM generates optimal Apify search parameters (Generic path)         |
| generate_tag_scores  | LLM creates custom scoring rules & tags (Generic path)               |
| fetch                | Scrapes LinkedIn profiles using Apify (dynamic or specialized query) |
| normalize            | Cleans data + applies either rich hardcoded tags or dynamic rules    |
| score                | Computes 0–10 score using dynamic or static tag map                  |
| analyze              | LLM adds detailed cultural & role-fit reasoning                      |
| rank                 | Sorts and selects Top 5 candidates                                   |
| report               | Generates final recruiter-ready ScoreCards                           | 
---
# 📁 Project Structure
```
recruiter_agent/
├── app.py
├── models.py
├── tag_scores.py
├── prompts.py
├── nodes/
│   ├── decide_mode.py
│   ├── parse_jd.py
│   ├── extract_apify_params.py
│   ├── generate_tag_scores.py
│   ├── fetch.py
│   ├── normalize.py
│   ├── scoring.py
│   ├── analysis.py
│   ├── rank.py
│   └── report.py
├── templates/index.html
└── .env
```



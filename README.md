# ORACLE — Multi-agent decision-making backend (architecture only)

This repository contains a production-ready, modular scaffold for ORACLE — a
multi-agent decision-making system. This initial commit provides the project
structure, configuration, and lightweight FastAPI health endpoint. No business
logic, RAG, memory, evaluation, or agent internals are implemented yet.

Quick start

1. Copy [.env.example](.env.example) to `.env` and set `OPENAI_API_KEY`.
2. Create a virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app (make sure `ai/src/` is on `PYTHONPATH`, the project keeps source and venv inside `ai/`):

```bash
# create a venv inside the ai/ folder and activate it
python -m venv ai/.venv
source ai/.venv/bin/activate
pip install -r requirements.txt

# run the dev server
PYTHONPATH=ai/src uvicorn oracle.api.main:app --reload --port 8000
```

Project layout and reasons

Refer to the `src/oracle` package for the main application scaffolding.
# 🧠 ORACLE – AI Deliberation Engine

ORACLE is a multi-agent AI decision support system that simulates expert deliberation before making complex decisions.

Instead of relying on a single AI response, ORACLE assigns specialized AI agents to analyze a problem from different perspectives. Their opinions are evaluated by a Judge Agent, producing a transparent, explainable, and balanced final decision.

---

## ✨ Features

- 🤖 Multi-Agent Decision Making
- 🌍 Climate Impact Analysis
- 💰 Economic Analysis
- ❤️ Health Impact Assessment
- 👥 Citizen Perspective
- ⚖️ Ethics Evaluation
- 🧑‍⚖️ Judge Agent for Final Decision
- 📖 Explainable AI (XAI)
- 📊 Confidence Score
- 🔄 What-If Scenario Analysis
- 📈 Decision Simulation
- 🧠 Decision Memory
- 📚 Retrieval-Augmented Generation (RAG)
- 📡 Live Data Integration

---

## 🏗️ Architecture

```
User
   │
   ▼
Problem Analysis
   │
   ▼
LangGraph Orchestrator
   │
   ├── Climate Agent
   ├── Economy Agent
   ├── Health Agent
   ├── Citizen Agent
   ├── Ethics Agent
   └── Scientist Agent
            │
            ▼
     Deliberation Engine
            │
            ▼
       Judge Agent
            │
            ▼
 Explainability + Confidence
            │
            ▼
     Final Recommendation
```

---

## 🛠️ Tech Stack

### AI

- LangGraph
- LangChain
- OpenAI GPT
- RAG
- ChromaDB (or Qdrant)
- Python

### Backend

- FastAPI
- Pydantic

### Frontend

- React
- Tailwind CSS

---

## 📂 Project Structure

```
oracle-ai/

├── app/
│
├── agents/
│
├── graph/
│
├── state/
│
├── prompts/
│
├── rag/
│
├── memory/
│
├── evaluation/
│
├── api/
│
├── services/
│
└── utils/
```

---

## 🚀 Workflow

1. User submits a decision-making problem.
2. LangGraph orchestrates all expert agents.
3. Each agent analyzes the problem from its own domain.
4. Agents deliberate using previous opinions.
5. Judge Agent evaluates all arguments.
6. ORACLE generates:
   - Final decision
   - Explanation
   - Confidence score
   - Risk assessment
   - Alternative solutions
   - Stakeholder analysis
   - Future simulation

---

## 🎯 Example

### Input

```
Should the government build a new factory in City A?
```

### Output

```
Decision:
Approve with Conditions

Reason:
- High economic benefit
- Moderate environmental risk
- Install emission filters
- Use renewable energy

Confidence:
89%

Risks:
Medium

Alternative:
Build in Site B
```

---

## 📌 Roadmap

- [ ] Multi-Agent Workflow
- [ ] Judge Agent
- [ ] RAG Integration
- [ ] Long-Term Memory
- [ ] Evaluation Engine
- [ ] Simulation Engine
- [ ] Live Data APIs
- [ ] Frontend Dashboard

---

## 📜 License

MIT License
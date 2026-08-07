# ORACLE — Agent Rules & Architecture Guide

> This file is the source of truth for any AI coding agent working on this project.
> Read it fully before writing a single line of code.

---

## What Is ORACLE?

ORACLE is a **multi-agent AI deliberation platform** built with **LangGraph + LangChain + OpenAI GPT-4o**.

It does NOT generate simple answers.
It simulates a **council of domain experts** that independently analyze a scenario, deliberate, and produce a transparent, evidence-based recommendation.

---

## Project Structure (DO NOT deviate from this)

```
src/oracle/
├── agents/          ← All agent logic lives here
├── api/             ← FastAPI endpoints only
├── evaluation/      ← Evaluation/testing logic
├── graph/           ← LangGraph graph definition
├── memory/          ← Memory/RAG logic
├── models/          ← Pydantic models / schemas
├── prompts/         ← System prompt strings (optional separate files)
├── rag/             ← Retrieval-Augmented Generation
├── services/        ← External service integrations
├── state/           ← OracleState TypedDict
├── tools/           ← LangChain @tool definitions
├── utils/           ← Shared utilities
├── config.py        ← All config and env vars
└── __init__.py
```

**Rules:**
- Every new file goes inside `src/oracle/` in the correct subfolder
- Never create files in the project root unless they are config files (`.env`, `requirements.txt`, etc.)
- Never create a new folder that doesn't exist in the structure above without asking first

---

## Tech Stack (LOCKED — do not substitute)

| Layer | Technology |
|---|---|
| Orchestration | LangGraph (StateGraph) |
| LLM Framework | LangChain |
| LLM Model | OpenAI GPT-4o (`gpt-4o`) |
| API | FastAPI |
| State | TypedDict (OracleState) |
| Tools | LangChain `@tool` decorator |
| External APIs | OpenWeatherMap, Tavily Search |
| Config | python-dotenv via `config.py` |

**Never use:** CrewAI, AutoGen, raw OpenAI SDK (use LangChain wrapper), hardcoded API keys.

---

## The Agents (8 total)

### Stage 1 — Input Processing
| Agent | File | Role |
|---|---|---|
| Scenario Analyzer | `agents/scenario_analyzer.py` | Parses user input, extracts topic/domain/complexity/relevant experts |

### Stage 2 — Expert Council (run in PARALLEL)
| Agent | File | Domain |
|---|---|---|
| Climate Agent | `agents/climate_agent.py` | Climate, environment, emissions |
| Economy Agent | `agents/economy_agent.py` | Economic impact, cost, growth |
| Health Agent | `agents/health_agent.py` | Public health, safety, medical |
| Citizen Agent | `agents/citizen_agent.py` | Social impact, equity, public opinion |
| Ethics Agent | `agents/ethics_agent.py` | Ethical implications, fairness, rights |
| Scientist Agent | `agents/scientist_agent.py` | Scientific evidence, data, research |

### Stage 3 — Deliberation
| Agent | File | Role |
|---|---|---|
| Deliberation Engine | `agents/deliberation_engine.py` | Finds agreements/disagreements, decides if re-iteration needed |
| Judge Agent | `agents/judge_agent.py` | Synthesizes final balanced verdict |

### Stage 4 — Output
| Agent | File | Role |
|---|---|---|
| Explainability Agent | `agents/explainability_agent.py` | Produces transparent human-readable explanation |

---

## Shared State (OracleState)

All agents read from and write to ONE shared state object. Never pass data between agents directly.

```python
class OracleState(TypedDict):
    user_input: str
    scenario_analysis: dict        # set by Scenario Analyzer
    expert_opinions: dict          # keyed by agent name, set by Expert Agents
    consensus: dict                # set by Deliberation Engine
    iteration_count: int           # managed by graph
    max_iterations: int            # default: 3
    needs_iteration: bool          # set by Deliberation Engine
    judge_verdict: dict            # set by Judge Agent
    explanation: dict              # set by Explainability Agent
    final_response: str            # set last, returned to user
    messages: list                 # LangGraph internal messages
```

**Rules:**
- Every agent function signature: `def agent_name(state: OracleState) -> OracleState`
- Every agent returns the full state with only its own field updated
- Never mutate state directly — return a new dict with updated fields

---

## Expert Agent Output Format

Every expert agent must return its opinion in this exact structure:

```python
{
    "analysis": str,            # detailed analysis paragraph
    "key_risks": list[str],     # 3-5 bullet risks
    "recommendations": list[str], # 3-5 actionable recommendations
    "confidence": float,        # 0.0 to 1.0
    "stance": str,              # "support" | "oppose" | "neutral"
    "evidence_used": list[str]  # sources or tool results referenced
}
```

---

## LangGraph Flow (DO NOT change the order)

```
START
  ↓
scenario_analyzer
  ↓
[PARALLEL via Send()]
  climate_agent, economy_agent, health_agent,
  citizen_agent, ethics_agent, scientist_agent
  ↓
deliberation_engine
  ↓
[CONDITIONAL EDGE]
  needs_iteration AND iteration_count < max_iterations?
    → YES: back to parallel experts (new round)
    → NO: continue
  ↓
judge_agent
  ↓
explainability_agent
  ↓
END
```

---

## Tools

Tools live in `src/oracle/tools/` and use LangChain `@tool` decorator.

| Tool | File | Used By |
|---|---|---|
| `get_weather_data` | `tools/weather_tool.py` | Climate Agent |
| `search_latest_data` | `tools/search_tool.py` | All experts |

**Rules:**
- All API keys come from `config.py` — never hardcode
- Tools must handle errors gracefully and return a fallback string if API fails
- Tools return structured dicts, not raw strings

---

## Config Rules

- All secrets and API keys live in `.env` and are accessed via `config.py`
- Required env vars:
  - `OPENAI_API_KEY`
  - `OPENWEATHER_API_KEY`
  - `TAVILY_API_KEY`
- Never access `os.environ` directly in agent files — always import from `config.py`

---

## Code Style Rules

- Python 3.11+
- Type hints on every function
- Docstring on every agent function (one line is enough)
- No print statements — use Python `logging`
- No TODO comments in final code
- Keep each agent file focused — no business logic outside its responsibility

---

## What ORACLE Is NOT

- ❌ Not a chatbot
- ❌ Not a simple Q&A system
- ❌ Not a single-agent system
- ❌ Does not return the first answer it generates
- ❌ Does not skip the deliberation step

---

## When In Doubt

1. Check this file first
2. Check `state/state.py` for the data contract
3. Check `graph/oracle_graph.py` for the flow
4. Ask before creating new files or changing the architecture

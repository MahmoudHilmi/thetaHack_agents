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
     #############################
reda@reda-HP-EliteBook-840-G3:~$ curl -s http://127.0.0.1:8001/decide \
  -H 'Content-Type: application/json' \
  -d '{"problem_description":"هل يتم تحويل أتوبيسات القاهرة إلى كهرباء؟","user_input":"الميزانية محدودة والأولوية للصحة وجودة الخدمة.","memory_scope":"my-test"}' | python3 -m json.tool
{
    "final_decision": "Proceed with a phased, equity-first electrification of Cairo's public bus fleet, beginning with a rigorously monitored pilot phase (500 buses on 3 highest-pollution, highest-ridership corridors) contingent on five legally binding pre-conditions: (1) concessional climate finance covering 100% of FX-denominated capex at <4% USD with 15+ year tenor; (2) a legislative ring-fence guaranteeing operational savings prevent fare hikes and fund a Just Transition Fund (1% of capex); (3) enforceable grid decarbonization PPAs matching new e-bus load with additional renewable capacity; (4) a worker retraining/placement guarantee codified in labor law with union co-governance; (5) a participatory oversight board with veto power on depot siting, fare changes, and corridor sequencing. Full fleet conversion proceeds only after pilot validates >220 km/day utilization, >98% charging reliability, and maintenance cost curves within modeled ranges.",
    "decision_reasoning": "The expert perspectives converge on a strong consensus: electrification delivers net positive benefits across climate (50\u201385% lifecycle emissions reduction), health (primary prevention against Cairo's top environmental killer), economy (positive NPV, 65% OPEX reduction, fuel import savings), and ethics (distributive justice for transit-dependent populations, intergenerational duty). The tensions are not about *whether* but *how*. The Climate and Health experts correctly identify the urgency\u2014diesel exhaust is a Group 1 carcinogen killing thousands annually\u2014but the Economy, Citizen, and Ethics experts rightly warn that rushing without solving financing (FX risk), grid cleanup (currently 90% non-renewable), and social justice (worker retraining/placement guarantee) would undermine the initiative's long-term success.",
    "final_confidence": 0.85,
    "climate_analysis": "**Analysis of the Decision to Convert Cairo's Public Bus Fleet to Electric**\n\n**1. Direct Climate Impact**\n\nThe conversion of Cairo's public bus fleet to electric vehicles (EVs) would significantly reduce direct greenhouse gas (GHG) emissions. Diesel buses emit approximately 220 grams of CO2 per passenger kilometer, whereas electric buses would emit around 20-50 grams of CO2 per passenger kilometer, depending on the source of electricity. This reduction would translate to a 90-95% decrease in GHG emissions from the bus fleet.\n\n**2. Long-term Environmental Consequences**\n\nThe transition to electric buses would also mitigate long-term environmental consequences, such as air pollution and climate change. The reduced emissions would lead to improved air quality, with estimated annual health savings of $1.5-2.5 billion. Moreover, the conversion would support Egypt's Nationally Determined Contribution (NDC) under the Paris Agreement, contributing to the country's climate change mitigation goals.\n\n**3. Carbon Footprint Implications and Lifecycle Emissions**\n\nA lifecycle assessment would reveal that electric buses have a lower carbon footprint than diesel buses. The carbon footprint of EVs is primarily influenced by the source of electricity used for charging. If the electricity is generated from renewable sources, such as solar or wind power, the carbon footprint would be significantly reduced. According to the International Energy Agency (IEA), the average carbon intensity of electricity in Egypt is around 550 grams of CO2 per kilowatt-hour (kWh). However, if the electricity is sourced from renewable energy, the carbon intensity would be close to zero.\n\n**4. Biodiversity Considerations**\n\nThe conversion of the bus fleet to electric vehicles would not have a direct impact on biodiversity. However, the transition to renewable energy sources, such as solar or wind power, would support the development of sustainable energy infrastructure, which could have indirect benefits for biodiversity.\n\n**5. Renewable vs. Non-renewable Resource Usage**\n\nTo minimize the carbon footprint of electric buses, it is essential to ensure that the electricity used for charging comes from renewable sources. Egypt has significant renewable energy resources, including solar and wind power, which can be leveraged to power the electric bus fleet. This would support the country's transition to a low-carbon economy and reduce reliance on non-renewable energy sources.\n\n**6. Potential for Climate Adaptation or Mitigation**\n\nThe conversion of Cairo's public bus fleet to electric vehicles has the potential to contribute significantly to climate adaptation and mitigation efforts. By reducing GHG emissions, the transition would support Egypt's climate change mitigation goals and contribute to the country's efforts to adapt to the impacts of climate change.\n\n**Recommendations**\n\n1. Ensure that the electricity used for charging electric buses comes from renewable sources, such as solar or wind power.\n2. Implement a phased, equity-first electrification of the bus fleet, beginning with a pilot phase on highest-pollution, highest-ridership corridors.\n3. Secure concessional climate finance to cover 100% of FX-denominated capital expenditures.\n4. Establish a legislative ring-fence to guarantee operational savings and prevent fare hikes.\n5. Implement a participatory governance structure with citizen oversight to ensure that the transition is equitable and just.\n\nBy following these recommendations, the conversion of Cairo's public bus fleet to electric vehicles can be a successful example of climate adaptation and mitigation in action.",
    "economy_analysis": "**Economic Impact Analysis of Electrifying Cairo's Public Bus Fleet**\n\n**1. Cost Implications and Budget Impact**\n\n* Initial investment: Estimated $1.2 billion - $1.8 billion for the phased conversion of 5,000 buses, including the purchase of electric buses, charging infrastructure, and grid upgrades.\n* Operating costs: 65% reduction in fuel costs (estimated $800 million - $1.2 billion annually) and lower maintenance costs (estimated 10% - 15% reduction).\n* Budget impact: The reduced fuel costs and operational savings will lead to a decrease in the city's transportation budget, potentially allowing for reallocation of funds to other areas.\n\n**2. Revenue and Profit Impact**\n\n* Increased ridership: Estimated 10% - 15% increase in ridership due to the improved air quality and reduced travel times.\n* Fare revenue: Estimated 5% - 10% increase in fare revenue due to the increased ridership.\n* Profit impact: The reduced operating costs and increased revenue will lead to a significant increase in profitability for the public transportation system.\n\n**3. Market Effects (Competition, Market Share, Pricing)**\n\n* Market competition: The electrification of the public bus fleet will increase competition for private transportation services, potentially leading to a reduction in private transportation usage.\n* Market share: The public transportation system will gain market share due to its improved air quality and reduced travel times.\n* Pricing: The reduced operating costs and increased revenue will allow for potential fare reductions, making public transportation more attractive to users.\n\n**4. Employment Consequences (Jobs Created/Lost, Wages, Labor Market)**\n\n* Job creation: Estimated 1,000 - 2,000 new jobs in the manufacturing, installation, and maintenance of electric buses and charging infrastructure.\n* Job loss: Estimated 1,000 - 2,000 jobs lost in the diesel bus maintenance sector.\n* Wages: The new jobs created will likely have higher wages than the jobs lost, potentially leading to an increase in the average wage in the transportation sector.\n* Labor market: The electrification of the public bus fleet will lead to a shift in the labor market, with a greater emphasis on skilled workers in the electric bus maintenance sector.\n\n**5. ROI and Financial Sustainability**\n\n* ROI: Estimated 10% - 15% return on investment due to the reduced operating costs and increased revenue.\n* Financial sustainability: The electrification of the public bus fleet will lead to a significant reduction in operating costs, making the system more financially sustainable in the long term.\n\n**6. Macroeconomic Effects (GDP, Inflation, Growth)**\n\n* GDP: Estimated 0.5% - 1% increase in GDP due to the reduced fuel costs and increased economic activity.\n* Inflation: Estimated 0.2% - 0.5% decrease in inflation due to the reduced fuel costs and lower transportation costs.\n* Growth: The electrification of the public bus fleet will lead to increased economic activity and growth, potentially leading to a 1% - 2% increase in GDP growth.\n\n**7. Supply Chain Implications**\n\n* Supply chain risks: The electrification of the public bus fleet will lead to a shift in the supply chain, with a greater emphasis on electric bus manufacturers and charging infrastructure providers.\n* Supply chain opportunities: The electrification of the public bus fleet will create opportunities for new businesses and industries, including electric bus manufacturers and charging infrastructure providers.\n\nOverall, the electrification of Cairo's public bus fleet will have a positive economic impact, with reduced operating costs, increased revenue, and improved profitability. The project will also create new jobs and opportunities in the electric bus maintenance sector, while reducing the city's reliance on diesel fuel and improving air quality.",
    "health_analysis": "**Analysis of the Decision to Convert Cairo's Public Bus Fleet to Electric**\n\n**1. Direct Health Effects and Medical Outcomes:**\n\n* The primary air pollutant of concern is particulate matter (PM2.5), which is a Group 1 carcinogen. Diesel exhaust is responsible for thousands of premature deaths annually in Cairo.\n* Electric buses emit zero tailpipe emissions, reducing PM2.5 and other air pollutants, which in turn decrease the risk of respiratory diseases, cardiovascular diseases, and cancer.\n* A study estimates that converting Cairo's bus fleet to electric could avoid 300-600 premature deaths per year, with a corresponding health savings of $1.5-2.5 billion annually.\n\n**2. Public Health Implications (Disease Prevention, Epidemics):**\n\n* Reducing PM2.5 exposure can prevent 2-3% of all-cause mortality and 1-2% of all respiratory disease hospitalizations.\n* Electric buses can help prevent the spread of respiratory diseases, such as asthma and chronic obstructive pulmonary disease (COPD), particularly among vulnerable populations, including children, older adults, and those with pre-existing respiratory conditions.\n* A well-planned electrification strategy can also reduce the risk of heat-related illnesses and mortality, particularly during heatwaves.\n\n**3. Healthcare System Impact (Resources, Accessibility, Capacity):**\n\n* The reduction in air pollution-related illnesses can alleviate pressure on Cairo's healthcare system, allowing for more efficient allocation of resources.\n* Electric buses can also reduce the burden on emergency services and hospitals, resulting in cost savings and improved healthcare outcomes.\n* The implementation of a Just Transition Fund can support workers in the transportation sector, ensuring they have access to training and reemployment opportunities, thereby reducing the social and economic costs of transition.\n\n**4. Population-Level Consequences (Vulnerable Groups, Equity):**\n\n* The benefits of electric buses will be most pronounced among vulnerable populations, including children, older adults, and those with pre-existing respiratory conditions.\n* A well-planned electrification strategy can ensure that the benefits are equitably distributed, particularly in low-income and marginalized communities.\n* The participatory governance structure and citizen oversight can help ensure that the needs of all stakeholders are taken into account, promoting equity and social justice.\n\n**5. Long-term Health Outcomes and Quality of Life:**\n\n* The long-term health benefits of electric buses can be significant, with estimates suggesting a 5-10% reduction in all-cause mortality and a 2-5% reduction in all respiratory disease hospitalizations.\n* Improved air quality can also enhance quality of life, with increased opportunities for outdoor activities and reduced risk of heat-related illnesses.\n\n**6. Mental Health and Psychological Impacts:**\n\n* The mental health benefits of electric buses can be substantial, with reduced exposure to air pollution and noise pollution contributing to improved mental well-being.\n* A well-designed electrification strategy can also promote a sense of community and social cohesion, particularly through participatory governance and citizen engagement.\n\n**7. Preventive vs. Reactive Health Measures:**\n\n* Electric buses represent a proactive approach to public health, reducing the risk of air pollution-related illnesses and improving overall health outcomes.\n* By investing in a Just Transition Fund and participatory governance, the healthcare system can focus on preventive measures, rather than reacting to the consequences of air pollution.\n\nIn conclusion, the decision to convert Cairo's public bus fleet to electric is a critical step towards improving public health outcomes, reducing healthcare costs, and promoting equity and social justice. A well-planned electrification strategy can ensure that the benefits are equitably distributed, particularly among vulnerable populations, and that the transition is managed in a way that supports workers and the community.",
    "citizen_perspective": "**Public Perception and Sentiment**\n\nThe general public in Cairo is likely to be in favor of converting the city's public bus fleet to electric, driven by growing concerns about air pollution, climate change, and public health. A survey conducted among ordinary citizens would show a significant majority (around 70-80%) in support of the initiative, citing improved air quality, reduced noise pollution, and increased energy efficiency as key benefits.\n\n**Daily Life Impact for Ordinary Citizens**\n\nThe conversion to electric buses would likely have a positive impact on daily life for ordinary citizens:\n\n* Reduced air pollution would lead to fewer respiratory problems, especially among vulnerable populations like children and the elderly.\n* Electric buses would be quieter, providing a more pleasant commuting experience.\n* The reduced noise pollution would also lead to improved quality of life for residents living near bus corridors.\n* However, there might be initial concerns about the reliability of electric bus charging infrastructure, potential delays, or increased fares to offset the higher upfront costs.\n\n**Social Justice Implications**\n\nThe conversion to electric buses would have significant social justice implications:\n\n* The initiative would disproportionately benefit low-income and marginalized communities, who are often the most affected by air pollution.\n* Electric buses would reduce health disparities, as those living in areas with high air pollution exposure would experience fewer health problems.\n* However, there might be concerns about job displacement among bus drivers and mechanics, requiring a just transition plan to ensure fair treatment and retraining opportunities.\n\n**Community Effects**\n\nThe conversion to electric buses would have a positive impact on community cohesion and local effects:\n\n* Improved air quality would lead to increased community engagement and participation in outdoor activities.\n* The initiative would create new economic opportunities, such as the development of electric bus charging infrastructure and related services.\n* However, there might be concerns about the potential disruption of bus routes and schedules, requiring careful planning and communication with local residents.\n\n**Public Trust and Confidence in Institutions**\n\nThe success of the electric bus conversion initiative would depend on the effective implementation of the plan, including:\n\n* Transparent communication about the project's progress and potential challenges.\n* Regular updates on the environmental and health benefits of the initiative.\n* Ensuring that the benefits of the initiative are equitably distributed among all citizens, particularly vulnerable populations.\n* Addressing concerns about job displacement and providing fair treatment and retraining opportunities for affected workers.\n\n**Quality of Life Considerations**\n\nThe conversion to electric buses would significantly improve the quality of life for ordinary citizens in Cairo:\n\n* Reduced air pollution would lead to improved health outcomes and reduced healthcare costs.\n* Electric buses would provide a more pleasant commuting experience, reducing stress and improving overall well-being.\n* The initiative would contribute to a cleaner and healthier environment, enhancing the quality of life for all citizens.\n\n**Access and Inclusivity for All Citizens**\n\nThe electric bus conversion initiative would need to ensure that all citizens have equal access to the benefits of the initiative:\n\n* Providing accessible and affordable electric buses for people with disabilities.\n* Ensuring that the initiative does not disproportionately benefit affluent or middle-class citizens.\n* Addressing concerns about the potential impact on low-income and marginalized communities, who might be most affected by air pollution.\n\nIn conclusion, the conversion to electric buses in Cairo would have a positive impact on public perception, daily life, social justice, community effects, public trust, quality of life, and access and inclusivity for all citizens. However, careful planning, transparent communication, and equitable distribution of benefits are essential to ensure the success of the initiative.",
    "ethics_evaluation": "**Analysis of the Decision: Electrification of Cairo's Public Bus Fleet**\n\n**Moral Principles Involved**\n\n1. **Justice**: The decision involves distributive justice, ensuring that the benefits and costs of electrification are fairly distributed among different groups, particularly transit-dependent populations.\n2. **Compassion**: The electrification of public buses aims to reduce harm to human health and the environment, demonstrating compassion for the well-being of citizens.\n3. **Honesty**: The decision-making process should be transparent, honest, and free from biases, ensuring that all stakeholders are informed and involved in the decision-making process.\n4. **Intergenerational duty**: The decision involves considering the long-term implications of the electrification of public buses, ensuring that the benefits and costs are shared fairly among current and future generations.\n\n**Fairness and Justice Considerations**\n\n1. **Distributive justice**: The decision should ensure that the benefits of electrification are distributed fairly among different groups, particularly transit-dependent populations.\n2. **Procedural justice**: The decision-making process should be transparent, inclusive, and free from biases, ensuring that all stakeholders are involved and informed.\n3. **Retributive justice**: The decision should address the harm caused by diesel exhaust, ensuring that those responsible for the harm are held accountable.\n\n**Rights and Responsibilities**\n\n1. **Individual rights**: Citizens have the right to clean air and a healthy environment, which is being compromised by diesel exhaust.\n2. **Collective rights**: The collective rights of transit-dependent populations, workers, and future generations should be considered in the decision-making process.\n3. **Responsibilities**: The government and other stakeholders have a responsibility to ensure that the electrification of public buses is done in a way that is fair, just, and transparent.\n\n**Potential Harm and Benefits to Different Groups**\n\n1. **Health benefits**: The electrification of public buses will reduce harm to human health and the environment.\n2. **Economic benefits**: The electrification of public buses will create jobs, reduce costs, and promote economic growth.\n3. **Social benefits**: The electrification of public buses will promote social justice, particularly for transit-dependent populations.\n\n**Ethical Frameworks Perspective**\n\n1. **Consequentialist**: The decision should prioritize the outcomes, ensuring that the benefits of electrification outweigh the costs.\n2. **Deontological**: The decision should be guided by rules and duties, ensuring that the electrification of public buses is done in a way that is fair, just, and transparent.\n3. **Virtue ethics**: The decision should prioritize the character of the stakeholders involved, ensuring that the decision-making process is guided by virtues such as honesty, compassion, and fairness.\n4. **Care ethics**: The decision should prioritize relationships and care for the well-being of citizens, particularly transit-dependent populations.\n\n**Transparency and Accountability**\n\n1. **Transparency**: The decision-making process should be transparent, ensuring that all stakeholders are informed and involved.\n2. **Accountability**: The decision-making process should be accountable, ensuring that those responsible for the harm caused by diesel exhaust are held accountable.\n\n**Long-term Ethical Implications**\n\n1. **Intergenerational duty**: The decision should prioritize the long-term implications of the electrification of public buses, ensuring that the benefits and costs are shared fairly among current and future generations.\n2. **Sustainability**: The decision should prioritize sustainability, ensuring that the electrification of public buses is done in a way that is environmentally friendly and sustainable.\n\nIn conclusion, the decision to electrify Cairo's public bus fleet involves complex moral and ethical considerations. The decision should prioritize fairness, justice, and compassion, ensuring that the benefits and costs are shared fairly among different groups. The decision-making process should be transparent, accountable, and guided by virtues such as honesty, compassion, and fairness. The long-term implications of the decision should prioritize sustainability and intergenerational duty.",
    "memory_matches": 3,
    "status": "success"
}
reda@reda-HP-EliteBook-840-G3:~$ 

########################### 


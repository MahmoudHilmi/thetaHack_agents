# ORACLE Prompts

This directory contains all prompt templates used by the ORACLE multi-agent system.

## Files

- **climate_prompt.txt** - Climate and environmental impact analysis
- **economy_prompt.txt** - Economic impact analysis
- **health_prompt.txt** - Health and public health impact analysis
- **citizen_prompt.txt** - Citizen perspective and public opinion
- **ethics_prompt.txt** - Ethical implications analysis
- **judge_prompt.txt** - Judge synthesis of all perspectives
- **loader.py** - Utility module for loading prompts

## Usage

### Option 1: Import Pre-loaded Prompts
```python
from oracle.prompts.loader import CLIMATE_PROMPT, ECONOMY_PROMPT, JUDGE_PROMPT
```

### Option 2: Load Prompt Dynamically
```python
from oracle.prompts.loader import load_prompt
climate = load_prompt('climate')
```

### Option 3: Import from Package
```python
from oracle.prompts import CLIMATE_PROMPT, ECONOMY_PROMPT, HEALTH_PROMPT
```

## Editing Prompts

To modify a prompt, simply edit the corresponding `.txt` file:
1. Open the file (e.g., `climate_prompt.txt`)
2. Edit the prompt template
3. Save the file
4. The changes will be automatically loaded when the agent runs

## Prompt Variables

All prompts use `{problem}` as the main input variable, except for `judge_prompt.txt` which uses:
- `{problem}` - The original problem statement
- `{perspectives}` - Formatted perspectives from all other agents

## Prompt Guidelines

When writing prompts:
1. Be clear about the agent's role and expertise
2. Specify what information should be included in the analysis
3. Provide structure (numbered lists, sections)
4. Include examples when helpful
5. Keep prompts focused and concise
6. Use placeholders like `{problem}` for dynamic content

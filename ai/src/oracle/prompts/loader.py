"""Utility functions for loading prompts from files."""

import os
from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """Load a prompt template from file.
    
    Args:
        prompt_name: Name of the prompt (e.g., 'climate', 'economy', 'judge')
    
    Returns:
        The prompt template as a string
    """
    prompts_dir = Path(__file__).parent
    prompt_file = prompts_dir / f"{prompt_name}_prompt.txt"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


# Load all prompts at module level for efficiency
CLIMATE_PROMPT = load_prompt('climate')
ECONOMY_PROMPT = load_prompt('economy')
HEALTH_PROMPT = load_prompt('health')
CITIZEN_PROMPT = load_prompt('citizen')
ETHICS_PROMPT = load_prompt('ethics')
JUDGE_PROMPT = load_prompt('judge')

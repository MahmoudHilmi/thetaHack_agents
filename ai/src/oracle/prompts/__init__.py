"""ORACLE Prompts Module

Contains all prompt templates for the multi-agent system.
Prompts are stored in separate .txt files for easy editing and management.

Usage:
    from oracle.prompts.loader import CLIMATE_PROMPT, ECONOMY_PROMPT, etc.
    or
    from oracle.prompts.loader import load_prompt
    climate = load_prompt('climate')
"""

from .package_info import DESCRIPTION
from oracle.prompts.loader import (
    load_prompt,
    CLIMATE_PROMPT,
    ECONOMY_PROMPT,
    HEALTH_PROMPT,
    CITIZEN_PROMPT,
    ETHICS_PROMPT,
    JUDGE_PROMPT,
)

__all__ = [
    "DESCRIPTION",
    "load_prompt",
    "CLIMATE_PROMPT",
    "ECONOMY_PROMPT",
    "HEALTH_PROMPT",
    "CITIZEN_PROMPT",
    "ETHICS_PROMPT",
    "JUDGE_PROMPT",
]

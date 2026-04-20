"""AI Cost Tracker - Zero-config AI cost calculator per commit/model with liteLLM."""

from .calculator import ai_cost, estimate_tokens
from .models import PRICES, DEFAULT_MODEL, DEFAULT_OPENROUTER_API_KEY, get_litellm_model_name
from .metrics import calculate_human_time
from .reports.badge import update_readme_badge

__version__ = "0.1.50"
__all__ = [
    "ai_cost", 
    "estimate_tokens", 
    "PRICES", 
    "DEFAULT_MODEL", 
    "DEFAULT_OPENROUTER_API_KEY", 
    "get_litellm_model_name",
    "calculate_human_time",
    "update_readme_badge"
]

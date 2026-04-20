"""Model pricing definitions with liteLLM integration."""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file

if __name__ == "__main__":
    load_dotenv()

# Default configuration from .env
DEFAULT_OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next")

# Model pricing ($/token) - includes liteLLM supported providers
PRICES: Dict[str, Dict[str, float]] = {
    # Anthropic
    "claude-4-sonnet": {"input": 3e-6, "output": 15e-6},
    "anthropic/claude-4-sonnet": {"input": 3e-6, "output": 15e-6},
    "claude-3.5-sonnet": {"input": 3e-6, "output": 15e-6},
    "claude-3.5-haiku": {"input": 0.8e-6, "output": 4e-6},
    "claude-3-opus": {"input": 15e-6, "output": 75e-6},
    "anthropic/claude-3.5-sonnet": {"input": 3e-6, "output": 15e-6},
    "anthropic/claude-3.5-haiku": {"input": 0.8e-6, "output": 4e-6},
    # OpenAI
    "gpt-4o": {"input": 5e-6, "output": 15e-6},
    "gpt-5.4-mini": {"input": 0.15e-6, "output": 0.6e-6},
    "gpt-4": {"input": 30e-6, "output": 60e-6},
    "openai/gpt-4o": {"input": 5e-6, "output": 15e-6},
    "openai/gpt-5.4-mini": {"input": 0.15e-6, "output": 0.6e-6},
    # OpenRouter / Qwen
    "openrouter/qwen/qwen3-coder-next": {"input": 0.5e-6, "output": 1.5e-6},
    "openrouter/qwen/qwen3-coder": {"input": 0.5e-6, "output": 1.5e-6},
    "openrouter/qwen/qwen2.5-coder": {"input": 0.3e-6, "output": 1.0e-6},
    # Ollama / Local
    "ollama": {"input": 1e-7, "output": 1e-7},
    "local": {"input": 1e-7, "output": 1e-7},
    "ollama/*": {"input": 1e-7, "output": 1e-7},
}

def get_model_price(model: str) -> Dict[str, float]:
    """Get pricing for a model, fallback to local if unknown."""
    # Try exact match first
    if model in PRICES:
        return PRICES[model]
    
    # Try provider/model format
    if "/" in model:
        # Check if it's an OpenRouter model
        if model.startswith("openrouter/"):
            return PRICES.get(model, {"input": 0.5e-6, "output": 1.5e-6})
        # Check if it's an Ollama model
        if model.startswith("ollama/"):
            return PRICES["ollama/*"]
    
    # Fallback to local pricing
    return PRICES["local"]


def get_openrouter_headers() -> Dict[str, str]:
    """Get headers for OpenRouter API calls."""
    return {
        "Authorization": f"Bearer {DEFAULT_OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/your-org/ai-cost-tracker",
        "X-Title": "AI Cost Tracker"
    }


def get_litellm_model_name(model: str) -> str:
    """Convert model name to liteLLM format."""
    # If model is already in liteLLM format, return as-is
    if "/" in model:
        return model
    # Default to openrouter if no provider specified
    return f"openrouter/{model}"

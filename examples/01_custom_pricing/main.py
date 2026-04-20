#!/usr/bin/env python3
"""Custom Model Pricing - add custom models or update pricing dynamically."""
from costs.models import PRICES, get_model_price
from costs.calculator import calculate_cost


if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Example: Custom Model Pricing")
    print("=" * 60)

# Show built-in prices
    print("\nBuilt-in prices:")
for model, prices in list(PRICES.items())[:5]:
    print(f"  {model}: input=${prices['input']:.2e}, output=${prices['output']:.2e}")

# Add custom model pricing
    print("\nAdding custom model...")
PRICES["custom/gpt-custom"] = {
    "input": 1.0e-6,   # $1 per million tokens
    "output": 2.0e-6   # $2 per million tokens
}

# Use custom model
custom_price = get_model_price("custom/gpt-custom")
    print(f"Custom model price: input=${custom_price['input']:.2e}, output=${custom_price['output']:.2e}")

# Calculate cost with custom model
tokens = {"input": 1000, "output": 500}
cost = calculate_cost(tokens, "custom/gpt-custom")
    print(f"\nCost for 1000 input + 500 output tokens: ${cost:.6f}")

# Dynamic pricing update
    print("\n" + "-" * 60)
    print("Dynamic pricing update example:")

def update_prices_from_api():
    """Simulate fetching current prices from provider API."""
    latest_prices = {
        "openai/gpt-4o": {"input": 2.5e-6, "output": 10e-6},  # Hypothetical new prices
    }
    
    for model, prices in latest_prices.items():
        PRICES[model] = prices
        print(f"  Updated {model}: input=${prices['input']:.2e}")

    update_prices_from_api()

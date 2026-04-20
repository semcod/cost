#!/usr/bin/env python3
"""Basic Tokenizer Usage - count tokens for different models."""
from costs.tokenizers import Tokenizer, count_tokens

CONSTANT_60 = 60


# Initialize tokenizer
tokenizer = Tokenizer()

# Sample code snippets for testing
code_snippets = {
    "simple_function": "def add(a, b): return a + b",
    "with_docstring": '''def calculate(x, y):
    """Calculate the sum of two numbers."""
    result = x + y
    return result
''',
    "complex_class": '''
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.cache = {}
    
    def process(self, data):
        if data.id in self.cache:
            return self.cache[data.id]
        result = self._transform(data)
        self.cache[data.id] = result
        return result
''',
}


if __name__ == "__main__":
    print("=" * CONSTANT_60)
    print("API Example: Basic Tokenizer Usage")
    print("=" * CONSTANT_60)

for name, code in code_snippets.items():
    print(f"\n{name}:")
    print(f"  Code length: {len(code)} chars")
    
    # Count tokens for different models
    gpt_tokens = tokenizer.count_tokens(code, "gpt-4o")
    claude_tokens = tokenizer.count_tokens(code, "claude-3.5-sonnet")
    
    print(f"  GPT-4o tokens:   {gpt_tokens:3d}")
    print(f"  Claude tokens:   {claude_tokens:3d}")
    print(f"  Difference:      {abs(gpt_tokens - claude_tokens):3d}")

# Using convenience function
    print("\n" + "-" * CONSTANT_60)
    print("Using count_tokens() convenience function:")
    print("-" * CONSTANT_60)

text = "Hello, World! This is a test."
models = ["gpt-4", "claude-3-opus", "openrouter/qwen/qwen3-coder-next"]

for model in models:
    tokens = count_tokens(text, model)
    print(f"{model:40} {tokens:3d} tokens")

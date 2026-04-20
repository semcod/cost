# Basic Tokenizer Usage

Demonstrates how to use the Tokenizer class for accurate token counting across different LLM models.

## What it shows

- Initializing the Tokenizer
- Counting tokens for different models (GPT-4o, Claude, etc.)
- Comparing token counts between providers
- Using the convenience `count_tokens()` function

## Output

Example output showing token counts for different code snippets:
```
simple_function:
  Code length: 27 chars
  GPT-4o tokens:   10
  Claude tokens:    10

with_docstring:
  Code length: 102 chars
  GPT-4o tokens:   26
  Claude tokens:   26
```

## Key Takeaways

- Both OpenAI (tiktoken) and Anthropic tokenizers are supported
- Token counts are usually very similar between models
- The tokenizer automatically selects the right backend based on model name

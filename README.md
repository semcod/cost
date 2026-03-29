# AI Cost Tracker

[![PyPI version](https://badge.fury.io/py/ai-cost-tracker.svg)](https://pypi.org/project/ai-cost-tracker/)

**Zero-config AI cost calculator per commit/model with liteLLM integration.**

Track AI usage costs across your git commits with three flexible usage modes - no initial configuration required.

## Features

- **liteLLM Integration** - Support for 100+ AI providers via liteLLM
- **OpenRouter Default** - Pre-configured for OpenRouter with Qwen models
- **Zero Config** - Works out of the box, reads from `.env` file
- **Smart Token Estimation** - Accurate cost calculation using liteLLM tokenizers
- **ROI Calculation** - Track value generated vs AI costs

## Installation

```bash
pip install ai-cost-tracker
```

## Quick Start

### 1. Initialize Configuration

```bash
aicost init
# Edit .env file to add your OpenRouter API key
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> .env
```

### 2. Run Analysis

```bash
# Uses defaults from .env (OpenRouter + Qwen)
aicost analyze --repo .

# Or specify directly
aicost analyze --repo . --model openrouter/qwen/qwen3-coder-next --api-key your_key_here
```

## Configuration

Create a `.env` file in your project root:

```bash
# Required: OpenRouter API key (https://openrouter.ai/keys)
OPENROUTER_API_KEY=your_key_here
PFIX_MODEL=openrouter/qwen/qwen3-coder-next
```

Or use the built-in init command:

```bash
aicost init
```

## Three Usage Options (Zero Config Required)

### Option 1: BYOK (Bring Your Own Key) - Free

Use your own API key via OpenRouter. Costs calculated locally with real provider pricing.

```bash
# With OpenRouter key (default from .env)
aicost analyze --repo .

# Explicit key
aicost analyze --repo . --api-key sk-or-v1-...
```

**Supported models via liteLLM:**
- `openrouter/qwen/qwen3-coder-next` (default)
- `openrouter/qwen/qwen3-coder`
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4o`
- `ollama/llama2` (local)
- 100+ more via liteLLM

### Option 2: Local/Ollama - Zero API Costs

No API key needed. Estimates based on diff size using local pricing.

```bash
aicost --repo . --mode local
```

**Estimation formula:** `diff_chars / 4 * 0.0001$/M tokens`

### Option 3: SaaS Subscription - Managed

Enterprise managed solution with dashboard and invoicing.

```bash
aicost --repo . --saas-token PLACEHOLDER
```

## Usage Examples

```bash
# Initialize .env config
aicost init

# Analyze last 50 commits (uses .env defaults)
aicost analyze --repo . -n 50

# Use specific model via liteLLM
aicost analyze --repo . --model anthropic/claude-3.5-sonnet

# Analyze all commits (not just AI-tagged)
aicost analyze --repo . --all

# Export to custom file
aicost analyze --repo . --output my_costs.csv

# Estimate single diff
aicost estimate my_changes.patch

# Read diff from stdin
git diff HEAD~1 | aicost estimate -
```

## Tagging AI Commits

Tag commits with `[ai:model]` for automatic tracking:

```bash
git commit -m "[ai:openrouter/qwen/qwen3-coder-next] Refactor authentication"
git commit -m "[ai:anthropic/claude-3.5-sonnet] Add payment integration"
```

## Sample Output

```
🔍 Analyzing 100 commits from my-project...
🤖 Model: openrouter/qwen/qwen3-coder-next | Mode: byok

==================================================
📊 AI COST ANALYSIS - openrouter/qwen/qwen3-coder-next
==================================================
   Commits analyzed: 42
   Total cost:       $0.3245
   Hours saved:      15.3h
   Value generated:  $1530.00
   ROI:              4718x
==================================================
📁 Results saved to: ai_costs.csv

💡 Recent AI commits:
   a1b2c3d4 | $0.0089 | [ai:qwen3-coder-next] Refactor...
   e5f6g7h8 | $0.0121 | [ai:claude-3.5-sonnet] Add feature...
```

## CSV Export Format

| Column | Description |
|--------|-------------|
| `commit_hash` | Short commit SHA |
| `commit_message` | Full commit message |
| `author` | Commit author name |
| `date` | ISO format datetime |
| `cost` | Calculated cost in USD |
| `cost_formatted` | Formatted cost string |
| `model` | AI model used |
| `mode` | Calculation mode (byok/local/saas) |
| `tokens_input` | Estimated input tokens |
| `tokens_output` | Estimated output tokens |
| `hours_saved` | Estimated hours saved |
| `roi` | ROI multiplier |

## Pricing Reference

| Model | Input | Output |
|-------|-------|--------|
| openrouter/qwen/qwen3-coder-next | $0.50/M | $1.50/M |
| openrouter/qwen/qwen2.5-coder | $0.30/M | $1.00/M |
| anthropic/claude-3.5-sonnet | $3/M | $15/M |
| anthropic/claude-3.5-haiku | $0.8/M | $4/M |
| openai/gpt-4o | $5/M | $15/M |
| openai/gpt-4o-mini | $0.15/M | $0.6/M |
| ollama/* | ~$0.0001/M | ~$0.0001/M |

## Business Model

| Tier | Price | Features |
|------|-------|----------|
| **BYOK** | Free | Use your own OpenRouter API key |
| **SaaS** | $9/month | Unlimited, managed keys, dashboard, EU invoicing |

## Development

```bash
# Install with poetry
poetry install

# Run CLI
poetry run aicost analyze --repo ..

# Publish to PyPI
poetry publish --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | (required for BYOK) |
| `PFIX_MODEL` | Default model for calculations | `openrouter/qwen/qwen3-coder-next` |

## License

Licensed under Apache-2.0.


MIT License

# AI Cost Tracker

[![PyPI version](https://badge.fury.io/py/costs.svg)](https://pypi.org/project/costs/)
[![AI Cost](https://img.shields.io/badge/AI%20Cost%20Tracker-Tool%20for%20tracking%20AI%20costs-blue)](https://github.com/semcod/cost)
[![Default Model](https://img.shields.io/badge/Default%20Model-Claude%204%20Sonnet-lightgrey)](https://anthropic.com/claude)

💰 **Track AI costs for your projects** - This tool helps developers monitor AI usage costs across git commits.

**Zero-config AI cost calculator per commit/model with liteLLM integration.**

---

## 📊 AI Cost Tracking for This Project

This project tracks its own AI development costs.

**Development Stats:**
- 📝 **18 commits** across **1 day** of active development
- ⏱️ **~6 hours** estimated development time (accounting for overlapping work)
- 💰 **AI Cost:** Analyze with `costs auto-badge --repo .`

```bash
pip install costs
costs auto-badge --repo .
```

![AI Cost for costs](https://img.shields.io/badge/AI%20Cost-Analyze%20with%20costs-blue)

---

Track AI usage costs across your git commits with three flexible usage modes - no initial configuration required.

## Features

- **liteLLM Integration** - Support for 100+ AI providers via liteLLM
- **Default: Claude 4 Sonnet** - Pre-configured with Anthropic's latest model
- **Zero Config** - Works out of the box, reads from `.env` file
- **Smart Token Estimation** - Accurate cost calculation using liteLLM tokenizers
- **ROI Calculation** - Track value generated vs AI costs
- **Date Filtering** - Analyze specific days, date ranges, or full history
- **Auto Badges** - Automatically generate and update cost badges in README
- **Rich Reports** - Markdown and HTML reports with visualizations

## Installation

```bash
pip install costs
```

## Quick Start

### 1. Initialize Configuration

```bash
costs init
# Edit .env file to add your OpenRouter API key
echo "OPENROUTER_API_KEY=YOUR_KEY" >> .env
```

### 2. Run Analysis

```bash
# Uses defaults from .env (Claude 4 Sonnet)
costs analyze --repo .

# Or specify directly
costs analyze --repo . --model anthropic/claude-4-sonnet --api-key YOUR_KEY
```

## Configuration

Create a `.env` file in your project root:

```bash
# Required: OpenRouter API key (https://openrouter.ai/keys)
OPENROUTER_API_KEY=YOUR_KEY
PFIX_MODEL=anthropic/claude-4-sonnet
```

Or use the built-in init command:

```bash
costs init
```

## Three Usage Options (Zero Config Required)

### Option 1: BYOK (Bring Your Own Key) - Free

Use your own API key via OpenRouter. Costs calculated locally with real provider pricing.

```bash
# With OpenRouter key (default from .env)
costs analyze --repo .

# Explicit key
costs analyze --repo . --api-key YOUR_KEY
```

**Supported models via liteLLM:**
- `anthropic/claude-4-sonnet` (default)
- `anthropic/claude-3.5-sonnet`
- `anthropic/claude-3.5-haiku`
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `openrouter/qwen/qwen3-coder-next`
- 100+ more via liteLLM

### Option 2: Local/Ollama - Zero API Costs

No API key needed. Estimates based on diff size using local pricing.

```bash
costs --repo . --mode local
```

**Estimation formula:** `diff_chars / 4 * 0.0001$/M tokens`

## Date Filtering

Analyze commits for specific time periods:

```bash
# Analyze specific day
costs analyze --repo . --date 2024-03-15

# Analyze date range
costs analyze --repo . --since 2024-01-01 --until 2024-03-31

# Analyze all commits since repository creation
costs analyze --repo . --full-history
```

## Badge Generation

Generate and update cost badges in your README:

```bash
# Generate badge based on pyproject.toml configuration
costs auto-badge --repo .

# Or manually
costs badge --repo . --model anthropic/claude-4-sonnet
```

This adds a badge section to README showing total cost, AI commits, and model used.

### Report Generation

```bash
# Generate markdown report with charts
costs report --repo . --format markdown

# Generate HTML report
costs report --repo . --format html

# Generate both and update README
costs report --repo . --format both --update-readme
```

## How It Works

1. **Parse git history** - Analyzuje commity z tagami `[ai:model]`
2. **Estimate tokens** - Używa heurystyki lub liteLLM do liczenia tokenów
3. **Calculate cost** - Mnoży tokeny × cena za model
4. **Generate ROI** - Szacuje oszczędność czasu (100 LOC/h × $100/h)

## Why liteLLM?

- **Universal API** - Jedna składnia dla 100+ providerów
- **Automatic routing** - Fallback między providerami
- **Cost tracking** - Wbudowane liczenie tokenów
- **OpenRouter** - Dostęp do najnowszych modeli bez kont premium

### Option 3: SaaS Subscription - Managed

Enterprise managed solution with dashboard and invoicing.

```bash
costs --repo . --saas-token PLACEHOLDER
```

## Usage Examples

```bash
# Initialize .env config
costs init

# Analyze last 50 commits (uses .env defaults)
costs analyze --repo . -n 50

# Use specific model via liteLLM
costs analyze --repo . --model anthropic/claude-3.5-sonnet

# Analyze all commits (not just AI-tagged)
costs analyze --repo . --all

# Export to custom file
costs analyze --repo . --output my_costs.csv

# Estimate single diff
costs estimate my_changes.patch

# Read diff from stdin
git diff HEAD~1 | costs estimate -
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
🤖 Model: anthropic/claude-4-sonnet | Mode: byok

==================================================
📊 AI COST ANALYSIS - anthropic/claude-4-sonnet
==================================================
   Commits analyzed: 42
   Total cost:       $12.34
   Hours saved:      15.3h
   Value generated:  $1530.00
   ROI:              124x
==================================================
📁 Results saved to: ai_costs.csv

💡 Recent AI commits:
   a1b2c3d4 | $0.32 | [ai:claude-4-sonnet] Refactor...
   e5f6g7h8 | $0.45 | [ai:claude-4-sonnet] Add feature...
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
| anthropic/claude-4-sonnet | $3/M | $15/M |
| anthropic/claude-3.5-sonnet | $3/M | $15/M |
| anthropic/claude-3.5-haiku | $0.8/M | $4/M |
| openai/gpt-4o | $5/M | $15/M |
| openai/gpt-4o-mini | $0.15/M | $0.6/M |
| openrouter/qwen/qwen3-coder-next | $0.50/M | $1.50/M |
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
poetry run costs analyze --repo ..

# Publish to PyPI
poetry publish --build
```

## PHP Badge Service

Standalone PHP service for generating badges:

```bash
cd services/badge-service
composer install
php -S localhost:8080
```

Generate badges via API:
```bash
curl "http://localhost:8080/badge.php?cost=12.34&model=claude-4&commits=42"
```

## Automatic Cost Calculation

The tool can automatically calculate costs and update badges on every commit and during test runs.

### Pre-commit Hook

Install the pre-commit hook to automatically update the badge before each commit:

```bash
# Copy hook to git hooks
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Or use project.sh (includes hook installation)
bash project.sh
```

The hook will:
1. Detect `costs` in global PATH or virtualenv
2. Run `costs auto-badge` if `[tool.costs]` is configured in `pyproject.toml`
3. Stage updated README.md (interactive prompt in terminal)

### Pytest Integration

Tests automatically validate the cost calculation pipeline:

```bash
# Run all tests including auto-badge test
pytest tests/test_cost.py -v

# Test will:
# - Check if [tool.costs] is configured
# - Run costs auto-badge
# - Verify badge was updated
```

### GitHub Actions

The repository includes a workflow that runs on push/PR:

```yaml
# .github/workflows/ai-cost-badge.yml
# Automatically updates badge on main branch
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `costs init` | Initialize `.env` configuration |
| `costs analyze` | Analyze repository commits |
| `costs stats` | Show repository statistics |
| `costs report` | Generate markdown/HTML reports |
| `costs badge` | Generate cost badge |
| `costs auto-badge` | Auto-generate badge from pyproject.toml |
| `costs estimate` | Estimate cost for single diff |

📖 **Automatic Badge Generation**: See [docs/AUTO_BADGE.md](docs/AUTO_BADGE.md) for GitHub Actions, pre-commit hooks, and CI/CD integration.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | (required for BYOK) |
| `PFIX_MODEL` | Default model for calculations | `anthropic/claude-4-sonnet` |

## License

Licensed under Apache-2.0.

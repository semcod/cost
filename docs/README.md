<!-- code2docs:start --># cost

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.9-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-33-green)
> **33** functions | **0** classes | **9** files | CC̄ = 5.2

> Auto-generated project documentation from source code analysis.

**Author:** Tom Sapletta  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/semcod/cost](https://github.com/semcod/cost)

## Installation

### From PyPI

```bash
pip install cost
```

### From Source

```bash
git clone https://github.com/semcod/cost
cd cost
pip install -e .
```


## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
cost ./my-project

# Only regenerate README
cost ./my-project --readme-only

# Preview what would be generated (no file writes)
cost ./my-project --dry-run

# Check documentation health
cost check ./my-project

# Sync — regenerate only changed modules
cost sync ./my-project
```

### Python API

```python
from cost import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```

## Generated Output

When you run `cost`, the following files are produced:

```
<project>/
├── README.md                 # Main project README (auto-generated sections)
├── docs/
│   ├── api.md               # Consolidated API reference
│   ├── modules.md           # Module documentation with metrics
│   ├── architecture.md      # Architecture overview with diagrams
│   ├── dependency-graph.md  # Module dependency graphs
│   ├── coverage.md          # Docstring coverage report
│   ├── getting-started.md   # Getting started guide
│   ├── configuration.md    # Configuration reference
│   └── api-changelog.md    # API change tracking
├── examples/
│   ├── quickstart.py       # Basic usage examples
│   └── advanced_usage.py   # Advanced usage examples
├── CONTRIBUTING.md         # Contribution guidelines
└── mkdocs.yml             # MkDocs site configuration
```

## Configuration

Create `cost.yaml` in your project root (or run `cost init`):

```yaml
project:
  name: my-project
  source: ./
  output: ./docs/

readme:
  sections:
    - overview
    - install
    - quickstart
    - api
    - structure
  badges:
    - version
    - python
    - coverage
  sync_markers: true

docs:
  api_reference: true
  module_docs: true
  architecture: true
  changelog: true

examples:
  auto_generate: true
  from_entry_points: true

sync:
  strategy: markers    # markers | full | git-diff
  watch: false
  ignore:
    - "tests/"
    - "__pycache__"
```

## Sync Markers

cost can update only specific sections of an existing README using HTML comment markers:

```markdown
<!-- cost:start -->
# Project Title
... auto-generated content ...
<!-- cost:end -->
```

Content outside the markers is preserved when regenerating. Enable this with `sync_markers: true` in your configuration.

## Architecture

```
cost/
    ├── ai_cost_tracker/        ├── models        ├── git_parser        ├── reports        ├── calculator        ├── index        ├── badge├── project        ├── cli```

## API Overview

### Functions

- `get_model_price(model)` — Get pricing for a model, fallback to local if unknown.
- `get_openrouter_headers()` — Get headers for OpenRouter API calls.
- `get_litellm_model_name(model)` — Convert model name to liteLLM format.
- `get_commit_diff(repo, commit)` — Get diff for a commit.
- `is_ai_commit(commit, tag_pattern)` — Check if commit message contains AI tag.
- `extract_ai_tag(commit)` — Extract AI tag from commit message.
- `is_commit_in_date_range(commit, since, until, specific_date)` — Check if commit falls within date range.
- `get_first_commit_date(repo)` — Get the date of the first commit in the repository.
- `parse_commits(repo_path, max_count, ai_only, since)` — Parse commits from repository with date filtering.
- `get_repo_name(repo)` — Get repository name from git remote or directory.
- `get_repo_stats(repo_path)` — Get repository statistics including first commit date.
- `generate_markdown_report(results, output_path)` — Generate markdown report with cost visualizations.
- `generate_html_report(results, output_path)` — Generate interactive HTML report with visualizations.
- `get_cost_color(cost)` — Get badge color based on cost level.
- `update_readme_badge(repo_path, results)` — Update README.md with cost badge.
- `estimate_tokens(diff)` — Estimate input/output tokens from diff.
- `calculate_cost(tokens, model)` — Calculate cost in USD from tokens.
- `calculate_roi(cost, lines_changed, hourly_rate)` — Calculate ROI metrics.
- `ai_cost(commit_diff, model, api_key, saas_token)` — Calculate AI cost for a commit.
- `batch_calculate_costs(commits_data, model, api_key, saas_token)` — Calculate costs for multiple commits.
- `generateBadge()` — —
- `determineColor()` — —
- `analyzeRepository()` — —
- `handleApiRequest()` — —
- `version_callback(value)` — —
- `callback(version)` — —
- `analyze(repo, model, api_key, saas_token)` — Analyze AI costs for git commits with liteLLM support.
- `report(repo, model, format, output_dir)` — Generate cost reports with visualizations.
- `badge(repo, model)` — Generate or update cost badge in README.md.
- `estimate(diff_file, model)` — Estimate cost for a single diff using liteLLM token counting.
- `stats(repo)` — Show repository statistics including commit history.
- `init(force)` — Initialize .env configuration file.
- `main()` — —


## Project Structure

📄 `project`
📄 `services.badge-service.badge` (4 functions)
📄 `services.badge-service.index`
📦 `src.ai_cost_tracker`
📄 `src.ai_cost_tracker.calculator` (5 functions)
📄 `src.ai_cost_tracker.cli` (9 functions)
📄 `src.ai_cost_tracker.git_parser` (8 functions)
📄 `src.ai_cost_tracker.models` (3 functions)
📄 `src.ai_cost_tracker.reports` (4 functions)

## Requirements

- Python >= >=3.9
- gitpython >=3.1- pandas >=2.0- typer >=0.12- httpx >=0.27- litellm >=1.0- python-dotenv >=1.0

## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/semcod/cost
cd cost

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 📖 [Full Documentation](https://github.com/semcod/cost/tree/main/docs) — API reference, module docs, architecture
- 🚀 [Getting Started](https://github.com/semcod/cost/blob/main/docs/getting-started.md) — Quick start guide
- 📚 [API Reference](https://github.com/semcod/cost/blob/main/docs/api.md) — Complete API documentation
- 🔧 [Configuration](https://github.com/semcod/cost/blob/main/docs/configuration.md) — Configuration options
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `docs/api.md` | Consolidated API reference | [View](./docs/api.md) |
| `docs/modules.md` | Module reference with metrics | [View](./docs/modules.md) |
| `docs/architecture.md` | Architecture with diagrams | [View](./docs/architecture.md) |
| `docs/dependency-graph.md` | Dependency graphs | [View](./docs/dependency-graph.md) |
| `docs/coverage.md` | Docstring coverage report | [View](./docs/coverage.md) |
| `docs/getting-started.md` | Getting started guide | [View](./docs/getting-started.md) |
| `docs/configuration.md` | Configuration reference | [View](./docs/configuration.md) |
| `docs/api-changelog.md` | API change tracking | [View](./docs/api-changelog.md) |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples/` | Usage examples | [Browse](./examples) |
| `mkdocs.yml` | MkDocs configuration | — |

<!-- code2docs:end -->
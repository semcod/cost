<!-- code2docs:start --># cost

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.9-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-43-green)
> **43** functions | **0** classes | **14** files | CC̄ = 5.3

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
    ├── costs/        ├── models        ├── metrics            ├── base        ├── git_parser        ├── reports/            ├── markdown        ├── calculator            ├── html            ├── badge        ├── index├── project        ├── badge        ├── cli```

## API Overview

### Functions

- `get_model_price(model)` — Get pricing for a model, fallback to local if unknown.
- `get_openrouter_headers()` — Get headers for OpenRouter API calls.
- `get_litellm_model_name(model)` — Convert model name to liteLLM format.
- `calculate_human_time(commits)` — Calculate human development time with realistic overhead.
- `get_cost_color(cost)` — Get badge color based on cost level.
- `get_commit_diff(repo, commit)` — Get diff for a commit.
- `is_ai_commit(commit, tag_pattern)` — Check if commit message contains AI tag.
- `extract_ai_tag(commit)` — Extract AI tag from commit message.
- `is_commit_in_date_range(commit, since, until, specific_date)` — Check if commit falls within date range.
- `get_first_commit_date(repo)` — Get the date of the first commit in the repository.
- `parse_commits(repo_path, max_count, ai_only, since)` — Parse commits from repository with date filtering.
- `get_repo_name(repo)` — Get repository name from git remote or directory.
- `get_repo_stats(repo_path)` — Get repository statistics including first commit date.
- `generate_markdown_report(results, output_path)` — Generate markdown report with cost visualizations.
- `get_file_type_multiplier(filename)` — Get multiplier based on file extension.
- `estimate_tokens(diff)` — Estimate tokens by parsing diff headers for file-type multipliers.
- `calculate_cost(tokens, model)` — Calculate cost from tokens using model prices.
- `calculate_roi(cost, lines_changed, hourly_rate, review_factor)` — Calculate ROI metrics with human review overhead.
- `ai_cost(commit_diff, model, api_key, saas_token)` — Calculate AI cost for a commit with file-type awareness.
- `batch_calculate_costs(commits_data, model, api_key, saas_token)` — Calculate costs for multiple commits.
- `generate_html_report(results, output_path)` — Generate interactive HTML report with visualizations.
- `update_readme_badge(repo_path, results)` — Update README.md with cost badge including human time calculation.
- `install_hook()` — —
- `generateBadge()` — —
- `determineColor()` — —
- `analyzeRepository()` — —
- `handleApiRequest()` — —
- `version_callback(value)` — —
- `callback(version)` — —
- `analyze(repo, model, api_key, saas_token)` — Analyze AI costs for git commits with liteLLM support.
- `report(repo, model, format, output_dir)` — Generate cost reports with visualizations.
- `badge(repo, model, all_commits)` — Generate or update cost badge in README.md.
- `auto_badge(repo, all_commits)` — Auto-generate badge based on pyproject.toml [tool.costs] configuration.
- `estimate(diff_file, model)` — Estimate cost for a single diff using liteLLM token counting.
- `stats(repo)` — Show repository statistics including commit history.
- `init(force, auto)` — Initialize AI cost tracking for current project.
- `main()` — —


## Project Structure

📄 `project` (1 functions)
📄 `services.badge-service.badge` (4 functions)
📄 `services.badge-service.index`
📦 `src.costs`
📄 `src.costs.calculator` (7 functions)
📄 `src.costs.cli` (14 functions)
📄 `src.costs.git_parser` (9 functions)
📄 `src.costs.metrics` (1 functions)
📄 `src.costs.models` (3 functions)
📦 `src.costs.reports`
📄 `src.costs.reports.badge` (1 functions)
📄 `src.costs.reports.base` (1 functions)
📄 `src.costs.reports.html` (1 functions)
📄 `src.costs.reports.markdown` (1 functions)

## Requirements

- Python >= >=3.9
- gitpython >=3.1- pandas >=2.0- typer >=0.12- click <8.1.0- httpx >=0.27- litellm >=1.0- python-dotenv >=1.0

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
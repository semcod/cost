# System Architecture Analysis

## Overview

- **Project**: /home/tom/github/semcod/cost
- **Primary Language**: python
- **Languages**: python: 6, php: 2, shell: 1
- **Analysis Mode**: static
- **Total Functions**: 33
- **Total Classes**: 0
- **Modules**: 9
- **Entry Points**: 12

## Architecture by Module

### src.ai_cost_tracker.cli
- **Functions**: 9
- **File**: `cli.py`

### src.ai_cost_tracker.git_parser
- **Functions**: 8
- **File**: `git_parser.py`

### src.ai_cost_tracker.calculator
- **Functions**: 5
- **File**: `calculator.py`

### services.badge-service.badge
- **Functions**: 4
- **File**: `badge.php`

### src.ai_cost_tracker.reports
- **Functions**: 4
- **File**: `reports.py`

### src.ai_cost_tracker.models
- **Functions**: 3
- **File**: `models.py`

## Key Entry Points

Main execution flows into the system:

### src.ai_cost_tracker.cli.analyze
> Analyze AI costs for git commits with liteLLM support.

**Three usage modes (zero config required):**

1. **BYOK** (Bring Your Own Key) - `aicost --re
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option

### src.ai_cost_tracker.cli.report
> Generate cost reports with visualizations.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, typer.echo, typer.echo

### src.ai_cost_tracker.cli.badge
> Generate or update cost badge in README.md.
- **Calls**: app.command, typer.Argument, typer.Option, typer.echo, src.ai_cost_tracker.git_parser.parse_commits, src.ai_cost_tracker.calculator.batch_calculate_costs, src.ai_cost_tracker.reports.update_readme_badge, os.getenv

### src.ai_cost_tracker.cli.stats
> Show repository statistics including commit history.
- **Calls**: app.command, typer.Argument, src.ai_cost_tracker.git_parser.get_repo_stats, typer.echo, typer.echo, typer.echo, typer.echo, typer.echo

### src.ai_cost_tracker.cli.estimate
> Estimate cost for a single diff using liteLLM token counting.
- **Calls**: app.command, typer.Argument, typer.Option, src.ai_cost_tracker.models.get_litellm_model_name, src.ai_cost_tracker.calculator.ai_cost, typer.echo, typer.echo, typer.echo

### services.badge-service.badge.handleApiRequest
- **Calls**: services.badge-service.badge.json_decode, services.badge-service.badge.file_get_contents, services.badge-service.badge.http_response_code, services.badge-service.badge.json_encode, services.badge-service.badge.generateBadge, services.badge-service.badge.isset, services.badge-service.badge.header, services.badge-service.badge.base64_encode

### src.ai_cost_tracker.cli.init
> Initialize .env configuration file.
- **Calls**: app.command, typer.Option, Path, env_path.write_text, typer.echo, env_path.exists, typer.echo, typer.Exit

### src.ai_cost_tracker.git_parser.extract_ai_tag
> Extract AI tag from commit message.
- **Calls**: re.search, match.group

### src.ai_cost_tracker.cli.version_callback
- **Calls**: typer.echo, typer.Exit

### src.ai_cost_tracker.cli.callback
- **Calls**: app.callback, typer.Option

### src.ai_cost_tracker.cli.main
- **Calls**: app

### src.ai_cost_tracker.models.get_openrouter_headers
> Get headers for OpenRouter API calls.

## Process Flows

Key execution flows identified:

### Flow 1: analyze
```
analyze [src.ai_cost_tracker.cli]
```

### Flow 2: report
```
report [src.ai_cost_tracker.cli]
```

### Flow 3: badge
```
badge [src.ai_cost_tracker.cli]
  └─ →> parse_commits
      └─> get_commit_diff
```

### Flow 4: stats
```
stats [src.ai_cost_tracker.cli]
  └─ →> get_repo_stats
      └─> get_repo_name
```

### Flow 5: estimate
```
estimate [src.ai_cost_tracker.cli]
  └─ →> get_litellm_model_name
  └─ →> ai_cost
      └─> estimate_tokens
      └─> calculate_cost
          └─ →> get_model_price
```

### Flow 6: handleApiRequest
```
handleApiRequest [services.badge-service.badge]
```

### Flow 7: init
```
init [src.ai_cost_tracker.cli]
```

### Flow 8: extract_ai_tag
```
extract_ai_tag [src.ai_cost_tracker.git_parser]
```

### Flow 9: version_callback
```
version_callback [src.ai_cost_tracker.cli]
```

### Flow 10: callback
```
callback [src.ai_cost_tracker.cli]
```

## Data Transformation Functions

Key functions that process and transform data:

### src.ai_cost_tracker.git_parser.parse_commits
> Parse commits from repository with date filtering.

Args:
    repo_path: Path to git repository
    
- **Output to**: git.Repo, repo.iter_commits, isinstance, src.ai_cost_tracker.git_parser.get_commit_diff, commits.append

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.ai_cost_tracker.cli.analyze` - 55 calls
- `src.ai_cost_tracker.cli.report` - 39 calls
- `src.ai_cost_tracker.git_parser.parse_commits` - 20 calls
- `src.ai_cost_tracker.cli.badge` - 20 calls
- `src.ai_cost_tracker.cli.stats` - 18 calls
- `src.ai_cost_tracker.cli.estimate` - 17 calls
- `src.ai_cost_tracker.reports.generate_markdown_report` - 16 calls
- `services.badge-service.badge.handleApiRequest` - 14 calls
- `src.ai_cost_tracker.reports.generate_html_report` - 14 calls
- `src.ai_cost_tracker.reports.update_readme_badge` - 13 calls
- `src.ai_cost_tracker.calculator.ai_cost` - 11 calls
- `services.badge-service.badge.analyzeRepository` - 9 calls
- `src.ai_cost_tracker.calculator.batch_calculate_costs` - 8 calls
- `src.ai_cost_tracker.git_parser.get_commit_diff` - 8 calls
- `src.ai_cost_tracker.cli.init` - 8 calls
- `src.ai_cost_tracker.git_parser.get_repo_stats` - 7 calls
- `src.ai_cost_tracker.git_parser.get_first_commit_date` - 5 calls
- `services.badge-service.badge.generateBadge` - 5 calls
- `src.ai_cost_tracker.calculator.calculate_roi` - 4 calls
- `src.ai_cost_tracker.git_parser.get_repo_name` - 4 calls
- `src.ai_cost_tracker.models.get_model_price` - 3 calls
- `src.ai_cost_tracker.calculator.estimate_tokens` - 2 calls
- `src.ai_cost_tracker.calculator.calculate_cost` - 2 calls
- `src.ai_cost_tracker.git_parser.is_ai_commit` - 2 calls
- `src.ai_cost_tracker.git_parser.extract_ai_tag` - 2 calls
- `src.ai_cost_tracker.cli.version_callback` - 2 calls
- `src.ai_cost_tracker.cli.callback` - 2 calls
- `src.ai_cost_tracker.git_parser.is_commit_in_date_range` - 1 calls
- `src.ai_cost_tracker.cli.main` - 1 calls
- `src.ai_cost_tracker.models.get_openrouter_headers` - 0 calls
- `src.ai_cost_tracker.models.get_litellm_model_name` - 0 calls
- `services.badge-service.badge.determineColor` - 0 calls
- `src.ai_cost_tracker.reports.get_cost_color` - 0 calls

## System Interactions

How components interact:

```mermaid
graph TD
    analyze --> command
    analyze --> Argument
    analyze --> Option
    report --> command
    report --> Argument
    report --> Option
    badge --> command
    badge --> Argument
    badge --> Option
    badge --> echo
    badge --> parse_commits
    stats --> command
    stats --> Argument
    stats --> get_repo_stats
    stats --> echo
    estimate --> command
    estimate --> Argument
    estimate --> Option
    estimate --> get_litellm_model_na
    estimate --> ai_cost
    handleApiRequest --> json_decode
    handleApiRequest --> file_get_contents
    handleApiRequest --> http_response_code
    handleApiRequest --> json_encode
    handleApiRequest --> generateBadge
    init --> command
    init --> Option
    init --> Path
    init --> write_text
    init --> echo
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.
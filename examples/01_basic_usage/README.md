# CLI Basic Usage

Common command-line usage patterns for the costs tool.

## What it shows

- Initialize configuration
- Analyze repositories
- Filter by date and time
- Different output options

## Files

- `run.sh` - Demonstrates common CLI commands

# Or run individual commands
costs init
costs analyze --repo . -n 50
```

### 1. Initialize configuration
```bash
costs init                      # Create .env file
costs init --force             # Overwrite existing
```

### 2. Analyze repository
```bash
costs analyze --repo .                         # Current repo
costs analyze --repo . --model openrouter/qwen/qwen3-coder-next
costs analyze --repo . --api-key YOUR_KEY
```

### 3. Filter by date
```bash
costs analyze --repo . --date 2024-03-15
costs analyze --repo . --since 2024-01-01 --until 2024-03-31
costs analyze --repo . --full-history
```

### 4. Output options
```bash
costs analyze --repo . --output my_costs.csv
costs stats --repo .
```

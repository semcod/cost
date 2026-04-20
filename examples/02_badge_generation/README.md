# CLI Badge Generation

Generate cost badges and reports for your README.

## What it shows

- Generate badges manually
- Auto-badge from pyproject.toml config
- Generate markdown and HTML reports

## Files

- `run.sh` - Demonstrates badge and report generation commands

# Or run individual commands
costs badge --repo . --all
costs report --repo . --format both
```

### 1. Manual badge generation
```bash
costs badge --repo .              # Current state
costs badge --repo . --all        # All commits (not just AI-tagged)
```

### 2. Auto-badge from config
```bash
costs auto-badge --repo .         # Read [tool.costs] from pyproject.toml
costs auto-badge --repo . --all # Include all commits
```

### 3. Report generation
```bash
costs report --repo . --format markdown
costs report --repo . --format html
costs report --repo . --format both --update-readme
```

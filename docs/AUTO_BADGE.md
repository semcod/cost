# Automatic Badge Generation

This document describes how to automatically generate and update AI cost badges in projects using `costs`.

## Methods Overview

| Method | Trigger | Use Case |
|--------|---------|----------|
| **GitHub Actions** | Push to main | Automatic CI/CD updates |
| **Pre-commit Hook** | Before each commit | Local development |
| **Post-commit Hook** | After each commit | Immediate badge refresh |
| **Package Scripts** | Build/test | Integration with build process |

---

## Method 1: GitHub Actions (Recommended)

Automatically updates badge on every push to main branch.

### Setup

1. Copy the workflow file to your project:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/ai-cost-badge.yml \
  https://raw.githubusercontent.com/semcod/cost/main/.github/workflows/ai-cost-badge.yml
```

2. Add `OPENROUTER_API_KEY` to repository secrets:
   - Go to Settings → Secrets → Actions
   - Add `OPENROUTER_API_KEY` with your key

3. The workflow will:
   - Run on every push to main/master
   - Update the badge in README.md
   - Commit changes automatically

### Configuration

Customize behavior in `pyproject.toml`:

```toml
[tool.costs]
badge = true
update_readme = true
full_history = true  # Analyze all commits
max_commits = 1000
```

---

## Method 2: Pre-commit Hook

Updates badge before each commit (local development).

### Setup

1. Install the hook:

```bash
# Copy hook to .git/hooks
curl -o .git/hooks/pre-commit \
  https://raw.githubusercontent.com/semcod/cost/main/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

2. Or use with [pre-commit framework](https://pre-commit.com):

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-cost-badge
        name: Update AI Cost Badge
        entry: costs auto-badge --repo . --quiet
        language: system
        pass_filenames: false
        always_run: true
```

---

## Method 3: Post-commit Hook

Updates badge immediately after each commit with `[ai:]` tag.

```bash
# .git/hooks/post-commit
#!/bin/bash
if git log -1 --pretty=%B | grep -q '\[ai:'; then
    echo "🤖 AI commit detected, updating badge..."
    costs auto-badge --repo . --quiet
    git add README.md
    git commit --amend --no-edit
fi
```

---

### Python (pyproject.toml)

```toml
[tool.poe.tasks]
badge = "costs auto-badge --repo ."
pre_build = ["badge", "build"]
```

### Node.js (package.json)

```json
{
  "scripts": {
    "postbuild": "costs auto-badge --repo .",
    "badge": "costs auto-badge --repo ."
  }
}
```

### Makefile

```makefile
.PHONY: badge
badge:
	costs auto-badge --repo .

build: badge
	python -m build
```

---

### VS Code

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Update AI Cost Badge",
      "type": "shell",
      "command": "costs auto-badge --repo .",
      "problemMatcher": []
    }
  ]
}
```

---

### pyproject.toml [tool.costs]

```toml
[tool.costs]
# Badge appearance
badge_format = "svg"           # svg or png
badge_style = "flat"           # flat, flat-square, plastic, for-the-badge
badge_label = "AI Cost"        # Label text

# README integration
update_readme = true           # Auto-update README.md
readme_path = "README.md"      # Path to README
badge_output_dir = "."         # Where to save badge files

# Analysis settings
default_model = "anthropic/claude-4-sonnet"
analysis_mode = "byok"         # byok, local, saas
full_history = false           # Analyze all commits
max_commits = 1000            # Max commits to analyze
ai_only = true                # Only count commits with [ai:] tags

# Color thresholds (USD)
badge_color_thresholds = { 
    low = 1.0,      # brightgreen
    medium = 5.0,   # green
    high = 10.0,    # yellow
    critical = 50.0 # orange/red
}

# Auto-generation triggers
auto_generate_on_install = false   # Generate on pip install
auto_generate_on_commit = false    # Generate on each commit
```

---

### 1. CI/CD Pipeline (Recommended for teams)

Use GitHub Actions for:
- Automatic updates on push
- Consistent badge across team
- No local setup required

### 2. Local Development

Use pre-commit hook for:
- Immediate feedback
- Local cost tracking
- Offline capability (with local mode)

### Badge not updating

1. Check pyproject.toml has `[tool.costs]` section
2. Verify costs is installed: `pip install costs`
3. Check if README.md exists and is writable
4. Ensure git repo is initialized: `git status`

### GitHub Actions failing

1. Check `OPENROUTER_API_KEY` secret is set
2. Verify workflow has write permissions
3. Check Actions tab for error logs

### Badge colors wrong

Adjust thresholds in pyproject.toml:

```toml
[tool.costs.badge_color_thresholds]
low = 0.5      # Green below $0.50
medium = 2.0   # Yellow below $2.00
high = 5.0     # Orange below $5.00
critical = 20.0 # Red above $20.00
```

---

### Step 1: Install costs

```bash
pip install costs
```

### Step 2: Configure pyproject.toml

```toml
[tool.costs]
badge = true
update_readme = true
default_model = "anthropic/claude-4-sonnet"
full_history = true
```

### Step 3: Add GitHub Actions

```bash
mkdir -p .github/workflows
curl -o .github/workflows/ai-cost-badge.yml \
  https://raw.githubusercontent.com/semcod/cost/main/.github/workflows/ai-cost-badge.yml
```

### Step 4: Set up secrets

In GitHub repository settings:
- Add `OPENROUTER_API_KEY` secret

### Step 5: Initial badge generation

```bash
costs auto-badge --repo .
git add README.md
git commit -m "docs: add AI cost tracking badge"
```

---

## Advanced: Custom Badge Server

For self-hosted badge generation:

```bash
cd services/badge-service
composer install
php -S localhost:8080
```

Then use in README:

```markdown
![AI Cost](http://your-server/badge.php?repo=your-org/your-repo)
```

See [badge-service README](../services/badge-service/README.md) for details.

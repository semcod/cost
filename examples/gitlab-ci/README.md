# GitLab CI

GitLab CI configuration for AI cost tracking.

## What it shows

- GitLab CI pipeline for cost analysis
- Update badge on every commit to main
- Generate cost report for merge requests

## Files

- `.gitlab-ci.yml` - The GitLab CI configuration

## Usage

Copy `.gitlab-ci.yml` to your repository:

```bash
cp .gitlab-ci.yml /path/to/your/repo/
cd /path/to/your/repo
git add .gitlab-ci.yml
git commit -m "Add AI cost tracking CI"
```

## Setup

1. Add `CI_TOKEN` as a GitLab CI/CD variable (for pushing badge updates)
2. Optional: Add `OPENROUTER_API_KEY` if using BYOK mode

### `ai-cost-badge`
- Runs on every commit to main/master
- Updates badge in README.md
- Commits and pushes changes

### `ai-cost-report`
- Runs on merge requests
- Generates cost report for MR commits
- Uploads as artifact

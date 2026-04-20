# Multi-Repository Analysis

Analyze costs across multiple repositories and aggregate results.

## What it shows

- Analyze multiple repositories in one run
- Aggregate costs across repos
- Generate combined reports

## Files

- `main.py` - Python example
- `run.sh` - Run the example
- `repos.txt` - List of repositories to analyze (template)

## Configuration

Edit `repos.txt` to list your repositories:
```
/home/user/projects/web-app
/home/user/projects/api-service
/home/user/projects/mobile-app
```

## Sample Output

```
Repository                     Commits    Tokens       Cost
----------------------------------------------------------------------
web-app                              5        1243 $    0.0037
api-service                          3         892 $    0.0027
mobile-app                           4        1567 $    0.0047
----------------------------------------------------------------------
TOTAL                                           3702 $    0.0111
```

## Key Takeaways

- Batch processing across repositories
- Centralized cost tracking for organizations
- Aggregate reporting capabilities

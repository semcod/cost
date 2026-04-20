#!/usr/bin/env python3
"""Multi-Repository Analysis - analyze costs across multiple repositories."""
import subprocess
import os
from costs.calculator import ai_cost

# List of repositories to analyze - update with your paths
REPOSITORIES = [
    "/path/to/repo1",
    "/path/to/repo2", 
    "/path/to/repo3",
]


if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Example: Multi-Repository Analysis")
    print("=" * 60)

def analyze_repository(repo_path):
    """Analyze a single repository."""
    if not os.path.exists(repo_path):
        return None
    
    try:
        # Get recent commits with AI tags
        result = subprocess.run(
            ["git", "log", "--grep=\\[ai:", "-10", "--pretty=format:%H"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        commits = result.stdout.strip().split("\n")
        commits = [c for c in commits if c]
        
        total_cost = 0
        total_tokens = 0
        
        for commit_hash in commits[:5]:
            diff_result = subprocess.run(
                ["git", "show", commit_hash, "--format="],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if diff_result.returncode == 0:
                cost_result = ai_cost(diff_result.stdout, model="claude-3.5-sonnet")
                total_cost += cost_result["cost"]
                total_tokens += cost_result["tokens"]["total"]
        
        return {
            "commits_analyzed": len(commits),
            "total_cost": total_cost,
            "total_tokens": total_tokens
        }
    except Exception as e:
        print(f"Error analyzing {repo_path}: {e}")
        return None

# Analyze all repositories
    print("\nAnalyzing repositories...")
    print(f"{'Repository':<30} {'Commits':>8} {'Tokens':>10} {'Cost':>12}")
    print("-" * 70)

total_cost = 0
total_tokens = 0

for repo in REPOSITORIES:
    repo_name = os.path.basename(repo)
    result = analyze_repository(repo)
    
    if result:
        print(f"{repo_name:<30} {result['commits_analyzed']:>8} "
              f"{result['total_tokens']:>10} ${result['total_cost']:>10.4f}")
        total_cost += result["total_cost"]
        total_tokens += result["total_tokens"]
    else:
        print(f"{repo_name:<30} {'N/A':>8} {'N/A':>10} {'N/A':>12}")

    print("-" * 70)
    print(f"{'TOTAL':<30} {'':8} {total_tokens:>10} ${total_cost:>10.4f}")

    print("\nNote: Update REPOSITORIES list in main.py with actual paths")

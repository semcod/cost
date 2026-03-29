"""README badge update logic."""

import re
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from ..metrics import calculate_human_time


def update_readme_badge(repo_path: Path, results: Dict[str, Any]) -> bool:
    """Update README.md with cost badge including human time calculation."""
    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        return False
    
    summary = results["summary"]
    model = summary["model"]
    total_cost = summary["total_cost"]
    
    # Get all commits (not just AI) for accurate human time calculation
    # Import here to avoid circular dependencies if any
    from ..git_parser import parse_commits
    all_commits_data = parse_commits(
        str(repo_path),
        max_count=1000,
        ai_only=False,
        full_history=True
    )
    # Convert to dict format expected by calculate_human_time
    all_commits = [
        {"date": c[0].committed_datetime.isoformat(), "author": c[0].author.name} 
        for c in all_commits_data
    ]
    
    # Calculate human time with realistic buffers
    human_hours = calculate_human_time(all_commits)
    human_cost = human_hours * 100  # $100/hour rate
    
    # Create badge lines with standout colors
    pypi_badge = "![PyPI](https://img.shields.io/badge/pypi-costs-blue)"
    version_badge = "![Version](https://img.shields.io/badge/version-0.1.31-blue)"
    python_badge = "![Python](https://img.shields.io/badge/python-3.9+-blue)"
    license_badge = "![License](https://img.shields.io/badge/license-Apache--2.0-green)"
    cost_badge = f"![AI Cost](https://img.shields.io/badge/AI%20Cost-${total_cost:.2f}-orange)"
    human_time_badge = f"![Human Time](https://img.shields.io/badge/Human%20Time-{human_hours:.1f}h-blue)"
    model_badge = f"![Model](https://img.shields.io/badge/Model-{model.replace('/', '%2F').replace('-', '--')}-lightgrey)"
    
    # Fix URL generation for OpenRouter
    model_url_path = model.replace("openrouter/", "")
    badge_section = f"""## AI Cost Tracking

{pypi_badge} {version_badge} {python_badge} {license_badge}
{cost_badge} {human_time_badge} {model_badge}

- 🤖 **LLM usage:** {summary['total_cost_formatted']} ({summary['total_commits']} commits)
- 👤 **Human dev:** ~${human_cost:.0f} ({human_hours:.1f}h @ $100/h, 30min dedup)

Generated on {datetime.now().strftime("%Y-%m-%d")} using [{model}](https://openrouter.ai/{model_url_path})

---

"""
    
    content = readme_path.read_text()
    
    # Check if badge section already exists
    if "## AI Cost Tracking" in content:
        # Replace existing section
        pattern = r"## AI Cost Tracking\n.*?\n---\n\n"
        content = re.sub(pattern, badge_section, content, flags=re.DOTALL)
        # Add after main badges if possible, else after first heading
        lines = content.split("\n")
        insert_idx = -1
        
        # Strategy 1: Find the end of a center-aligned badge block
        for i, line in enumerate(lines):
            if "</p>" in line and i < 50:  # Usually at the top
                insert_idx = i + 1
                break
        
        # Strategy 2: Fallback to after the first # heading
        if insert_idx == -1:
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    insert_idx = i + 1
                    break
        
        if insert_idx != -1:
            lines.insert(insert_idx, "\n" + badge_section)
            content = "\n".join(lines)
    
    readme_path.write_text(content)
    return True

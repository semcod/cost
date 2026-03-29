"""Core cost calculation logic."""

from typing import Dict, Optional, Any, List, Tuple
import httpx
from .models import get_model_price


# Advanced metrics configuration
DEFAULT_HOURLY_RATE = 100.0  # USD/h
HUMAN_REVIEW_OVERHEAD = 0.2  # 20% of AI-saved time is spent on review
LOC_PER_HOUR = 100           # Human productivity baseline

# File type impact multipliers for token estimation
# Logic-heavy languages have a higher weight than boilerplate/docs
FILE_TYPE_MULTIPLIERS = {
    ".py": 1.5,
    ".js": 1.2,
    ".ts": 1.3,
    ".cpp": 1.8,
    ".go": 1.4,
    ".rs": 1.5,
    ".php": 1.1,
    ".md": 0.5,
    ".json": 0.4,
    ".yaml": 0.6,
    ".html": 0.8,
    ".css": 0.9,
}


def get_file_type_multiplier(filename: str) -> float:
    """Get multiplier based on file extension."""
    for ext, mult in FILE_TYPE_MULTIPLIERS.items():
        if filename.endswith(ext):
            return mult
    return 1.0


def _estimate_single_file_tokens(diff: str, filename: Optional[str] = None) -> Dict[str, int]:
    """Heuristic for a single file's tokens."""
    chars = len(diff)
    multiplier = get_file_type_multiplier(filename) if filename else 1.0
    base_tokens = max(int((chars // 4) * multiplier), 1)
    
    return {
        "input": int(base_tokens * 2.5),
        "output": int(base_tokens * 4.5),
        "total": int(base_tokens * 7)
    }


def estimate_tokens(diff: str) -> Dict[str, int]:
    """Estimate tokens by parsing diff headers for file-type multipliers."""
    if not diff:
        return {"input": 0, "output": 0, "total": 0}
        
    # Split diff by "diff --git"
    parts = diff.split("diff --git")
    
    # If no headers found, estimate as single block
    if len(parts) <= 1 and not diff.strip().startswith("diff --git"):
        return _estimate_single_file_tokens(diff)
        
    total_input = 0
    total_output = 0
    
    for part in parts:
        if not part.strip():
            continue
            
        # Parse filename from +++ b/path
        filename = None
        for line in part.splitlines():
            if line.startswith("+++ b/"):
                filename = line[6:]
                break
        
        tokens = _estimate_single_file_tokens(part, filename)
        total_input += tokens["input"]
        total_output += tokens["output"]
        
    return {
        "input": total_input,
        "output": total_output,
        "total": total_input + total_output
    }


def calculate_cost(tokens: Dict[str, int], model: str) -> float:
    """Calculate cost from tokens using model prices."""
    price = get_model_price(model)
    cost = (tokens["input"] * price["input"] + 
            tokens["output"] * price["output"])
    return max(cost, 0.0001)  # minimum cost


def calculate_roi(
    cost: float, 
    lines_changed: int, 
    hourly_rate: float = DEFAULT_HOURLY_RATE,
    review_factor: float = HUMAN_REVIEW_OVERHEAD
) -> Dict[str, Any]:
    """Calculate ROI metrics with human review overhead."""
    # Gross time saved by AI
    hours_saved_gross = lines_changed / LOC_PER_HOUR
    
    # Net time saved (Subtract review overhead)
    review_time = hours_saved_gross * review_factor
    hours_saved_net = max(hours_saved_gross - review_time, 0.0)
    
    # Financial metrics
    value_generated = hours_saved_net * hourly_rate
    roi = value_generated / cost if cost > 0 else float('inf')
    
    return {
        "hours_saved": round(hours_saved_net, 2),
        "review_time": round(review_time, 2),
        "value_generated": round(value_generated, 2),
        "roi": round(roi, 1),
        "roi_formatted": f"{roi:.0f}x" if roi < 1000 else "∞"
    }


def ai_cost(
    commit_diff: str,
    model: str = "claude-3.5-sonnet",
    api_key: Optional[str] = None,
    saas_token: Optional[str] = None,
    saas_url: str = "https://your-saas.com/api/cost"
) -> Dict[str, Any]:
    """Calculate AI cost for a commit with file-type awareness."""
    tokens = estimate_tokens(commit_diff)
    lines_changed = len([l for l in commit_diff.splitlines() if l.strip()])
    
    # SaaS Mode
    if saas_token:
        try:
            resp = httpx.post(
                saas_url,
                json={"tokens": tokens, "model": model},
                headers={"Authorization": f"Bearer {saas_token}"},
                timeout=10.0
            )
            resp.raise_for_status()
            data = resp.json()
            cost = data.get("cost", 0.0)
            return {
                "cost": cost,
                "cost_formatted": f"${cost:.4f}",
                "model": model,
                "mode": "saas",
                "tokens": tokens,
                **calculate_roi(cost, lines_changed)
            }
        except:
            pass
            
    # Local/BYOK Mode
    cost = calculate_cost(tokens, model)
    mode = "byok" if api_key else "local"
    
    return {
        "cost": cost,
        "cost_formatted": f"${cost:.4f}",
        "model": model,
        "mode": mode,
        "tokens": tokens,
        **calculate_roi(cost, lines_changed)
    }


def batch_calculate_costs(
    commits_data: List[Tuple[Any, str]],
    model: str = "claude-3.5-sonnet",
    api_key: Optional[str] = None,
    saas_token: Optional[str] = None
) -> Dict[str, Any]:
    """Calculate costs for multiple commits."""
    results = []
    total_cost = 0.0
    total_hours_saved = 0.0
    total_value = 0.0
    
    for commit, diff in commits_data:
        cost_info = ai_cost(diff, model, api_key=api_key, saas_token=saas_token)
        cost_info["commit_hash"] = commit.hexsha[:8]
        cost_info["commit_message"] = commit.message.strip()
        cost_info["author"] = commit.author.name
        cost_info["date"] = commit.committed_datetime.isoformat()
        
        results.append(cost_info)
        total_cost += cost_info["cost"]
        total_hours_saved += cost_info["hours_saved"]
        total_value += cost_info["value_generated"]
    
    avg_roi = total_value / total_cost if total_cost > 0 else 0
    
    return {
        "commits": results,
        "summary": {
            "total_commits": len(results),
            "total_cost": round(total_cost, 4),
            "total_cost_formatted": f"${total_cost:.4f}",
            "total_hours_saved": round(total_hours_saved, 2),
            "total_value_generated": round(total_value, 2),
            "average_roi": f"{avg_roi:.0f}x" if avg_roi < 1000 else "∞",
            "model": model,
            "mode": results[0]["mode"] if results else "unknown"
        }
    }

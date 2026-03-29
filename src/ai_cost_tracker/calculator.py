"""Core cost calculation logic."""

from typing import Dict, Optional, Any
import httpx

from .models import get_model_price
from .git_parser import get_commit_diff


def estimate_tokens(diff: str) -> Dict[str, int]:
    """Estimate input/output tokens from diff.
    
    Heuristic: ~4 chars per token, input:output ratio ~2:5
    """
    chars = len(diff)
    base_tokens = max(chars // 4, 1)
    return {
        "input": base_tokens * 2,   # context/prompt
        "output": base_tokens * 5,   # generated code
        "total": base_tokens * 7
    }


def calculate_cost(tokens: Dict[str, int], model: str) -> float:
    """Calculate cost in USD from tokens."""
    price = get_model_price(model)
    cost = (tokens["input"] * price["input"] + 
            tokens["output"] * price["output"])
    return max(cost, 0.0001)  # minimum cost


def calculate_roi(cost: float, lines_changed: int, hourly_rate: float = 100.0) -> Dict[str, Any]:
    """Calculate ROI metrics.
    
    Assumptions:
    - Developer writes ~100 LOC/hour
    - Developer hourly rate $100/h
    """
    hours_saved = lines_changed / 100.0
    value_generated = hours_saved * hourly_rate
    roi = value_generated / cost if cost > 0 else float('inf')
    
    return {
        "hours_saved": round(hours_saved, 2),
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
    """Calculate AI cost for a commit.
    
    Three modes:
    1. BYOK: Provide api_key, calculate locally with real prices
    2. Local: No keys, estimate with local pricing
    3. SaaS: Provide saas_token, call managed API
    """
    tokens = estimate_tokens(commit_diff)
    lines_changed = len([l for l in commit_diff.splitlines() if l.strip()])
    
    # Mode 3: SaaS subscription
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
        except Exception as e:
            # Fallback to local calculation
            pass
    
    # Mode 1 & 2: Local calculation
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
    commits_data,
    model: str = "claude-3.5-sonnet",
    api_key: Optional[str] = None,
    saas_token: Optional[str] = None
) -> Dict[str, Any]:
    """Calculate costs for multiple commits.
    
    Returns aggregated results.
    """
    results = []
    total_cost = 0.0
    total_hours_saved = 0.0
    total_value = 0.0
    
    for commit, diff in commits_data:
        cost_info = ai_cost(diff, model, api_key, saas_token)
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

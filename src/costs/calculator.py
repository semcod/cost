"""Core cost calculation logic."""

from typing import Dict, Optional, Any, List, Tuple
import httpx
from .models import get_model_price
from .tokenizers import Tokenizer, GitDiffParser

CONSTANT_1 = 1.1
CONSTANT_1 = 1.2
CONSTANT_1 = 1.3
CONSTANT_1 = 1.4
CONSTANT_1 = 1.5
CONSTANT_1 = 1.8
CONSTANT_4 = 4
CONSTANT_8 = 8
CONSTANT_30 = 30


CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_4 = CONSTANT_4
CONSTANT_8 = CONSTANT_8
CONSTANT_30 = CONSTANT_30


CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_1 = CONSTANT_1
CONSTANT_4 = CONSTANT_4
CONSTANT_8 = CONSTANT_8
CONSTANT_30 = CONSTANT_30


# Initialize tokenizer
_tokenizer = Tokenizer()


# Advanced metrics configuration
DEFAULT_HOURLY_RATE = 100.0  # USD/h
HUMAN_REVIEW_OVERHEAD = 0.2  # 20% of AI-saved time is spent on review
LOC_PER_HOUR = 100           # Human productivity baseline

# File type impact multipliers for token estimation
# Logic-heavy languages have a higher weight than boilerplate/docs
FILE_TYPE_MULTIPLIERS = {
    ".py": CONSTANT_1,
    ".js": CONSTANT_1,
    ".ts": CONSTANT_1,
    ".cpp": CONSTANT_1,
    ".go": CONSTANT_1,
    ".rs": CONSTANT_1,
    ".php": CONSTANT_1,
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


def estimate_tokens(diff: str, model: Optional[str] = None) -> Dict[str, int]:
    """
    Estimate tokens using proper tokenization.
    
    Args:
        diff: Git diff content
        model: Model name for accurate token counting
        
    Returns:
        Dict with input, output, and total token counts
    """
    if not diff:
        return {"input": 0, "output": 0, "total": 0}
    
    # Parse diff stats for accurate line counting
    diff_stats = GitDiffParser.parse_diff_stats(diff)
    
    # Create realistic prompt that would be sent to LLM
    prompt = f"Review this code change:\n```diff\n{diff}\n```"
    
    # Count input tokens accurately
    input_tokens = _tokenizer.count_tokens(prompt, model)
    
    # Estimate output tokens based on actual added lines
    # Industry heuristic: code review output ~30 tokens per added line
    # Minimum fallback: 25% of input for simple reviews
    added_lines = diff_stats["added_lines"]
    output_from_lines = added_lines * CONSTANT_30
    output_from_ratio = int(input_tokens * 0.25)
    
    output_tokens = max(output_from_lines, output_from_ratio, 1)
    
    return {
        "input": input_tokens,
        "output": output_tokens,
        "total": input_tokens + output_tokens
    }


# Legacy function for backward compatibility
def _estimate_single_file_tokens(diff: str, filename: Optional[str] = None) -> Dict[str, int]:
    """Legacy heuristic - kept for backward compatibility."""
    return estimate_tokens(diff)


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
    """Calculate AI cost for a commit with proper tokenization."""
    tokens = estimate_tokens(commit_diff, model)
    
    # Use accurate line stats from diff parser
    diff_stats = GitDiffParser.parse_diff_stats(commit_diff)
    lines_changed = diff_stats["total_changed"]
    
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
        cost_info["commit_hash"] = commit.hexsha[:CONSTANT_8]
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
            "total_cost": round(total_cost, CONSTANT_4),
            "total_cost_formatted": f"${total_cost:.4f}",
            "total_hours_saved": round(total_hours_saved, 2),
            "total_value_generated": round(total_value, 2),
            "average_roi": f"{avg_roi:.0f}x" if avg_roi < 1000 else "∞",
            "model": model,
            "mode": results[0]["mode"] if results else "unknown"
        }
    }

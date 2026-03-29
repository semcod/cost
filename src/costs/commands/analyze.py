import os
from pathlib import Path
from typing import Optional
import typer
import pandas as pd
import git
from ..calculator import batch_calculate_costs
from ..git_parser import parse_commits, get_repo_name
from ..models import get_litellm_model_name

def _get_repo(repo_path: Path) -> git.Repo:
    """Validate repository existence and return git.Repo object."""
    if not repo_path.exists():
        typer.echo(f"❌ Repository not found: {repo_path}", err=True)
        raise typer.Exit(1)
    
    try:
        return git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        typer.echo(f"❌ Not a git repository: {repo_path}", err=True)
        raise typer.Exit(1)


def _get_execution_context(
    mode: str, 
    api_key: str, 
    saas_token: str
) -> tuple[str, Optional[str], Optional[str]]:
    """Determine calculation mode and credentials."""
    effective_mode = mode
    if mode == "auto":
        if saas_token:
            effective_mode = "saas"
        elif api_key:
            effective_mode = "byok"
        else:
            effective_mode = "local"

    use_saas = effective_mode == "saas"
    effective_api_key = api_key if not use_saas else None
    effective_saas_token = saas_token if use_saas else None
    
    return effective_mode, effective_api_key, effective_saas_token


def _get_filter_str(
    specific_date: Optional[str],
    since: Optional[str],
    until: Optional[str],
    full_history: bool
) -> str:
    """Build human-friendly filter description."""
    filter_desc = []
    if specific_date:
        filter_desc.append(f"date={specific_date}")
    elif since or until or full_history:
        if full_history:
            filter_desc.append("full history")
        else:
            if since:
                filter_desc.append(f"since={since}")
            if until:
                filter_desc.append(f"until={until}")
    
    return " | ".join(filter_desc) if filter_desc else "last commits"


def _display_results(results: dict, output: Path, model_name: str):
    """Summarize and export analysis results."""
    summary = results["summary"]
    
    # Output results
    typer.echo()
    typer.echo("=" * 50)
    typer.echo(f"📊 AI COST ANALYSIS - {model_name}")
    typer.echo("=" * 50)
    typer.echo(f"   Commits analyzed: {summary['total_commits']}")
    typer.echo(f"   Total cost:       {summary['total_cost_formatted']}")
    typer.echo(f"   Hours saved:      {summary['total_hours_saved']:.1f}h")
    typer.echo(f"   Value generated:  ${summary['total_value_generated']:.2f}")
    typer.echo(f"   ROI:              {summary['average_roi']}")
    typer.echo("=" * 50)
    
    # Export to CSV
    df = pd.DataFrame(results["commits"])
    df.to_csv(output, index=False)
    typer.echo(f"📁 Results saved to: {output}")
    
    # Show sample
    if len(results["commits"]) > 0:
        typer.echo()
        typer.echo("💡 Recent AI commits:")
        for c in results["commits"][:5]:
            msg = c["commit_message"][:40].replace("\n", " ")
            typer.echo(f"   {c['commit_hash']} | {c['cost_formatted']} | {msg}")


def analyze_logic(
    repo: Path,
    model: str,
    api_key: str,
    saas_token: str,
    mode: str,
    max_commits: int,
    output: Path,
    ai_only: bool,
    all_commits: bool,
    saas_url: str,
    since: Optional[str],
    until: Optional[str],
    specific_date: Optional[str],
    full_history: bool,
):
    """Logic for analyze command."""
    git_repo = _get_repo(repo)
    
    # Determine mode and credentials
    effective_mode, effective_api_key, effective_saas_token = _get_execution_context(
        mode, api_key, saas_token
    )

    # Convert to liteLLM format
    litellm_model = get_litellm_model_name(model)
    filter_str = _get_filter_str(specific_date, since, until, full_history)
    
    # Handle ai_only vs all_commits logic
    effective_ai_only = ai_only and not all_commits
    
    typer.echo(f"🔍 Analyzing {max_commits} commits from {get_repo_name(git_repo)}...")
    typer.echo(f"🤖 Model: {litellm_model} | Mode: {effective_mode} | Filter: {filter_str}")
    
    # Parse commits with date filtering
    commits_data = parse_commits(
        str(repo),
        max_count=max_commits,
        ai_only=effective_ai_only,
        since=since,
        until=until,
        specific_date=specific_date,
        full_history=full_history
    )
    
    if not commits_data:
        typer.echo("⚠️  No commits found. Use --all to analyze all commits.")
        raise typer.Exit(0)
    
    # Calculate costs
    results = batch_calculate_costs(
        commits_data,
        model=litellm_model,
        api_key=effective_api_key,
        saas_token=effective_saas_token
    )
    
    _display_results(results, output, litellm_model)

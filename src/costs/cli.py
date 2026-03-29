"""CLI for AI Cost Tracker with liteLLM integration."""

import os
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

from .models import DEFAULT_MODEL
from .commands.analyze import analyze_logic
from .commands.report import report_logic
from .commands.badge import badge_logic, auto_badge_logic
from .commands.utils import estimate_logic, stats_logic, init_logic

# Load .env for CLI defaults
load_dotenv()

app = typer.Typer(help="AI Cost Tracker - Zero-config AI cost calculator per commit/model")


def version_callback(value: bool):
    if value:
        typer.echo("ai-cost-tracker 0.1.39")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
):
    pass


@app.command()
def analyze(
    repo: Path = typer.Argument(..., help="Path to git repository"),
    model: str = typer.Option(
        os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next"),
        "--model", "-m",
        help="AI model to use (default from .env LLM_MODEL)"
    ),
    api_key: str = typer.Option(
        os.getenv("OPENROUTER_API_KEY", ""),
        "--api-key",
        help="OpenRouter API key (default from .env OPENROUTER_API_KEY)"
    ),
    saas_token: str = typer.Option("", "--saas-token", help="SaaS subscription token (optional)"),
    mode: str = typer.Option("auto", "--mode", help="Calculation mode: auto, byok, local, saas"),
    max_commits: int = typer.Option(100, "--max-commits", "-n", help="Max commits to analyze"),
    output: Path = typer.Option(Path("ai_costs.csv"), "--output", "-o", help="Output CSV file"),
    ai_only: bool = typer.Option(True, "--ai-only", help="Only analyze commits with [ai:] tag"),
    all_commits: bool = typer.Option(False, "--all", help="Analyze all commits (not just AI-tagged)"),
    saas_url: str = typer.Option("https://your-saas.com/api/cost", "--saas-url", help="SaaS API endpoint"),
    since: Optional[str] = typer.Option(None, "--since", help="Start date (YYYY-MM-DD) - analyze commits from this date"),
    until: Optional[str] = typer.Option(None, "--until", help="End date (YYYY-MM-DD) - analyze commits until this date"),
    specific_date: Optional[str] = typer.Option(None, "--date", help="Specific date (YYYY-MM-DD) - analyze only this day"),
    full_history: bool = typer.Option(False, "--full-history", help="Analyze all commits since repository creation"),
):
    """Analyze AI costs for git commits with liteLLM support."""
    analyze_logic(
        repo, model, api_key, saas_token, mode, max_commits, output, 
        ai_only, all_commits, saas_url, since, until, specific_date, full_history
    )


@app.command()
def report(
    repo: Path = typer.Argument(..., help="Path to git repository"),
    model: str = typer.Option(
        os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next"),
        "--model", "-m",
        help="AI model to use"
    ),
    format: str = typer.Option("markdown", "--format", "-f", help="Report format: markdown, html, both"),
    output_dir: Path = typer.Option(Path("cost-reports"), "--output", "-o", help="Output directory"),
    update_readme: bool = typer.Option(False, "--update-readme", help="Update README.md with badge"),
):
    """Generate cost reports with visualizations."""
    report_logic(repo, model, format, output_dir, update_readme)


@app.command()
def badge(
    repo: Path = typer.Argument(..., help="Path to git repository"),
    model: str = typer.Option(
        os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next"),
        "--model", "-m",
        help="AI model to use"
    ),
    all_commits: bool = typer.Option(False, "--all", help="Analyze all commits (not just AI-tagged)"),
):
    """Generate or update cost badge in README.md."""
    badge_logic(repo, model, all_commits)


@app.command()
def auto_badge(
    repo: Path = typer.Option(Path("."), "--repo", "-r", help="Path to git repository"),
    all_commits: bool = typer.Option(False, "--all", help="Analyze all commits (not just AI-tagged)"),
):
    """Auto-generate badge based on pyproject.toml [tool.costs] configuration."""
    auto_badge_logic(repo, all_commits)


@app.command()
def estimate(
    diff_file: Path = typer.Argument(..., help="Path to diff file or '-' for stdin"),
    model: str = typer.Option(
        os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next"),
        "--model", "-m",
        help="AI model to use (default from .env LLM_MODEL)"
    ),
):
    """Estimate cost for a single diff using liteLLM token counting."""
    estimate_logic(diff_file, model)


@app.command()
def stats(
    repo: Path = typer.Argument(..., help="Path to git repository"),
):
    """Show repository statistics including commit history."""
    stats_logic(repo)


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing configuration"),
    auto: bool = typer.Option(False, "--auto", "-a", help="Auto-configure project with all defaults"),
):
    """Initialize AI cost tracking for current project."""
    init_logic(force, auto)


def main():
    app()


if __name__ == "__main__":
    main()

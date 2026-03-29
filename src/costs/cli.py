"""CLI for AI Cost Tracker with liteLLM integration."""

import os
from pathlib import Path
from typing import Optional

import typer
import pandas as pd
import git
from dotenv import load_dotenv

from .calculator import batch_calculate_costs, ai_cost
from .git_parser import parse_commits, get_repo_name, get_repo_stats
from .models import DEFAULT_MODEL, DEFAULT_OPENROUTER_API_KEY, get_litellm_model_name

# Load .env for CLI defaults
load_dotenv()


app = typer.Typer(help="AI Cost Tracker - Zero-config AI cost calculator per commit/model")


def version_callback(value: bool):
    if value:
        typer.echo("ai-cost-tracker 0.1.0")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
):
    pass


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
    if not repo.exists():
        typer.echo(f"❌ Repository not found: {repo}", err=True)
        raise typer.Exit(1)
    
    try:
        git_repo = git.Repo(repo)
    except git.InvalidGitRepositoryError:
        typer.echo(f"❌ Not a git repository: {repo}", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"📊 Analyzing repository: {get_repo_name(git_repo)}")
    typer.echo(f"🤖 Using model: {model}")
    
    # Analyze commits
    commits_data = parse_commits(str(repo), max_count=1000, ai_only=True, full_history=True)
    if not commits_data:
        typer.echo("⚠️  No AI commits found in repository")
        raise typer.Exit(0)
    
    # Calculate costs
    results = batch_calculate_costs(commits_data, model=model)
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Generate reports
    if format in ("markdown", "both"):
        md_path = output_dir / "cost-report.md"
        from .reports import generate_markdown_report
        generate_markdown_report(results, md_path)
        typer.echo(f"✅ Markdown report: {md_path}")
    
    if format in ("html", "both"):
        html_path = output_dir / "cost-report.html"
        from .reports import generate_html_report
        generate_html_report(results, html_path)
        typer.echo(f"✅ HTML report: {html_path}")
    
    # Update README if requested
    if update_readme:
        from .reports import update_readme_badge
        if update_readme_badge(repo, results):
            typer.echo(f"✅ Updated README.md with badge")
        else:
            typer.echo("⚠️  README.md not found, skipping badge update")
    
    # Print summary
    summary = results["summary"]
    typer.echo()
    typer.echo("=" * 50)
    typer.echo("📊 COST REPORT SUMMARY")
    typer.echo("=" * 50)
    typer.echo(f"   Total Cost: {summary['total_cost_formatted']}")
    typer.echo(f"   AI Commits: {summary['total_commits']}")
    typer.echo(f"   Hours Saved: {summary['total_hours_saved']:.1f}h")
    typer.echo(f"   ROI: {summary['average_roi']}")
    typer.echo("=" * 50)


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
    if not repo.exists():
        typer.echo(f"❌ Repository not found: {repo}", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"📊 Analyzing repository for badge...")
    
    # Analyze commits
    commits_data = parse_commits(str(repo), max_count=1000, ai_only=not all_commits, full_history=True)
    if not commits_data:
        if all_commits:
            typer.echo("⚠️  No commits found")
        else:
            typer.echo("⚠️  No AI commits found. Use --all to analyze all commits.")
        raise typer.Exit(0)
    
    # Calculate costs
    results = batch_calculate_costs(commits_data, model=model)
    
    # Update README
    from .reports import update_readme_badge
    if update_readme_badge(repo, results):
        typer.echo(f"✅ Badge updated in README.md")
        summary = results["summary"]
        typer.echo(f"   Cost: {summary['total_cost_formatted']}")
        typer.echo(f"   Commits: {summary['total_commits']}")
        typer.echo(f"   Model: {summary['model']}")
    else:
        typer.echo("❌ README.md not found")
        raise typer.Exit(1)


@app.command()
def auto_badge(
    repo: Path = typer.Option(Path("."), "--repo", "-r", help="Path to git repository"),
    all_commits: bool = typer.Option(False, "--all", help="Analyze all commits (not just AI-tagged)"),
):
    """Auto-generate badge based on pyproject.toml [tool.costs] configuration.
    
    This command reads configuration from pyproject.toml and automatically
    generates or updates the badge in README.md.
    """
    import tomllib
    
    # Read pyproject.toml config
    pyproject_path = repo / "pyproject.toml"
    if not pyproject_path.exists():
        typer.echo("❌ pyproject.toml not found", err=True)
        raise typer.Exit(1)
    
    try:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        tool_config = config.get("tool", {}).get("costs", {})
    except Exception as e:
        typer.echo(f"❌ Error reading pyproject.toml: {e}", err=True)
        raise typer.Exit(1)
    
    # Check if badge generation is enabled
    if not tool_config.get("badge", True):
        typer.echo("ℹ️  Badge generation disabled in pyproject.toml")
        raise typer.Exit(0)
    
    if not repo.exists():
        typer.echo(f"❌ Repository not found: {repo}", err=True)
        raise typer.Exit(1)
    
    try:
        git_repo = git.Repo(repo)
    except git.InvalidGitRepositoryError:
        typer.echo(f"❌ Not a git repository: {repo}", err=True)
        raise typer.Exit(1)
    
    model = tool_config.get("default_model", DEFAULT_MODEL)
    full_history = tool_config.get("full_history", False)
    max_commits = tool_config.get("max_commits", 1000)
    
    typer.echo(f"🔍 Analyzing repository: {get_repo_name(git_repo)}")
    typer.echo(f"🤖 Model: {model}")
    
    # Analyze commits
    commits_data = parse_commits(
        str(repo),
        max_count=max_commits,
        ai_only=not all_commits,
        full_history=full_history
    )
    
    if not commits_data:
        if all_commits:
            typer.echo("⚠️  No commits found")
        else:
            typer.echo("⚠️  No AI commits found. Use --all to analyze all commits.")
        raise typer.Exit(0)
    
    # Calculate costs
    results = batch_calculate_costs(commits_data, model=model)
    
    # Update README
    from .reports import update_readme_badge
    if update_readme_badge(repo, results):
        typer.echo(f"✅ Badge updated in README.md")
        summary = results["summary"]
        typer.echo(f"   Cost: {summary['total_cost_formatted']}")
        typer.echo(f"   Commits: {summary['total_commits']}")
        typer.echo(f"   Model: {summary['model']}")
    else:
        readme_path = tool_config.get("readme_path", "README.md")
        typer.echo(f"❌ {readme_path} not found")
        raise typer.Exit(1)


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
    if str(diff_file) == "-":
        import sys
        diff_content = sys.stdin.read()
    else:
        if not diff_file.exists():
            typer.echo(f"❌ File not found: {diff_file}", err=True)
            raise typer.Exit(1)
        diff_content = diff_file.read_text()
    
    litellm_model = get_litellm_model_name(model)
    result = ai_cost(diff_content, model=litellm_model)
    
    typer.echo()
    typer.echo(f"💰 Estimated cost: {result['cost_formatted']}")
    typer.echo(f"🤖 Model: {litellm_model}")
    typer.echo(f"📊 Tokens: {result['tokens']['total']:,} (in: {result['tokens']['input']:,}, out: {result['tokens']['output']:,})")
    typer.echo(f"⚡ ROI: {result['roi_formatted']}")


@app.command()
def stats(
    repo: Path = typer.Argument(..., help="Path to git repository"),
):
    """Show repository statistics including commit history."""
    if not repo.exists():
        typer.echo(f"❌ Repository not found: {repo}", err=True)
        raise typer.Exit(1)
    
    try:
        git_repo = git.Repo(repo)
    except git.InvalidGitRepositoryError:
        typer.echo(f"❌ Not a git repository: {repo}", err=True)
        raise typer.Exit(1)
    
    repo_stats = get_repo_stats(str(repo))
    
    typer.echo()
    typer.echo("📊 Repository Statistics")
    typer.echo("=" * 40)
    typer.echo(f"   Repository: {repo_stats['repo_name']}")
    typer.echo(f"   Total commits: {repo_stats['total_commits']}")
    if repo_stats['first_commit_date']:
        typer.echo(f"   First commit: {repo_stats['first_commit_date']}")
    if repo_stats['last_commit_date']:
        typer.echo(f"   Last commit: {repo_stats['last_commit_date']}")
    typer.echo("=" * 40)


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing configuration"),
    auto: bool = typer.Option(False, "--auto", "-a", help="Auto-configure project with all defaults"),
):
    """Initialize AI cost tracking for current project.
    
    Creates .env file and adds [tool.costs] to pyproject.toml if present.
    Use --auto for non-interactive setup.
    """
    project_dir = Path(".").resolve()
    
    # --- 1. Setup .env file ---
    env_path = project_dir / ".env"
    env_template = """# AI Cost Tracking Configuration
# Get your API key from: https://openrouter.ai/keys

# OpenRouter API Key (required for real cost calculation)
OPENROUTER_API_KEY=

# Default AI model for cost analysis
LLM_MODEL=openrouter/qwen/qwen3-coder-next
"""
    
    if env_path.exists() and not force:
        typer.echo("⚠️  .env file already exists. Use --force to overwrite.")
    else:
        env_path.write_text(env_template)
        typer.echo("✅ Created .env file")
    
    # --- 2. Setup pyproject.toml [tool.costs] ---
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding='utf-8')
        
        if '[tool.costs]' in content and not force:
            typer.echo("⚠️  [tool.costs] already configured in pyproject.toml")
        else:
            costs_config = '''\n[tool.costs]
# AI Cost tracking configuration
badge = true
update_readme = true
readme_path = "README.md"
default_model = "openrouter/qwen/qwen3-coder-next"
analysis_mode = "byok"
full_history = true
max_commits = 500

# Cost thresholds for badge colors (USD)
badge_color_thresholds = { low = 1.0, medium = 5.0, high = 10.0, critical = 50.0 }
'''
            with open(pyproject, 'a', encoding='utf-8') as f:
                f.write(costs_config)
            typer.echo("✅ Added [tool.costs] to pyproject.toml")
    
    # --- 3. Ensure .gitignore ignores .env ---
    gitignore = project_dir / ".gitignore"
    gitignore_entry = ".env\n"
    if gitignore.exists():
        content = gitignore.read_text(encoding='utf-8')
        if '.env' not in content:
            with open(gitignore, 'a', encoding='utf-8') as f:
                f.write('\n# Environment variables\n' + gitignore_entry)
            typer.echo("✅ Added .env to .gitignore")
    else:
        gitignore.write_text(gitignore_entry + ".env.local\n")
        typer.echo("✅ Created .gitignore with .env")
    
    # --- Summary ---
    typer.echo()
    typer.echo("=" * 50)
    typer.echo("🤖 AI Cost Tracking initialized!")
    typer.echo("=" * 50)
    typer.echo("Next steps:")
    typer.echo("1. Edit .env and add your OPENROUTER_API_KEY")
    typer.echo("2. Run: costs auto-badge --repo . --all")
    typer.echo("=" * 50)


def main():
    app()


if __name__ == "__main__":
    main()

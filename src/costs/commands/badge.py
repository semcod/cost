from pathlib import Path
import typer
import git
from ..calculator import batch_calculate_costs
from ..git_parser import parse_commits, get_repo_name
from ..models import DEFAULT_MODEL

def badge_logic(
    repo: Path,
    model: str,
    all_commits: bool,
):
    """Logic for badge command."""
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
    from ..reports import update_readme_badge
    if update_readme_badge(repo, results):
        typer.echo(f"✅ Badge updated in README.md")
        summary = results["summary"]
        typer.echo(f"   Cost: {summary['total_cost_formatted']}")
        typer.echo(f"   Commits: {summary['total_commits']}")
        typer.echo(f"   Model: {summary['model']}")
    else:
        typer.echo("❌ README.md not found")
        raise typer.Exit(1)


def auto_badge_logic(
    repo: Path,
    all_commits: bool,
):
    """Logic for auto-badge command."""
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
    from ..reports import update_readme_badge
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

import os
from pathlib import Path
import typer
import git
from ..calculator import batch_calculate_costs
from ..git_parser import parse_commits, get_repo_name

def report_logic(
    repo: Path,
    model: str,
    format: str,
    output_dir: Path,
    update_readme: bool,
):
    """Logic for report command."""
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
        from ..reports import generate_markdown_report
        generate_markdown_report(results, md_path)
        typer.echo(f"✅ Markdown report: {md_path}")
    
    if format in ("html", "both"):
        html_path = output_dir / "cost-report.html"
        from ..reports import generate_html_report
        generate_html_report(results, html_path)
        typer.echo(f"✅ HTML report: {html_path}")
    
    # Update README if requested
    if update_readme:
        from ..reports import update_readme_badge
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

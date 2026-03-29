import sys
from pathlib import Path
import typer
import git
from ..calculator import ai_cost
from ..git_parser import get_repo_stats
from ..models import get_litellm_model_name

def estimate_logic(
    diff_file: Path,
    model: str,
):
    """Logic for estimate command."""
    if str(diff_file) == "-":
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


def stats_logic(
    repo: Path,
):
    """Logic for stats command."""
    if not repo.exists():
        typer.echo(f"❌ Repository not found: {repo}", err=True)
        raise typer.Exit(1)
    
    try:
        git.Repo(repo)
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


def init_logic(
    force: bool,
    auto: bool,
):
    """Logic for init command."""
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

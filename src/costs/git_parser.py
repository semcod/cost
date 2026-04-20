"""Git commit parsing utilities."""

import re
from datetime import datetime, date
from typing import List, Optional, Tuple, Union
import git


def get_commit_diff(repo: git.Repo, commit: git.Commit) -> str:
    """Get diff for a commit."""
    if not commit.parents:
        # First commit in repo - get full tree diff
        return commit.tree.diff(git.Tree.NULL_TREE).__str__()
    
    parent = commit.parents[0]
    diff = parent.diff(commit, create_patch=True)
    
    result = []
    for d in diff:
        if d.diff:
            result.append(d.diff.decode('utf-8', errors='ignore') if isinstance(d.diff, bytes) else str(d.diff))
    
    return "\n".join(result)


def is_ai_commit(commit: git.Commit, tag_pattern: str = r"\[ai:") -> bool:
    """Check if commit message contains AI tag."""
    return bool(re.search(tag_pattern, commit.message))


def extract_ai_tag(commit: git.Commit) -> Optional[str]:
    """Extract AI tag from commit message."""
    match = re.search(r"\[ai:([^\]]+)\]", commit.message)
    return match.group(1) if match else None


def is_commit_in_date_range(
    commit: git.Commit,
    since: Optional[Union[date, datetime]] = None,
    until: Optional[Union[date, datetime]] = None,
    specific_date: Optional[date] = None
) -> bool:
    """Check if commit falls within date range.
    
    Args:
        commit: Git commit object
        since: Start date (inclusive)
        until: End date (inclusive)
        specific_date: Exact date to match (overrides since/until)
    
    Returns:
        True if commit is within the specified date range
    """
    commit_date = commit.committed_datetime.date()
    
    if specific_date:
        return commit_date == specific_date
    
    if since and commit_date < since:
        return False
    
    if until and commit_date > until:
        return False
    
    return True


def get_first_commit_date(repo: git.Repo) -> date:
    """Get the date of the first commit in the repository."""
    try:
        # Get all commits and find the oldest one
        all_commits = list(repo.iter_commits('--all'))
        if not all_commits:
            return date.today()
        
        # The last commit in the list is the oldest (first)
        oldest_commit = all_commits[-1]
        return oldest_commit.committed_datetime.date()
    except Exception:
        return date.today()


def _to_date(val: Optional[Union[date, datetime, str]]) -> Optional[date]:
    """Helper to convert various types to a date object."""
    if val is None:
        return None
    if isinstance(val, str):
        return datetime.strptime(val, "%Y-%m-%d").date()
    if isinstance(val, datetime):
        return val.date()
    return val


def _parse_date_args(
    repo: git.Repo,
    since: Optional[Union[date, datetime, str]] = None,
    until: Optional[Union[date, datetime, str]] = None,
    specific_date: Optional[Union[date, str]] = None,
    full_history: bool = False
) -> Tuple[Optional[date], Optional[date], Optional[date]]:
    """Parse various date argument formats into standard date objects."""
    if specific_date:
        return None, None, _to_date(specific_date)
    
    parsed_since = _to_date(since)
    parsed_until = _to_date(until)
    
    if full_history and not parsed_since:
        parsed_since = get_first_commit_date(repo)
            
    return parsed_since, parsed_until, None


def parse_commits(
    repo_path: str,
    max_count: int = 100,
    ai_only: bool = True,
    since: Optional[Union[date, datetime, str]] = None,
    until: Optional[Union[date, datetime, str]] = None,
    specific_date: Optional[Union[date, str]] = None,
    full_history: bool = False
) -> List[Tuple[git.Commit, str]]:
    """Parse commits from repository with date filtering."""
    repo = git.Repo(repo_path)
    commits = []
    
    # Parse date arguments
    parsed_since, parsed_until, parsed_specific = _parse_date_args(
        repo, since, until, specific_date, full_history
    )
    
    # Determine max_count for full history
    iter_count = max_count if not full_history else None
    
    for commit in repo.iter_commits(max_count=iter_count):
        # Check AI tag filter
        if ai_only and not is_ai_commit(commit):
            continue
        
        # Check date filters
        if not is_commit_in_date_range(commit, parsed_since, parsed_until, parsed_specific):
            continue
        
        diff = get_commit_diff(repo, commit)
        commits.append((commit, diff))
    
    return commits


def get_repo_name(repo: git.Repo) -> str:
    """Get repository name from git remote or directory."""
    try:
        origin = repo.remote("origin")
        url = origin.url
        # Extract repo name from URL
        if url.endswith('.git'):
            url = url[:-4]
        return url.split('/')[-1]
    except:
        return repo.working_dir.split('/')[-1]


def get_repo_stats(repo_path: str) -> dict:
    """Get repository statistics including first commit date."""
    repo = git.Repo(repo_path)
    
    all_commits = list(repo.iter_commits('--all'))
    first_commit = all_commits[-1] if all_commits else None
    last_commit = all_commits[0] if all_commits else None
    
    return {
        "total_commits": len(all_commits),
        "first_commit_date": first_commit.committed_datetime.date() if first_commit else None,
        "last_commit_date": last_commit.committed_datetime.date() if last_commit else None,
        "repo_name": get_repo_name(repo)
    }

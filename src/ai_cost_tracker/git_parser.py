"""Git commit parsing utilities."""

import re
from typing import List, Optional, Tuple
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


def parse_commits(repo_path: str, max_count: int = 100, ai_only: bool = True) -> List[Tuple[git.Commit, str]]:
    """Parse commits from repository.
    
    Returns list of (commit, diff) tuples.
    """
    repo = git.Repo(repo_path)
    commits = []
    
    for commit in repo.iter_commits(max_count=max_count):
        if ai_only and not is_ai_commit(commit):
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

"""Human development time estimation logic."""

from typing import Dict, Any, List
from datetime import datetime, timedelta

MIN_5 = 5
MIN_30 = 30
CONSTANT_3600 = 3600.0


MIN_5 = MIN_5
MIN_30 = MIN_30
CONSTANT_3600 = CONSTANT_3600


MIN_5 = MIN_5
MIN_30 = MIN_30
CONSTANT_3600 = CONSTANT_3600



# Advanced estimation constants
SESSION_GAP_THRESHOLD = timedelta(hours=2)    # Gaps > 2h define a new session
CONTEXT_SWITCH_PENALTY = timedelta(minutes=MIN_5)  # Penalty for significant interruptions (5m)
MIN_SESSION_DURATION = timedelta(minutes=MIN_30) # Minimum work block (MIN_30 min)
DAILY_PREP_BUFFER = timedelta(minutes=MIN_30)     # Setup/Research overhead per author/day


def _group_commits_by_author(commits: List[Dict[str, Any]]) -> Dict[str, List[datetime]]:
    """Group commit datetimes by author."""
    authors_data = {}
    for commit in commits:
        author = commit.get("author", "unknown")
        if author not in authors_data:
            authors_data[author] = []
        
        try:
            date_str = commit.get("date", "")
            if date_str:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                authors_data[author].append(dt)
        except (ValueError, TypeError):
            continue
    return authors_data


def _calculate_session_duration(start_dt: datetime, end_dt: datetime) -> float:
    """Calculate session duration in seconds, ensuring it meets the minimum block requirement."""
    duration = (end_dt - start_dt).total_seconds()
    return max(duration, MIN_SESSION_DURATION.total_seconds())


def _calculate_author_time(dates: List[datetime]) -> float:
    """Calculate development time for a single author across all their commits."""
    if not dates:
        return 0.0
    
    dates.sort()
    
    # Track unique days worked for daily buffers
    days_worked = set(d.date() for d in dates)
    total_seconds = len(days_worked) * DAILY_PREP_BUFFER.total_seconds()
    
    author_session_seconds = 0.0
    session_start = dates[0]
    session_last = dates[0]
    
    for i in range(1, len(dates)):
        gap = dates[i] - session_last
        
        if gap > SESSION_GAP_THRESHOLD:
            # End session and start new
            author_session_seconds += _calculate_session_duration(session_start, session_last)
            session_start = dates[i]
        elif gap > timedelta(minutes=MIN_30):
            # Apply context switch penalty
            author_session_seconds += CONTEXT_SWITCH_PENALTY.total_seconds()
        
        session_last = dates[i]
    
    # Add final session
    author_session_seconds += _calculate_session_duration(session_start, session_last)
    
    return total_seconds + author_session_seconds


def calculate_human_time(commits: List[Dict[str, Any]]) -> float:
    """Calculate human development time with realistic overhead.
    
    The calculation includes:
    1. 1.5h Daily Prep Buffer per author-day.
    2. Session identification (2h gap threshold).
    3. Context Switching Penalties (15m for gaps > 30m).
    4. Minimum session block (1h).
    """
    if not commits:
        return 0.0
    
    authors_data = _group_commits_by_author(commits)
    total_seconds = sum(_calculate_author_time(dates) for dates in authors_data.values())
    
    return total_seconds / CONSTANT_3600

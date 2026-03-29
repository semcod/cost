"""Human development time estimation logic."""

from typing import Dict, Any, List
from datetime import datetime, timedelta


# Advanced estimation constants
SESSION_GAP_THRESHOLD = timedelta(hours=2)    # Gaps > 2h define a new session
CONTEXT_SWITCH_PENALTY = timedelta(minutes=15) # Penalty for gaps between 30m and 2h
MIN_SESSION_DURATION = timedelta(hours=1.0)   # Minimum work block (1h)
DAILY_PREP_BUFFER = timedelta(hours=1.5)      # Setup/Research overhead per author/day


def calculate_human_time(commits: List[Dict[str, Any]]) -> float:
    """Calculate human development time with realistic overhead.
    
    1. Groups commits by Author and Date.
    2. Adds a 1.5h Daily Prep Buffer (Research/Setup) per author-day.
    3. Identifies Work Sessions (gaps > 2h).
    4. Applies Context Switching Penalty (15m) for gaps between 30m and 2h.
    5. Ensures minimum session duration (1h).
    """
    if not commits:
        return 0.0
    
    # Group commits by author
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
        except:
            continue
    
    total_seconds = 0.0
    
    for author, dates in authors_data.items():
        if not dates:
            continue
        
        dates.sort()
        
        # Track unique days worked for daily buffers
        days_worked = set(d.date() for d in dates)
        total_seconds += len(days_worked) * DAILY_PREP_BUFFER.total_seconds()
        
        session_start = dates[0]
        session_last = dates[0]
        author_session_seconds = 0.0
        
        for i in range(1, len(dates)):
            gap = dates[i] - session_last
            
            if gap > SESSION_GAP_THRESHOLD:
                # End session: duration + buffer (enforce minimum)
                session_duration = max((session_last - session_start).total_seconds(), 
                                      MIN_SESSION_DURATION.total_seconds())
                author_session_seconds += session_duration
                # Start new session
                session_start = dates[i]
            elif gap > timedelta(minutes=30):
                # Context switch penalty
                author_session_seconds += CONTEXT_SWITCH_PENALTY.total_seconds()
            
            session_last = dates[i]
        
        # Add final session for this author
        session_duration = max((session_last - session_start).total_seconds(), 
                              MIN_SESSION_DURATION.total_seconds())
        author_session_seconds += session_duration
        total_seconds += author_session_seconds
    
    return total_seconds / 3600.0

#!/usr/bin/env python3
"""Cost Trends and Analytics - track cost trends with projections."""
from datetime import datetime, timedelta
import random


if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Example: Cost Trends and Analytics")
    print("=" * 60)

def generate_sample_data(days=30):
    """Generate sample daily cost data."""
    data = []
    base_cost = 0.5
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        weekday_factor = 1.5 if date.weekday() < 5 else 0.5
        daily_cost = base_cost * weekday_factor * (0.8 + random.random() * 0.4)
        commits = int(3 * weekday_factor * (0.5 + random.random()))
        
        data.append({
            "date": date,
            "cost": daily_cost,
            "commits": max(1, commits),
            "tokens": int(daily_cost * 1000000 / 3)
        })
    
    return data

data = generate_sample_data(30)

# Calculate metrics
total_cost = sum(d["cost"] for d in data)
total_commits = sum(d["commits"] for d in data)
avg_daily = total_cost / len(data)

def moving_average(data, window=7):
    result = []
    for i in range(len(data)):
        window_data = data[max(0, i-window+1):i+1]
        avg = sum(d["cost"] for d in window_data) / len(window_data)
        result.append(avg)
    return result

ma7 = moving_average(data)

    print(f"\nSummary (Last 30 days):")
    print(f"  Total cost: ${total_cost:.4f}")
    print(f"  Total commits: {total_commits}")
    print(f"  Average daily: ${avg_daily:.4f}")
    print(f"  Cost per commit: ${total_cost/total_commits:.4f}")

    print(f"\nRecent 7-day trend:")
recent_7 = data[-7:]
for i, day in enumerate(recent_7):
    ma = ma7[-7+i]
    indicator = "↑" if day["cost"] > ma else "↓" if day["cost"] < ma else "→"
    print(f"  {day['date'].strftime('%Y-%m-%d')}: ${day['cost']:.4f} "
          f"({day['commits']} commits) {indicator}")

# Projection
    print(f"\nProjection (based on 30-day average):")
monthly_projection = avg_daily * 30
yearly_projection = avg_daily * 365
    print(f"  Next month estimate: ${monthly_projection:.2f}")
    print(f"  Annual estimate: ${yearly_projection:.2f}")

# Budget alert simulation
BUDGET_THRESHOLD = 20.0
if monthly_projection > BUDGET_THRESHOLD:
    print(f"\n⚠️  ALERT: Monthly projection (${monthly_projection:.2f}) "
          f"exceeds budget (${BUDGET_THRESHOLD:.2f})")

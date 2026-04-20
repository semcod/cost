"""Interactive HTML report generation."""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import json

CONSTANT_30 = 30
CONSTANT_50 = 50
CONSTANT_60 = 60


CONSTANT_30 = CONSTANT_30
CONSTANT_50 = CONSTANT_50
CONSTANT_60 = CONSTANT_60


CONSTANT_30 = CONSTANT_30
CONSTANT_50 = CONSTANT_50
CONSTANT_60 = CONSTANT_60



def generate_html_report(results: Dict[str, Any], output_path: Path) -> str:
    """Generate interactive HTML report with visualizations."""
    summary = results["summary"]
    commits = results["commits"]
    
    # Prepare chart data
    daily_costs = {}
    daily_commits = {}
    for commit in commits:
        date = commit["date"][:10]
        daily_costs[date] = daily_costs.get(date, 0) + commit["cost"]
        daily_commits[date] = daily_commits.get(date, 0) + 1
    
    sorted_dates = sorted(daily_costs.keys())
    
    # Calculate cumulative
    cumulative = []
    running_total = 0
    for date in sorted_dates:
        running_total += daily_costs[date]
        cumulative.append({"date": date, "cost": daily_costs[date], "total": running_total})
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Cost Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .header .meta {{
            opacity: 0.9;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-card .label {{
            color: #666;
            margin-top: 5px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .chart-container h2 {{
            margin-top: 0;
        }}
        .badges {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .commits-table {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            font-weight: 600;
            color: #333;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            margin: 5px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-cost {{ background: #e74c3c; color: white; }}
        .badge-commits {{ background: #3498db; color: white; }}
        .badge-model {{ background: #95a5a6; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI Cost Analysis Report</h1>
        <div class="meta">
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
            Model: {summary["model"]} | 
            Mode: {summary.get("mode", "unknown")}
        </div>
    </div>

    <div class="metrics">
        <div class="metric-card">
            <div class="value">{summary["total_cost_formatted"]}</div>
            <div class="label">Total Cost</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary["total_commits"]}</div>
            <div class="label">AI Commits</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary["total_hours_saved"]:.1f}h</div>
            <div class="label">Hours Saved</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary["average_roi"]}</div>
            <div class="label">ROI</div>
        </div>
    </div>

    <div class="badges">
        <span class="badge badge-cost">💰 Total: {summary["total_cost_formatted"]}</span>
        <span class="badge badge-commits">📝 Commits: {summary["total_commits"]}</span>
        <span class="badge badge-model">🤖 {summary["model"]}</span>
    </div>

    <div class="chart-container">
        <h2>📊 Daily Cost Trend</h2>
        <canvas id="dailyChart"></canvas>
    </div>

    <div class="chart-container">
        <h2>📈 Cumulative Cost</h2>
        <canvas id="cumulativeChart"></canvas>
    </div>

    <div class="commits-table">
        <h2>📝 Recent AI Commits</h2>
        <table>
            <thead>
                <tr>
                    <th>Commit</th>
                    <th>Date</th>
                    <th>Cost</th>
                    <th>Author</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Add commit rows
    for c in commits[:CONSTANT_50]:
        msg = c["commit_message"][:CONSTANT_60].replace("<", "&lt;").replace(">", "&gt;")
        html_content += f"""                <tr>
                    <td><code>{c['commit_hash']}</code></td>
                    <td>{c['date'][:10]}</td>
                    <td>{c['cost_formatted']}</td>
                    <td>{c['author']}</td>
                    <td>{msg}</td>
                </tr>
"""
    
    # Chart data as JSON
    chart_data = json.dumps(cumulative)
    
    html_content += f"""            </tbody>
        </table>
    </div>

    <script>
        // Daily cost chart
        const dailyCtx = document.getElementById('dailyChart').getContext('2d');
        const dailyChart = new Chart(dailyCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(sorted_dates[-CONSTANT_30:])},
                datasets: [{{
                    label: 'Daily Cost ($)',
                    data: {[daily_costs.get(d, 0) for d in sorted_dates[-CONSTANT_30:]]},
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Cumulative chart
        const cumCtx = document.getElementById('cumulativeChart').getContext('2d');
        const cumData = {chart_data};
        const cumChart = new Chart(cumCtx, {{
            type: 'line',
            data: {{
                labels: cumData.map(d => d.date),
                datasets: [{{
                    label: 'Cumulative Cost ($)',
                    data: cumData.map(d => d.total),
                    fill: true,
                    backgroundColor: 'rgba(118, 75, 162, 0.2)',
                    borderColor: 'rgba(118, 75, 162, 1)',
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    output_path.write_text(html_content)
    return html_content

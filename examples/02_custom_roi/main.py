#!/usr/bin/env python3
"""Custom ROI Analysis - customize ROI calculations with different parameters."""
from costs.calculator import calculate_roi


if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Example: Custom ROI Analysis")
    print("=" * 60)

# Scenario parameters
scenarios = [
    {
        "name": "Junior Developer",
        "cost": 0.50,
        "lines_changed": 150,
        "hourly_rate": 50.0,
        "loc_per_hour": 80,
        "review_overhead": 0.3  # 30% review time
    },
    {
        "name": "Senior Developer",
        "cost": 0.50,
        "lines_changed": 150,
        "hourly_rate": 150.0,
        "loc_per_hour": 120,
        "review_overhead": 0.2  # 20% review time
    },
    {
        "name": "Consultant",
        "cost": 0.50,
        "lines_changed": 150,
        "hourly_rate": 250.0,
        "loc_per_hour": 100,
        "review_overhead": 0.25
    },
]

    print(f"\n{'Scenario':<20} {'Cost':>8} {'Hours Saved':>12} {'Value':>12} {'ROI':>8}")
    print("-" * 70)

for scenario in scenarios:
    roi = calculate_roi(
        cost=scenario["cost"],
        lines_changed=scenario["lines_changed"],
        hourly_rate=scenario["hourly_rate"],
        review_factor=scenario["review_overhead"]
    )
    
    # Adjust hours saved based on custom LOC/hour
    hours_saved_gross = scenario["lines_changed"] / scenario["loc_per_hour"]
    review_time = hours_saved_gross * scenario["review_overhead"]
    hours_saved_net = max(hours_saved_gross - review_time, 0)
    value = hours_saved_net * scenario["hourly_rate"]
    
    print(f"{scenario['name']:<20} ${scenario['cost']:>6.2f} {hours_saved_net:>10.1f}h "
          f"${value:>10.2f} {roi['roi_formatted']:>8}")

    print("\n" + "-" * 70)
    print("Key insight: Higher hourly rates = higher ROI, even with same AI cost")

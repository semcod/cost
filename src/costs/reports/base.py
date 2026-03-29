"""Shared reporting utilities."""

def get_cost_color(cost: float) -> str:
    """Get badge color based on cost level."""
    if cost < 1:
        return "brightgreen"
    elif cost < 5:
        return "green"
    elif cost < 10:
        return "yellow"
    elif cost < 50:
        return "orange"
    else:
        return "red"

from __future__ import annotations

from collections import Counter
from typing import Any

RISK_WEIGHTS = {
    "opened": 5,
    "clicked": 25,
    "reported": -20,
    "training_completed": -10,
}


def summarize_campaign(events: list[dict[str, Any]]) -> dict[str, int]:
    """Summarize authorized phishing awareness simulation events.

    The model rewards safe behavior such as reporting and training completion,
    while assigning risk to simulated opens and clicks. No credential capture or
    real phishing delivery logic is included in this project.
    """
    counts = Counter(str(event.get("event_type", "unknown")) for event in events)
    risk_score = sum(RISK_WEIGHTS.get(event_type, 0) * count for event_type, count in counts.items())
    risk_score = max(0, min(100, risk_score))

    return {
        "total_events": len(events),
        "opened": counts.get("opened", 0),
        "clicked": counts.get("clicked", 0),
        "reported": counts.get("reported", 0),
        "training_completed": counts.get("training_completed", 0),
        "campaign_risk_score": risk_score,
    }

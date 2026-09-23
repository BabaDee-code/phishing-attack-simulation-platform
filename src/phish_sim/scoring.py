from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

RISK_WEIGHTS = {
    "opened": 5,
    "clicked": 25,
    "reported": -20,
    "training_completed": -10,
}


def summarize_campaign(events: list[dict[str, Any]]) -> dict[str, int]:
    """Summarize authorized phishing awareness simulation events.

    Campaign risk is the average bounded participant risk rather than a raw event
    total. This keeps scores comparable across differently sized simulations and
    prevents one participant's repeated events from dominating the campaign.
    No credential capture or real phishing delivery logic is included.
    """
    counts = Counter(str(event.get("event_type", "unknown")) for event in events)
    participant_events: dict[str, Counter[str]] = defaultdict(Counter)

    for event in events:
        user_id = str(event.get("user_id", "unknown"))
        event_type = str(event.get("event_type", "unknown"))
        participant_events[user_id][event_type] += 1

    participant_scores = [_participant_risk(user_counts) for user_counts in participant_events.values()]
    campaign_risk = round(sum(participant_scores) / len(participant_scores)) if participant_scores else 0

    participant_count = len(participant_events)
    clickers = sum(1 for user_counts in participant_events.values() if user_counts.get("clicked", 0) > 0)
    reporters = sum(1 for user_counts in participant_events.values() if user_counts.get("reported", 0) > 0)

    return {
        "total_events": len(events),
        "participants": participant_count,
        "opened": counts.get("opened", 0),
        "clicked": counts.get("clicked", 0),
        "reported": counts.get("reported", 0),
        "training_completed": counts.get("training_completed", 0),
        "click_rate_percent": _percentage(clickers, participant_count),
        "report_rate_percent": _percentage(reporters, participant_count),
        "campaign_risk_score": campaign_risk,
    }


def _participant_risk(counts: Counter[str]) -> int:
    """Return a bounded behavioral risk score for one simulation participant."""
    # Score whether a behavior occurred rather than multiplying by raw repeats.
    # A participant can therefore contribute at most one weight per behavior.
    score = sum(weight for event_type, weight in RISK_WEIGHTS.items() if counts.get(event_type, 0) > 0)
    return max(0, min(100, score))


def _percentage(numerator: int, denominator: int) -> int:
    if denominator == 0:
        return 0
    return round((numerator / denominator) * 100)

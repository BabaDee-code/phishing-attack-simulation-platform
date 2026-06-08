from phish_sim.scoring import summarize_campaign


def test_clicks_increase_campaign_risk():
    result = summarize_campaign([
        {"event_type": "opened"},
        {"event_type": "clicked"},
        {"event_type": "clicked"},
    ])
    assert result["clicked"] == 2
    assert result["campaign_risk_score"] > 0


def test_reporting_and_training_reduce_risk():
    result = summarize_campaign([
        {"event_type": "clicked"},
        {"event_type": "reported"},
        {"event_type": "training_completed"},
    ])
    assert result["reported"] == 1
    assert result["training_completed"] == 1
    assert result["campaign_risk_score"] == 0


def test_risk_score_is_capped_at_100():
    result = summarize_campaign([{"event_type": "clicked"} for _ in range(20)])
    assert result["campaign_risk_score"] == 100

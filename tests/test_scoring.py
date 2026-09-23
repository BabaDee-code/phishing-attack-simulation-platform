from phish_sim.scoring import summarize_campaign


def test_clicks_increase_campaign_risk():
    result = summarize_campaign([
        {"user_id": "U001", "event_type": "opened"},
        {"user_id": "U001", "event_type": "clicked"},
        {"user_id": "U002", "event_type": "clicked"},
    ])
    assert result["clicked"] == 2
    assert result["participants"] == 2
    assert result["campaign_risk_score"] > 0


def test_reporting_and_training_reduce_participant_risk():
    result = summarize_campaign([
        {"user_id": "U001", "event_type": "clicked"},
        {"user_id": "U001", "event_type": "reported"},
        {"user_id": "U001", "event_type": "training_completed"},
    ])
    assert result["reported"] == 1
    assert result["training_completed"] == 1
    assert result["campaign_risk_score"] == 0


def test_repeated_clicks_do_not_inflate_one_participants_risk():
    single_click = summarize_campaign([{"user_id": "U001", "event_type": "clicked"}])
    repeated_clicks = summarize_campaign(
        [{"user_id": "U001", "event_type": "clicked"} for _ in range(20)]
    )
    assert repeated_clicks["campaign_risk_score"] == single_click["campaign_risk_score"] == 25


def test_campaign_score_is_invariant_to_population_scale():
    small = summarize_campaign([
        {"user_id": "U001", "event_type": "clicked"},
        {"user_id": "U002", "event_type": "reported"},
    ])
    large = summarize_campaign([
        {"user_id": f"C{i}", "event_type": "clicked"} for i in range(10)
    ] + [
        {"user_id": f"R{i}", "event_type": "reported"} for i in range(10)
    ])
    assert small["campaign_risk_score"] == large["campaign_risk_score"]
    assert small["click_rate_percent"] == large["click_rate_percent"] == 50
    assert small["report_rate_percent"] == large["report_rate_percent"] == 50


def test_empty_campaign_has_zero_metrics():
    result = summarize_campaign([])
    assert result["participants"] == 0
    assert result["click_rate_percent"] == 0
    assert result["report_rate_percent"] == 0
    assert result["campaign_risk_score"] == 0

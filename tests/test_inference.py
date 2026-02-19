from resy_sniper.inference import parse_rule_from_text


def test_parse_explicit_pattern():
    rule = parse_rule_from_text("They release 30 days out at 09:00 sharp")
    assert rule is not None
    assert rule.days_ahead == 30
    assert rule.drop_time == "09:00"


def test_parse_missing_pattern_returns_none():
    assert parse_rule_from_text("no useful scheduling info") is None

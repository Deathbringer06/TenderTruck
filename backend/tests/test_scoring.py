from src.modules.scoring.service import check_inn


def test_check_inn_returns_mock_risk_and_reason() -> None:
    result = check_inn("1234567890")

    assert result["risk"] in {"LOW", "MEDIUM", "HIGH"}
    assert result["reason"]
    assert result == check_inn("1234567890")

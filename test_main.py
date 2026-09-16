from app.main import handler


def test_health_returns_ok():
    response = handler({"rawPath": "/health"}, None)
    assert response["statusCode"] == 200
    assert "ok" in response["body"]


def test_other_path_returns_greeting():
    response = handler({"rawPath": "/"}, None)
    assert "Hello from Lambda" in response["body"]


def test_missing_path_defaults_to_greeting():
    response = handler({}, None)
    assert "Hello from Lambda" in response["body"]

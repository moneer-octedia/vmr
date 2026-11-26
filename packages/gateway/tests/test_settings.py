import pytest
from gateway.settings import load_settings
from pydantic import ValidationError


def test_env_overrides_nested_port(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GATEWAY_DB__PASSWORD", "a-long-enough-secret")
    monkeypatch.setenv("GATEWAY_DB__PORT", "6543")

    settings = load_settings()

    assert settings.db.port == 6543


def test_secret_never_appear_in_repr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GATEWAY_DB__PASSWORD", "a-long-enough-secret")

    settings = load_settings()

    assert "a-long-enough-secret" not in repr(settings)


def test_error_names_the_bad_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GATEWAY_DB__PASSWORD", "a-long-enough-secret")
    monkeypatch.setenv("GATEWAY_DB__PORT", "99999")

    with pytest.raises(ValidationError) as exc_info:
        load_settings()

    assert exc_info.value.errors()[0]["loc"] == ("db", "port")

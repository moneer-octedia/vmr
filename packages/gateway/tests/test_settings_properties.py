import pytest
from gateway.settings import load_settings
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

env_safe_text = st.text(
    alphabet=st.characters(exclude_characters="\x00", exclude_categories=("Cs",)),
    min_size=12,
)


@given(password=env_safe_text)
def test_secret_never_in_repr(password: str) -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("GATEWAY_DB__PASSWORD", password)
        settings = load_settings()
        assert password not in repr(settings)


VALID_PASSWORD = "a-long-enough-secret"


@given(port=st.integers(min_value=1, max_value=65535))
def test_any_valid_port_is_accepted(port: int) -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("GATEWAY_DB__PASSWORD", VALID_PASSWORD)
        mp.setenv("GATEWAY_DB__PORT", str(port))
        assert load_settings().db.port == port


@given(port=st.integers(max_value=0) | st.integers(min_value=65536))
def test_any_invalid_port_is_rejected_naming_the_field(port: int) -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("GATEWAY_DB__PASSWORD", VALID_PASSWORD)
        mp.setenv("GATEWAY_DB__PORT", str(port))
        with pytest.raises(ValidationError) as exc_info:
            load_settings()
        assert [e["loc"] for e in exc_info.value.errors()] == [("db", "port")]

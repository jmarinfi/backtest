import pytest  # type: ignore
from pydantic import ValidationError

from app.core.config import Settings


def test_default_base_url_api_connect():
    """Should load default value from .env file"""
    config = Settings()  # type: ignore
    assert config.base_url_api_connect == "http://localhost:8080/api/v1/market-data"


def test_base_url_api_connect_override(monkeypatch):
    """Should load overridden value from environment variable"""
    monkeypatch.setenv("BASE_URL_API_CONNECT", "https://example.com/api")
    config = Settings()  # type: ignore
    assert config.base_url_api_connect == "https://example.com/api"


def test_missing_base_url_api_connect(monkeypatch, tmp_path):
    """
    Should raise ValidationError when env var is missing and no .env found
    """
    # Change to an empty temporary directory without .env
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.chdir(empty_dir)
    # Ensure no environment variable
    monkeypatch.delenv("BASE_URL_API_CONNECT", raising=False)

    with pytest.raises(ValidationError):
        Settings()  # type: ignore

import os
import pytest
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_config_fields():
    config = CalculatorConfig()
    assert isinstance(config.base_dir, Path)
    assert isinstance(config.max_history_size, int)
    assert isinstance(config.auto_save, bool)
    assert isinstance(config.precision, int)
    assert isinstance(config.max_input_value, Decimal)
    assert isinstance(config.default_encoding, str)


def test_path_properties_are_computed():
    base_dir = Path("/tmp").resolve()
    config = CalculatorConfig(base_dir=base_dir)
    assert config.log_dir == base_dir / "logs"
    assert config.log_file == base_dir / "logs/calculator.log"
    assert config.history_dir == base_dir / "history"
    assert config.history_file == base_dir / "history/calculator_history.csv"


def test_custom_env_override(monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", "/custom")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "42")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "12345")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-16")
    monkeypatch.setenv("CALCULATOR_LOG_FILE", "/custom/logs/log.txt")

    config = CalculatorConfig()
    assert config.base_dir == Path("/custom")
    assert config.max_history_size == 42
    assert config.auto_save is False
    assert config.precision == 4
    assert config.max_input_value == Decimal("12345")
    assert config.default_encoding == "utf-16"
    assert config.log_file == Path("/custom/logs/log.txt")


def test_config_validation_success():
    config = CalculatorConfig(
        max_history_size=10,
        precision=2,
        max_input_value=Decimal("100")
    )
    config.validate()  # Should not raise


def test_config_validation_failure():
    # Fails due to max_history_size
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            base_dir=Path("/tmp").resolve(),
            max_history_size=0,
            precision=1,
            max_input_value=Decimal("1")
        ).validate()

    # Fails due to precision
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            base_dir=Path("/tmp").resolve(),
            max_history_size=1,
            precision=0,
            max_input_value=Decimal("1")
        ).validate()

    # Fails due to max_input_value
    with pytest.raises(ConfigurationError):
        CalculatorConfig(
            base_dir=Path("/tmp").resolve(),
            max_history_size=1,
            precision=1,
            max_input_value=Decimal("-1")
        ).validate()

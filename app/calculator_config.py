from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv
from app.exceptions import ConfigurationError

load_dotenv()  # Load environment variables from .env


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@dataclass
class CalculatorConfig:
    """Holds calculator app configuration values."""

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    ):
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        self.max_history_size = int(
    max_history_size
    if max_history_size is not None
    else os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
)

        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = (
            auto_save if auto_save is not None
            else (auto_save_env == 'true' or auto_save_env == '1')
        )

        self.precision = (
            precision
            if precision is not None
            else int(os.getenv('CALCULATOR_PRECISION', '10'))
        )

        self.max_input_value = (
            max_input_value if max_input_value is not None
            else Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999'))
        )

        self.default_encoding = (
            default_encoding if default_encoding is not None
            else os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        )

    @property
    def log_dir(self) -> Path:
        """Return directory path for log files."""
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        """Return directory path for calculation history."""
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """Return file path for storing calculation history."""
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()

    @property
    def log_file(self) -> Path:
        """Return file path for storing logs."""
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
    ##validate configuration values
        if not isinstance(self.max_history_size, int) or self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")

        if not isinstance(self.precision, int) or self.precision <= 0:
            raise ConfigurationError("precision must be positive")

        if not isinstance(self.max_input_value, (int, float, Decimal)) or Decimal(self.max_input_value) <= 0:
            raise ConfigurationError("max_input_value must be positive")

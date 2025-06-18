########################
# History Management   #
########################

from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    """Abstract observer interface for reacting to new calculations."""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Handle a new calculation event."""
        pass  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """Logs each new calculation to the log file."""

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None") #pragma: no cover
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = {calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """Automatically saves history after each calculation if enabled."""

    def __init__(self, calculator: Any):
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None") #pragma: no cover
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved") #pragma: no cover

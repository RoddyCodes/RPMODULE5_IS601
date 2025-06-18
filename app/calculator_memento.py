from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """Stores calculator history and timestamp for undo/redo support."""

    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the memento to a dictionary."""
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        """Deserialize a dictionary to recreate a CalculatorMemento."""
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )

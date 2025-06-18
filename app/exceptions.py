########################
# Exception Hierarchy  #
########################

class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""
    pass


class ValidationError(CalculatorError):
    """Raised when user input is invalid (e.g., non-numeric, out of range)."""
    pass


class OperationError(CalculatorError):
    """Raised when a calculation operation fails (e.g., division by zero)."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when configuration values are missing or invalid."""
    pass

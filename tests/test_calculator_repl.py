import pytest
from unittest.mock import patch
from app.calculator_repl import calculator_repl


@patch("builtins.input", side_effect=["help", "exit"])
@patch("builtins.print")
def test_help_command(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")


@patch("builtins.input", side_effect=["save", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.save_history")
def test_save_command(mock_save, mock_print, mock_input):
    calculator_repl()
    assert mock_save.call_count >= 1
    mock_print.assert_any_call("History saved successfully")


@patch("builtins.input", side_effect=["load", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.load_history")
def test_load_command(mock_load, mock_print, mock_input):
    calculator_repl()
    assert mock_load.call_count >= 1
    mock_print.assert_any_call("History loaded successfully")


@patch("builtins.input", side_effect=["add", "100", "250", "exit"])
@patch("builtins.print")
def test_add_command(mock_print, mock_input):
    calculator_repl()
    assert any("Result" in str(call[0][0]) and "350" in str(call[0][0]) for call in mock_print.call_args_list)


@patch("builtins.input", side_effect=["unknowncmd", "exit"])
@patch("builtins.print")
def test_unknown_command(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unknown command: 'unknowncmd'. Type 'help' for available commands.")


@patch("builtins.input", side_effect=["undo", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.undo", return_value=True)
def test_undo_command(mock_undo, mock_print, mock_input):
    calculator_repl()
    mock_undo.assert_called_once()
    mock_print.assert_any_call("Operation undone")


@patch("builtins.input", side_effect=["undo", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.undo", return_value=False)
def test_undo_nothing_to_undo(mock_undo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to undo")


@patch("builtins.input", side_effect=["redo", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.redo", return_value=True)
def test_redo_command(mock_redo, mock_print, mock_input):
    calculator_repl()
    mock_redo.assert_called_once()
    mock_print.assert_any_call("Operation redone")


@patch("builtins.input", side_effect=["redo", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.redo", return_value=False)
def test_redo_nothing_to_redo(mock_redo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to redo")


@patch("builtins.input", side_effect=["clear", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.clear_history")
def test_clear_command(mock_clear, mock_print, mock_input):
    calculator_repl()
    mock_clear.assert_called_once()
    mock_print.assert_any_call("History cleared")


@patch("builtins.input", side_effect=["history", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.show_history", return_value=[])
def test_history_empty(mock_show, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("No calculations in history")


@patch("builtins.input", side_effect=["history", "exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.show_history", return_value=["5 + 3 = 8"])
def test_history_with_entries(mock_show, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("1. 5 + 3 = 8")


@patch("builtins.input", side_effect=[KeyboardInterrupt, "exit"])
@patch("builtins.print")
def test_keyboard_interrupt(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nOperation cancelled")


@patch("builtins.input", side_effect=[EOFError])
@patch("builtins.print")
def test_eof_exit(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nInput terminated. Exiting...")


@patch("builtins.input", side_effect=["exit"])
@patch("builtins.print")
@patch("app.calculator.Calculator.save_history", side_effect=Exception("fail"))
def test_exit_save_failure(mock_save, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Warning: Could not save history: fail")
    mock_print.assert_any_call("Goodbye!")

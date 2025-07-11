from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

def calculator_repl():
    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root - Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue #pragma: no cover

                if command == 'exit':
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}") #pragma: no cover
                    print("Goodbye!") #pragma: no cover
                    break #pragma: no cover

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}") #pragma: no cover
                    continue #pragma: no cover

                if command == 'clear':
                    calc.clear_history()
                    print("History cleared")
                    continue #pragma: no cover

                if command == 'undo':
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue #pragma: no cover

                if command == 'redo':
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue #pragma: no cover

                if command == 'save':
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}") #pragma: no cover
                    continue #pragma: no cover

                if command == 'load':
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}") #pragma: no cover
                    continue #pragma: no cover

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue #pragma: no cover
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue #pragma: no cover

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        result = calc.perform_operation(a, b)

                        # Format result cleanly
                        if isinstance(result, Decimal):
                            if result == result.to_integral():
                                result = str(result.quantize(Decimal("1")))
                            else:
                                result = str(result.normalize())

                        print(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                    continue #pragma: no cover

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue #pragma: no cover
            except EOFError:
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}") #pragma: no cover
                continue #pragma: no cover

    except Exception as e:
        print(f"Fatal error: {e}") #pragma: no cover
        logging.error(f"Fatal error in calculator REPL: {e}") #pragma: no cover
        raise #pragma: no cover
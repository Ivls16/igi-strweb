"""
Purpose: Custom exceptions and user input validation functions.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

class InvalidStudentDataError(Exception):
    """Custom exception raised when student data is invalid."""
    pass


def get_valid_string(prompt: str) -> str:
    """
    Safely gets a non-empty string from the user.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty.")
            return value
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""


def get_valid_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Safely gets an integer from the user within an optional range.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be at least {min_val}.")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be at most {max_val}.")
            return value
        except ValueError as e:
            print(f"Error: Invalid number. {e}. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return 0
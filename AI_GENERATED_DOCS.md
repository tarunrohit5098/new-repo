# Release Notes: Improved Greeting and Calculator Module Added

## Summary of Changes

This release includes two significant changes:

1.  **Improved `greet_user` function:** The `greet_user` function in `app.py` has been enhanced to handle invalid input more gracefully and its internal logic was changed from f-string to string concatenation.  It now explicitly checks for empty or non-string inputs, returning a more appropriate default message.

2.  **New `calculator.py` module:** A new module, `calculator.py`, has been added. This module contains the `SimpleCalculator` class, providing basic arithmetic operations (addition, subtraction, multiplication, and division).  The `divide` method includes error handling for division by zero.

## New Features / Fixes

*   **Improved Error Handling in `greet_user`:** The `greet_user` function now correctly handles cases where the input `name` is either empty or not a string.
*   **Added `SimpleCalculator` class:**  A new class, `SimpleCalculator`, provides methods for basic arithmetic operations (add, subtract, multiply, divide).
*   **Division by Zero Handling:** The `divide` method in `SimpleCalculator` includes error handling for division by zero, returning an informative error message instead of crashing.
*   **Changed `greet_user` internal logic:** The internal logic of the `greet_user` function was changed from f-string to string concatenation for better readability and maintainability.

## How to Use

**Using the `SimpleCalculator` class:**

```python
from calculator import SimpleCalculator

calculator = SimpleCalculator()

# Perform calculations
addition_result = calculator.add(5, 3)  # Result: 8
subtraction_result = calculator.subtract(10, 4)  # Result: 6
multiplication_result = calculator.multiply(7, 2)  # Result: 14
division_result = calculator.divide(15, 3)  # Result: 5.0
division_by_zero_result = calculator.divide(10, 0)  # Result: "Error: Cannot divide by zero."

print(f"Addition: {addition_result}")
print(f"Subtraction: {subtraction_result}")
print(f"Multiplication: {multiplication_result}")
print(f"Division: {division_result}")
print(f"Division by zero: {division_by_zero_result}")
```

**Using the updated `greet_user` function:**

```python
from app import greet_user

print(greet_user("Alice"))  # Output: Hello, Alice! Welcome.
print(greet_user(""))       # Output: Hello, guest!
print(greet_user(123))      # Output: Hello, guest!
```

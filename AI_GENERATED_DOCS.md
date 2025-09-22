# SimpleCalculator Update: Percentage Calculation

## Summary of Changes

This update introduces a new functionality to the `SimpleCalculator` class: percentage calculation.  The `multiply` function has been removed. The new `percentage` function allows users to calculate the percentage of one number with respect to another, handling the case of a zero denominator gracefully.


## New Features / Fixes

*   **Added:** `percentage(self, x, y)` method to calculate the percentage of `x` with respect to `y`.  The function returns a float representing the percentage or an error message if `y` is zero.
*   **Removed:** `multiply(self, x, y)` method.


## How to Use

The new `percentage` method can be used as follows:

```python
from calculator import SimpleCalculator

calc = SimpleCalculator()

# Calculate 50% of 200
result = calc.percentage(50, 200)
print(f"50% of 200 is: {result}")  # Output: 25.0

# Handle zero denominator
result = calc.percentage(10, 0)
print(f"Percentage calculation with zero denominator: {result}") # Output: Error: Cannot calculate percentage with denominator zero.

```

# calculator.py

class SimpleCalculator:
    """
    A simple calculator to perform basic arithmetic operations.
    This class holds no state.
    """

    def add(self, x, y):
        """Returns the sum of two numbers."""
        return x + y

    def subtract(self, x, y):
        """Returns the difference of two numbers."""
        return x - y

    def percentage(self, x, y):
        """
        Returns the percentage of x with respect to y.
        For example, percentage(50, 200) returns 25.0
        """
        if y == 0:
            return "Error: Cannot calculate percentage with denominator zero."
        return (x / y) * 100

    def divide(self, x, y):
        """
        Returns the division of two numbers.
        Returns an error message if division by zero occurs.
        """
        if y == 0:
            return "Error: Cannot divide by zero."
        return x / y
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

    def multiply(self, x, y):
        """Returns the product of two numbers."""
        return x * y

    def divide(self, x, y):
        """
        Returns the division of two numbers.
        Returns an error message if division by zero occurs.
        """
        if y == 0:
            return "Error: Cannot divide by zero."
        return x / y
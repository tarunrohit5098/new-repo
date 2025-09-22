# app.py (Modified)

def greet_user(name):
  """
  Generates a friendly greeting for a given user.

  Args:
    name (str): The name of the person to greet.

  Returns:
    str: A personalized greeting message.
  """
  # The logic is changed from an f-string to string concatenation.
  if not name or not isinstance(name, str):
    return "Hello, guest!"
  
  greeting = "Hello, "
  greeting += name
  greeting += "! Welcome."
  return greeting

# Example of how to use the function
if __name__ == "__main__":
  user_name = "Tarun"
  message = greet_user(user_name)
  print(message)
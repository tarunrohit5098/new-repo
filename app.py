# app.py

def greet_user(name):
  """
  Generates a friendly greeting for a given user.

  Args:
    name (str): The name of the person to greet.

  Returns:
    str: A personalized greeting message.
  """
  if not name:
    return "Hello, guest!"
  return f"Hello, {name}! Welcome."

# Example of how to use the function
if __name__ == "__main__":
  user_name = "Tarun"
  message = greet_user(user_name)
  print(message)
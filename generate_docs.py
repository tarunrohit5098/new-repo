import os
import sys
import google.generativeai as genai

# Get the API Key from GitHub Secrets
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Get the code diff from the environment variable (this is the change)
code_diff = os.environ.get("CODE_DIFF")
if not code_diff:
    print("Error: CODE_DIFF environment variable not found or is empty.")
    sys.exit(1)

# The prompt remains the same
prompt = f"""
Based on the following code changes (git diff), please act as an expert technical writer and generate clear documentation in Markdown format.

The documentation should have three sections:
1.  **Summary of Changes**: A high-level overview of what was changed.
2.  **New Features / Fixes**: A bulleted list of new features added or bugs fixed.
3.  **How to Use**: If new functions or components were added, provide a simple code example of how to use them.

Here is the code diff:
---
{code_diff}
---
"""

try:
    # Call the Gemini API
    response = model.generate_content(prompt)

    # Save the generated documentation to a file
    with open("AI_GENERATED_DOCS.md", "w") as f:
        f.write(response.text)

    print("✅ Documentation generated successfully in AI_GENERATED_DOCS.md")

except Exception as e:
    print(f"❌ Error generating documentation: {e}")
    sys.exit(1)
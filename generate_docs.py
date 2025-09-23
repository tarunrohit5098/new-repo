import os
import sys
import google.generativeai as genai

# --- Configuration ---
COMMIT_SHA = sys.argv[1] if len(sys.argv) > 1 else "latest"
DOCS_DIR = f"docs/{COMMIT_SHA}"
CODE_DIFF = os.environ.get("CODE_DIFF")

# --- Gemini API Setup ---
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"❌ Error configuring Gemini API: {e}")
    sys.exit(1)

# --- Prompt Definitions ---
def get_feature_prompt(diff):
    return f"""
    Act as an expert technical writer. Based on the following code diff, generate a high-level feature document in Markdown. Include:
    1.  **Summary of Changes**: A high-level overview of what was changed.
    2.  **New Features / Fixes**: A bulleted list of new features added or bugs fixed.
    3.  **How to Use**: If new functions or components were added, provide a simple code example.
    4.  **Visual Flowchart**: Generate a Mermaid syntax flowchart for any new complex logic.

    Code Diff:
    ---
    {diff}
    ---
    """

def get_delta_prompt(diff):
    return f"""
    Act as a senior developer performing a code review. Based on the following diff, provide a detailed, file-by-file breakdown of the changes in Markdown. For each file, explain:
    1.  **Code Delta**: Detail the differences between the old and new code.
    2.  **Technical Reasoning**: Infer the reason for the change (e.g., "refactored for efficiency," "fixed a null reference bug," "added error handling").

    Code Diff:
    ---
    {diff}
    ---
    """

# --- Main Functions ---
def generate_documentation(prompt, output_filename):
    """Generic function to call Gemini API and save the response."""
    try:
        print(f"📄 Generating {output_filename}...")
        response = model.generate_content(prompt)
        with open(os.path.join(DOCS_DIR, output_filename), "w") as f:
            f.write(response.text)
        print(f"✅ Successfully created {output_filename}")
    except Exception as e:
        print(f"❌ Error generating {output_filename}: {e}")

def main():
    if not CODE_DIFF:
        print("Error: CODE_DIFF environment variable not found or is empty.")
        sys.exit(1)

    # Generate Feature Summary (including flowchart)
    feature_prompt = get_feature_prompt(CODE_DIFF)
    generate_documentation(feature_prompt, "feature_summary.md")

    # Generate Code Delta Document
    delta_prompt = get_delta_prompt(CODE_DIFF)
    generate_documentation(delta_prompt, "code_delta.md")

if __name__ == "__main__":
    main()
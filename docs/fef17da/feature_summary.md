# Feature Document: Hybrid Payslip Data Extraction

## 1. Summary of Changes

This document details the implementation of a new Python script (`sample.py`, previously absent) that performs payslip data extraction from PDF documents using a hybrid approach.  The system leverages Google Document AI for Optical Character Recognition (OCR) and text extraction, followed by an instruction-tuned Large Language Model (LLM) via OpenAI's API (presumably using Ollama for local Llama 3 access) to structure the extracted text into a standardized JSON format.  The script includes robust error handling and debugging features.


## 2. New Features / Fixes

* **New Feature:**  Implementation of a complete payslip data extraction pipeline. This pipeline combines Google Document AI for OCR and an LLM for data structuring.
* **New Feature:**  `create_llm_prompt()` function generates a detailed prompt for the LLM, including instructions, example JSON output, and the extracted document text.
* **New Feature:**  `process_payslip_with_llm()` function orchestrates the entire process, from calling Google Document AI to processing the LLM response and handling potential errors.
* **New Feature:**  Added comprehensive error handling and debugging output, including printing the full (or truncated) document text extracted by Google Document AI and the raw LLM output.  Specific error messages are provided for easier troubleshooting.
* **Improved Data Handling:** The script now correctly handles potential multiple mentions of financial data within a single payslip, prioritizing the values found on the last page.


## 3. How to Use

The script requires the following libraries: `json`, `openai`, `google.cloud.documentai`, and `re`.  Make sure you have these installed (`pip install json openai google-cloud-documentai`).  You also need a Google Cloud project with Document AI enabled and an Ollama instance with the `llama3` model running.  Replace placeholders with your actual values:

```python
import sample

project_id = "your-google-cloud-project-id"
location = "your-google-cloud-location"  # e.g., "us"
processor_id = "your-document-ai-processor-id"
file_path = "/path/to/your/payslip.pdf"
llm_api_base = "your-ollama-api-base-url" # e.g., http://localhost:11444


results = sample.process_payslip_with_llm(project_id, location, processor_id, file_path, llm_api_base)
print(json.dumps(results, indent=2))
```

## 4. Visual Flowchart

```mermaid
graph TD
    A[Start] --> B{Google Document AI};
    B -- Success --> C[Extract Text];
    B -- Failure --> D[Error Handling];
    C --> E{Create LLM Prompt};
    E --> F{Send to LLM (Llama 3)};
    F -- Success --> G[Parse JSON Response];
    F -- Failure --> D;
    G --> H[Return JSON Data];
    H --> I[End];
    D --> I;
```

This flowchart illustrates the main steps in the payslip data extraction process.  The script incorporates error handling at various points to ensure robustness.  Detailed error messages assist in troubleshooting.

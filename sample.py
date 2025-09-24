# parser.py

import json
from openai import OpenAI
from google.cloud import documentai
from typing import List, Dict, Any
import re 

def create_llm_prompt(full_document_text: str, desired_json_example: str) -> str:
    """Creates a direct, instruction-tuned prompt for the LLM to output JSON."""
    
    prompt = f"""
You are an expert-level data extraction agent specializing in payslips. Your task is to analyze the raw text from a multi-page PDF document and convert it into a structured JSON object.

Follow these rules precisely:
1.  The document may contain multiple payslips. Identify each distinct payslip.
2.  A single payslip can span more than one page. You MUST merge all related information into a single JSON object for that payslip.
3.  A new payslip often starts immediately after the previous one ends, sometimes on the same page. A change in key dates (like `pay_date` or `end_date`), or a new employee/employer name is a strong indicator of a new payslip.
4.  For financial fields like `gross_earnings` and `net_pay`, if a value appears multiple times for the same payslip (e.g., on page 1 and page 2), the final and correct value is usually the one mentioned on the LAST page for that payslip section.
5.  Your output MUST be a single, valid JSON object. It should have one root key called "payslips", which contains a list of payslip objects. Do not include any other text or explanations in your response outside of the JSON object itself.
6.  The `payslip_number` field is crucial. If not explicitly present in the text, you must infer it or create a logical, sequential number (e.g., "00500356", "00500357") based on the order of payslips you identify. Ensure payslip numbers are unique and sequential.
7.  Ensure all fields from the example below are present in each payslip object, even if their value is null or 0.0 if not found in the document.

--- EXAMPLE OF DESIRED JSON OUTPUT STRUCTURE AND VALUES ---
{desired_json_example}
--- END OF EXAMPLE ---

Now, analyze the following document text and generate the final JSON object.

--- DOCUMENT TEXT START ---
{full_document_text}
--- DOCUMENT TEXT END ---
"""
    return prompt

def process_payslip_with_llm(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    llm_api_base: str,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Processes a PDF using a hybrid approach:
    1. Google Document AI for OCR and text extraction.
    2. A local LLM (Llama 3 via Ollama) for structuring and grouping the data.
    """
    # --- Step 1: Extract full, ordered text using Google Document AI ---
    print("Step 1: Calling Google Document AI for OCR and text extraction...")
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document_text = result.document.text
    print("✅ Text successfully extracted from Document AI.")
    
    # --- NEW DEBUGGING CODE: Print full document text and length ---
    print("\n--- Full Document Text from Document AI (for debugging) ---")
    # Print a truncated version if the text is very long, otherwise print all
    print(document_text[:4000] + "..." if len(document_text) > 4000 else document_text)
    print(f"--- Document Text Length: {len(document_text)} characters ---")
    # --- END NEW DEBUGGING CODE ---

    # --- Step 2: Use Ollama (Llama 3) to structure the extracted text into JSON ---
    print("\nStep 2: Sending extracted text to Ollama (llama3) for structuring...")
    
    # This is the desired output you provided. It's crucial for the LLM to understand the structure.
    desired_json_example = """
{
    "payslips": [
        {
            "payslip_number": "00500356",
            "employer_name": "YOUNG & RUBICAM INC.",
            "employee_name": "James Gallo",
            "pay_date": "12/15/2017",
            "start_date": "12/01/2017",
            "end_date": "12/15/2017",
            "gross_earnings": 19817.25,
            "net_pay": 17046.60
        },
        {
            "payslip_number": "00500357",
            "employer_name": "YOUNG & RUBICAM INC.",
            "employee_name": "James Gallo",
            "pay_date": "12/15/2017",
            "start_date": "12/01/2017",
            "end_date": "12/15/2017",
            "gross_earnings": 26570.12,
            "net_pay": 16694.00
        },
        {
            "payslip_number": "00520361",
            "employer_name": "YOUNG & RUBICAM INC.",
            "employee_name": "James Gallo",
            "pay_date": "12/29/2017",
            "start_date": "12/16/2017",
            "end_date": "12/31/2017",
            "gross_earnings": 23983.92,
            "net_pay": 19712.62
        }
    ]
}
"""
    
    prompt = create_llm_prompt(document_text, desired_json_example)

    try:
        llm_client = OpenAI(base_url=llm_api_base, api_key="ollama")
        
        response = llm_client.chat.completions.create(
            model="llama3", # Use the specific Llama 3 model name
            messages=[
                {"role": "system", "content": "You are an expert-level data extraction agent specializing in payslips. Your ONLY output is a valid JSON object."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0, # Keep low for deterministic, factual output
            response_format={"type": "json_object"}, # Instruct Ollama to output JSON
        )
        
        llm_output = response.choices[0].message.content
        
        print("\n--- Raw LLM Output (for debugging) ---")
        print(llm_output)
        print("---------------------------------------\n")

        json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
        if json_match:
            clean_llm_output = json_match.group(0)
            print("✅ Successfully extracted potential JSON string from LLM response.")
            return json.loads(clean_llm_output)
        else:
            raise ValueError("No valid JSON object found in LLM response.")

    except json.JSONDecodeError as jde:
        print(f"❌ JSON Decode Error: {jde}")
        print("This means the LLM response was not valid JSON even after extraction attempts.")
        return {"payslips": [], "error": f"JSON Decode Error: {jde}"}
    except Exception as e:
        print(f"❌ An error occurred during LLM communication or processing: {e}")
        print(f"Error details: {str(e)}")
        print("Please ensure Ollama is running and 'llama3' model is pulled.")
        return {"payslips": [], "error": str(e)}
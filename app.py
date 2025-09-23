# backend/app.py

import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from typing import List, Dict, Any

# --- Helper Functions (Combined for Simplicity) ---

def process_single_page_pdf(project_id: str, location: str, processor_id: str, file_content: bytes) -> List[documentai.Document.Entity]:
    """Sends a single-page PDF (as bytes) to the Document AI API."""
    try:
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        name = client.processor_path(project_id, location, processor_id)
        
        raw_document = documentai.RawDocument(content=file_content, mime_type="application/pdf")
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        
        print(f"   > Sending page to Document AI...")
        result = client.process_document(request=request)
        print(f"   > Received {len(result.document.entities)} entities from Document AI.")
        return result.document.entities
    except Exception as e:
        print(f"   > Error during Document AI processing for a page: {e}")
        return []

def extract_payslip_details(payslip_entities: List[documentai.Document.Entity]) -> Dict[str, Any]:
    """Extracts required fields from a list of entities by picking the one with the highest confidence."""
    extracted_data = {}
    required_fields = [
        "employer_name", "employee_name", "pay_date",
        "start_date", "end_date", "gross_earnings", "net_pay"
    ]
    best_entities = {}
    for entity in payslip_entities:
        if entity.type_ in required_fields:
            if entity.type_ not in best_entities or entity.confidence > best_entities[entity.type_].confidence:
                best_entities[entity.type_] = entity
                
    for field, entity in best_entities.items():
        extracted_data[field] = {
            "value": entity.mention_text.replace('\n', ' ').strip(),
            "confidence": f"{entity.confidence:.1%}"
        }
    return extracted_data

# --- Flask App and Main Pipeline ---
load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/api/ocr", methods=["POST"])
def ocr_pipeline():
    """
    This is the definitive pipeline. It treats each page of the uploaded PDF
    as a completely separate payslip. This is the most robust method to prevent
    data from different payslips from being mixed up.

    The process is:
    1. Split the PDF into individual pages in memory.
    2. Loop through each page.
    3. Make one separate API call to Document AI for each page.
    4. Extract the final fields from that page's result.
    5. Return one JSON object per page.
    """
    if 'file' not in request.files: return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if not file or file.filename == '': return jsonify({"error": "No file selected"}), 400

    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        location = os.getenv("GCP_LOCATION")
        processor_id = os.getenv("GCP_PAYSLIP_PROCESSOR_ID")
        
        file_content = file.read()
        reader = PdfReader(io.BytesIO(file_content))
        final_response = []
        
        print(f"\n--- Starting new job: Found {len(reader.pages)} pages. Processing one by one. ---")

        for i, page in enumerate(reader.pages):
            page_number = i + 1
            print(f"--- Processing Page {page_number} of {len(reader.pages)} ---")
            
            # Create a single-page PDF in a memory buffer
            writer = PdfWriter()
            writer.add_page(page)
            with io.BytesIO() as page_buffer:
                writer.write(page_buffer)
                page_buffer.seek(0)
                single_page_content = page_buffer.read()
            
            # Call Document AI for this single page
            page_entities = process_single_page_pdf(project_id, location, processor_id, single_page_content)
            
            # Format the JSON for this single payslip
            payslip_data = {
                "payslip_number": page_number,
                "page_range": f"{page_number}-{page_number}",
                "extracted_data": extract_payslip_details(page_entities)
            }
            final_response.append(payslip_data)
            
        print("--- Job complete. Sending final response. ---")
        return jsonify(final_response)

    except Exception as e:
        print(f"An unexpected error occurred in the API endpoint: {e}")
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
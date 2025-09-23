# Payslip OCR API Documentation: Update

## Summary of Changes

This update replaces a simple greeting function with a fully functional Flask-based API for Optical Character Recognition (OCR) of payslips using Google Cloud Document AI.  The API processes uploaded PDF files, splits them into individual pages, sends each page to the Document AI API for analysis, extracts key information (employer name, employee name, pay dates, gross earnings, net pay, etc.), and returns the extracted data in a structured JSON format.  Error handling and improved logging have also been implemented.

## New Features / Fixes

* **New OCR API Endpoint:** Added a `/api/ocr` POST endpoint that accepts a PDF file upload and returns extracted payslip data.
* **Multi-Page Payslip Support:** The API now handles multi-page PDF files by processing each page as a separate payslip, preventing data mixing.
* **Google Cloud Document AI Integration:**  The API integrates with Google Cloud Document AI for accurate and efficient OCR.
* **Robust Error Handling:** Improved error handling to gracefully manage file upload issues and Document AI API errors.
* **Detailed Logging:** Added logging statements to track API requests and processing steps.
* **Improved Data Extraction:** Extracts payslip details by selecting the most confident results from Document AI.
* **Configuration via Environment Variables:** Uses environment variables to configure GCP project ID, location, and processor ID.
* **Clear JSON Response:** Provides a structured JSON response with extracted data and confidence scores for each identified field.


## How to Use

To use the new OCR API, send a POST request to the `/api/ocr` endpoint with a PDF file as multipart/form-data.  The response will be a JSON array, where each element represents a page from the input PDF, containing the extracted payslip details.

**Example using `curl`:**

```bash
curl -X POST -F "file=@path/to/your/payslip.pdf" http://localhost:5000/api/ocr
```

**Example Response (JSON):**

```json
[
  {
    "payslip_number": 1,
    "page_range": "1-1",
    "extracted_data": {
      "employer_name": {
        "value": "Acme Corporation",
        "confidence": "98.5%"
      },
      "employee_name": {
        "value": "John Doe",
        "confidence": "95.2%"
      },
      "pay_date": {
        "value": "2024-03-15",
        "confidence": "99.1%"
      },
      "start_date": {
        "value": "2024-03-01",
        "confidence": "97.8%"
      },
      "end_date": {
        "value": "2024-03-31",
        "confidence": "98.1%"
      },
      "gross_earnings": {
        "value": "5000.00",
        "confidence": "96.7%"
      },
      "net_pay": {
        "value": "4000.00",
        "confidence": "97.3%"
      }
    }
  },
  {
    "payslip_number": 2,
    "page_range": "2-2",
    "extracted_data": { ... }  // Data for page 2
  }
]
```

**Before running:** Ensure you have the necessary Python packages installed (`pip install flask flask-cors google-cloud-documentai PyPDF2 python-dotenv`).  Also, set the environment variables `GCP_PROJECT_ID`, `GCP_LOCATION`, and `GCP_PAYSLIP_PROCESSOR_ID` with your Google Cloud project details.  The application assumes that a pre-trained Document AI processor for payslips is already configured.

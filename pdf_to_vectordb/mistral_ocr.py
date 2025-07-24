import os
from mistralai import Mistral

def ocr_from_pdf(pdf_file_path, api_key, language):
    """
    Perform OCR on a PDF file using Mistral's OCR service.

    :param pdf_file_path: Path to the PDF file.
    :param api_key: Mistral API key.
    :return: Extracted text from the PDF.
    """
    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Read the PDF file content
    with open(pdf_file_path, "rb") as f:
        content = f.read()

    # Upload the PDF file to Mistral and get the signed URL
    uploaded_file = client.files.upload(
        file={"file_name": os.path.basename(pdf_file_path), "content": content},
        purpose="ocr",
    )
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id)

    # Define the document source for OCR processing
    document_source = {"type": "document_url", "document_url": signed_url.url}

    try:
        # Perform OCR on the uploaded file with the specified language
        ocr_response = client.ocr.process(
            model="mistral-ocr-2505", 
            document=document_source, 
            include_image_base64=True
            # language=language  # Add language parameter here
        )

        # Extract the text from the OCR response
        # extracted_text = "\n\n".join(page.markdown for page in ocr_response.pages).strip()
        extracted_text = "\n\n".join(
        f"---Page End---\n{page.markdown.strip()}"
        for i, page in enumerate(ocr_response.pages)
    ).strip()

    except Exception as e:
        return f"Error processing OCR: {str(e)}"

    return extracted_text


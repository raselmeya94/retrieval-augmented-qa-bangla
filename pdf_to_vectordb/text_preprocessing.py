import re
from mistral_ocr import ocr_from_pdf
from langchain.schema import Document
from advanced_preprocessing import extract_answers , mcq_answering , fix_serial_numbers

def remove_jpeg_images(markdown_text: str) -> str:

    # Remove all ![...](...jpeg) or ...JPEG with case-insensitivity
    cleaned = re.sub(r'!\[.*?\]\([^)]+\.jpe?g\)', '', markdown_text, flags=re.IGNORECASE)

    return cleaned.strip()

    


def text_extractor(pdf_path, api_key , language):

    original_text= ocr_from_pdf(pdf_path, api_key , language)   # original text
    cleaned_image_tags= remove_jpeg_images(original_text)  # removed image tags
    advanced_prep_text= extract_answers(cleaned_image_tags) # Language Correction
    fix_sr_text = fix_serial_numbers(advanced_prep_text)   # MCQ Correction
    final_correction_text=  mcq_answering(fix_sr_text)

    return final_correction_text


def markdown_page_split(text: str, source: str) -> list[Document]:

    docs = []
    pages = text.split('--Page End--')

    for page_num, page in enumerate(pages, start=1):
        page = page.strip()
        if page:
            docs.append(Document(page_content=page, metadata={"source": source, "page": page_num}))

    print(f"✅ Total documents created: {len(docs)}")
    # print("📝 Sample documents:", docs[:2])
    return docs

import re
from mistral_ocr import ocr_from_pdf
from langchain.schema import Document
from advanced_preprocessing import extract_answers , mcq_answering , fix_serial_numbers

def remove_jpeg_images(markdown_text):

    # Remove all ![...](...jpeg) or ...JPEG with case-insensitivity
    cleaned = re.sub(r'!\[.*?\]\([^)]+\.jpe?g\)', '', markdown_text, flags=re.IGNORECASE)

    return cleaned.strip()

def clean_markdown_tags(text):
    # Remove LaTeX expressions like $\checkmark$
    text = re.sub(r'\$\\[a-zA-Z]+\$', ' ', text)

    # Remove markdown table alignment tags (like | :--: | etc.)
    text = re.sub(r'\|\s*:?-+:?\s*\|?', ' ', text)

    # Remove other markdown symbols, but keep parentheses ()
    text = re.sub(r'[`\*#_\-\[\]><~]', ' ', text)  # Removed () from the character set

    # Replace <br> tags with newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Step ২: Remove extra spaces
    lines = text.splitlines()
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines if line.strip()]

    # Step ৩: Return the cleaned text
    return '\n'.join(cleaned_lines)

def clean_irrelevant_lines(text):
    # Define patterns to remove based on common keywords
    patterns = [
        r'১০ MINUTE SCHOOL',
        r'HSC\s*[০-৯0-9]{1,2}',             
        r'অনলাইন\s*ব্যাচ',
        r'বাংলা\s*-\s*ইংরেজি\s*-\s*আইসিটি',
        r'বাংলা\s*<br>\s*(১ম|২য়|দ্বিতীয়|দ্বিতীয়)\s*পত্র',
        r'(১ম|২য়|দ্বিতীয়|দ্বিতীয়)\s*পত্র',
        r'অনলাইন\s*ব্যাচ\s*সম্পর্কিত\s*যেকোনো\s*জিজ্ঞাসায়',
    ]

    combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)

    # Remove any matching line
    cleaned_lines = [
        line for line in text.splitlines()
        if not combined_pattern.search(line.strip())
    ]

    return '\n'.join(cleaned_lines).strip()


def text_extractor(pdf_path, api_key, language):
    # Step 1: OCR the PDF using your selected model and language
    original_text = ocr_from_pdf(pdf_path, api_key, language)

    # Step 2: Remove unwanted lines like headers, footers, instructions
    basic_cleaned_text = clean_irrelevant_lines(original_text)

    # Step 3: Remove any leftover image tags or placeholders like <jpeg> or ![](image.jpg)
    cleaned_image_tags = remove_jpeg_images(basic_cleaned_text)

    # Step 4: Remove all markdown tags including ###, ##, | :--: |, and replace them with space
    cleaned_md_tag = clean_markdown_tags(cleaned_image_tags)

    # Step 5: Extract MCQs and answers from the cleaned text block (e.g., using regex)
    advanced_prep_text = extract_answers(cleaned_md_tag)

    # Step 6: Fix serial number inconsistencies like missing or duplicate numbering
    fix_sr_text = fix_serial_numbers(advanced_prep_text)

    # Step 7: Apply MCQ answer inference logic (e.g., answer: গ )
    final_correction_text = mcq_answering(fix_sr_text)

    return final_correction_text


def markdown_page_split(text, source):

    docs = []
    pages = text.split('Page End')

    for page_num, page in enumerate(pages, start=1):
        page = page.strip()
        if page:
            docs.append(Document(page_content=page, metadata={"source": source, "page": page_num}))

    print(f"✅ Total documents created: {len(docs)}")
    # print("📝 Sample documents:", docs[:2])
    return docs

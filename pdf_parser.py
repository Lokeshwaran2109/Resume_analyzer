import pdfplumber

def extract_text(file) -> str:
    """
    Extract text from uploaded PDF file (Streamlit or file path safe).
    """

    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # Safety check
        if not text.strip():
            return "No text found in PDF."

        if len(text.strip()) < 50:
            print("⚠ Warning: Very little text extracted from PDF")

        return text.strip()

    except Exception as e:
        return f"PDF reading error: {str(e)}"

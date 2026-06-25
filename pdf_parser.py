import pdfplumber

def extract_text(file):

    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        return f"Error reading PDF: {e}"

    return text.lower()

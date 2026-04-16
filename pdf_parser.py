import pdfplumber

def extract_text(file_path):
    text = "" 
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text+=page_text + "\n"

        if len(text.strip())<50:
            print("very little text extraction")
        
        return text
    except Exception as e:
        print("error reading pdf",e)
        return None


        
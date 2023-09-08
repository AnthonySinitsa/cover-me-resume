import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file path.
    
    Args:
    - pdf_path (str): Path to the PDF file.
    
    Returns:
    - str: Extracted text from the PDF.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extractText()
    except Exception as e:  # Catching generic exception for PyPDF2 errors
        raise ValueError(f"An error occurred while reading the PDF: {str(e)}")
    
    if not text:
        raise ValueError("The PDF doesn't seem to contain any text.")
    
    return text

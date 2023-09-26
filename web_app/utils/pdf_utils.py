from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_pdf(pdf_content):
  """
  Extract text from a PDF content.

  Parameters:
  - pdf_content (bytes): The content of the PDF file.

  Returns:
  - str: The extracted text from the PDF.
  """
  try:
    pdf_file = BytesIO(pdf_content)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
      text += page.extract_text()

    # Check if the extracted text is meaningful
    if not text or len(text.strip()) < 50:
      raise ValueError("The extracted text from the PDF is either empty or too short.")

    return text

  except Exception as e:
    raise ValueError(f"An error occurred while reading the PDF: {str(e)}")


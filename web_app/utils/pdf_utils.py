from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
  """
  Extract text from a PDF file.

  Parameters:
  - pdf_path (str): The path to the PDF file.

  Returns:
  - str: The extracted text from the PDF.
  """
  try:
    with open(pdf_path, 'rb') as file:
      reader = PdfReader(file)
      text = ""
      for page in reader.pages:
        text += page.extract_text()

      # Check if the extracted text is meaningful
      if not text or len(text.strip()) < 50:
        raise ValueError("The extracted text from the PDF is either empty or too short.")

      return text

  except Exception as e:
    raise ValueError(f"An error occurred while reading the PDF: {str(e)}")

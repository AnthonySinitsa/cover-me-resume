import PyPDF2

def extract_text_from_pdf(file_path):
  try:
      with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
          text += reader.getPage(page_num).extractText()
        
        # Check if the extracted text is too short, which might indicate an image-only PDF.
        if len(text) < 50:  # You can adjust this threshold as needed.
          raise ValueError("The uploaded PDF seems to be image-based or contains very little text.")
        
        return text

  except PyPDF2.utils.PdfReadError:
    raise ValueError("The uploaded file appears to be a corrupted or invalid PDF.")

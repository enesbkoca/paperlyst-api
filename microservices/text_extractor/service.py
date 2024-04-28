import os
import fitz # PyMuPDF

def extract_abstract(file_path, start_texts=["ABSTRACT, Abstract"], end_texts=["INTRODUCTION", "Introduction"]):
    """
    Extracts the abstract from a PDF file.

    Args:
        file_path (str): The path to the PDF file.
        start_texts (list): A list of possible start texts.
        end_texts (list): A list of possible end texts.

    Returns:
        str: The abstract of the PDF file as a string.

    Raises:
        FileNotFoundError: If the file_path does not correspond to an existing file.
        Exception: If the file_path does not correspond to a PDF file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file found at {file_path}")

    if not file_path.endswith('.pdf'):
        raise Exception(f"File {file_path} is not a PDF")

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    start_positions = [text.find(start_text) for start_text in start_texts if text.find(start_text) != -1]
    start = min(start_positions) if start_positions else 0
    end_positions = [text.find(end_text, start) for end_text in end_texts if text.find(end_text, start) != -1]
    end = min(end_positions) if end_positions else len(text)
    abstract = text[start:end].strip()
    return abstract


class Microservice1Service:
    def process_data(self, file_path):

        # Extract abstract from PDF
        abstract = extract_abstract(file_path)
        return abstract

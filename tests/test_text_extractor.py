import unittest
import os
from microservices.text_extractor.test import extract_abstract

class TestExtractAbstract(unittest.TestCase):
    def setUp(self):
        self.start_texts = ["Abstract", "Abstract.", "Abstract:", "Abstract -", "ABSTRACT", "Abstract\n", "Abstract\n\n", "Abstract\n\n\n", "Abstract\n\n\n\n"]
        self.end_texts = ["Introduction", "1 Introduction", "1   Introduction", "1. Introduction"]

    def test_extract_abstract(self):
        """
        Check if the extracted abstract is correct.
        """

        self.file_path = "../../tests/PDFs/abstract.pdf"
        abstract = extract_abstract(self.file_path, self.start_texts, self.end_texts)
        
        expected_abstract = "This is a simple abstract."
        self.assertEqual(abstract, expected_abstract)

    def test_non_existent_file_path(self):
        """
        Check if the function raises a FileNotFoundError when the file path does not exist.
        """

        self.file_path = "../../tests/PDFs/none_existent.pdf"
        with self.assertRaises(FileNotFoundError):
            _ = extract_abstract(self.file_path, self.start_texts, self.end_texts)

    def test_non_pdf_file(self):
        """
        Check if the function raises an Exception when the file path does not correspond to a PDF file.
        """

        self.file_path = "../../tests/PDFs/not_a_pdf.png"
        with self.assertRaises(Exception): 
            _ = extract_abstract(self.file_path, self.start_texts, self.end_texts)

    def test_pdf_without_abstract(self):
        """
        Check if the function returns an empty string when the PDF file does not contain an abstract.
        """

        self.file_path = "../../tests/PDFs/no_abstract.pdf"
        abstract = extract_abstract(self.file_path, self.start_texts, self.end_texts)
        self.assertEqual(abstract, "")
    
    def test_pdf_with_no_end_text(self):
        """
        Check if the function returns the abstract until the end of the PDF when there is no end text.
        """

        self.file_path = "../../tests/PDFs/no_end_texts.pdf"
        abstract = extract_abstract(self.file_path, self.start_texts, self.end_texts)

        expected_abstract = "This is a simple abstract.\nThis is the end of the abstract."
        self.assertEqual(abstract, expected_abstract)

if __name__ == "__main__":
    unittest.main()
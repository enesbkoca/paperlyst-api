import unittest
import torch
from microservices.vectorization.service import Microservice1Service

class TestMicroservice1Service(unittest.TestCase):
    def setUp(self):
        self.service = Microservice1Service(model_name="bert-base-uncased")

    def test_single_sentence(self):
        sentence = "This is a test sentence."
        embeddings = self.service.process_data(sentence)
        self.assertEqual(embeddings.shape, (1, 768))

    def test_multiple_sentences(self):
        sentences = ["This is a test sentence.", "This is another test sentence."]
        embeddings = self.service.process_data(sentences)
        self.assertEqual(embeddings.shape, (len(sentences), 768))

    def test_empty_input(self):
        sentences = ""
        embeddings = self.service.process_data(sentences)
        self.assertEqual(embeddings.shape, (1, 768))

if __name__ == '__main__':
    unittest.main()
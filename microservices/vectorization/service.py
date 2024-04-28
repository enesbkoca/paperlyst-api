from transformers import AutoTokenizer, AutoModel
import torch

# BERT has 0.25 secs latency without chromadb wrapper
# BERT has 0.70 secs latency with chromadb wrapper
# MiniLM has 0.35 secs latency with chromadb wrapper
# All in the second run
# chromadb wrapper takes 9.5 secs in the first run
# the first run without rapper was faster but can't remember the exact time
# Meta-Llama had time-out :)

class Microservice1Service:
    def __init__(self, model_name):

        # Load pre-trained model and tokenizer
        self.model_name = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def process_data(self, data):
        
        # Tokenize sentences
        inputs = self.tokenizer(data, return_tensors='pt', padding=True, truncation=True)

        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)

        # The last hidden-state is the first element of the output tuple
        last_hidden_states = outputs.last_hidden_state

        # To get sentence embeddings, you can average the token embeddings for each sentence
        sentence_embeddings = last_hidden_states.mean(dim=1)
        # sentence_embeddings = sentence_embeddings.tolist()
        return sentence_embeddings
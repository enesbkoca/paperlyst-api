from chromadb import Documents, EmbeddingFunction, Embeddings
from transformers import BertModel, BertTokenizer
import torch
import os
from pathlib import Path

def download_and_save_bert_model(model_name: str, save_directory: Path):
    """
    Download and save the BERT model and the tokenizer locally.
    
    Parameters:
            model_name (str): The name of the BERT model to download.
            save_directory (str): The directory to save the downloaded tokenizer and model.
            
    Returns:
            tokenizer (BertTokenizer): The downloaded tokenizer.
            model (BertModel): The downloaded BERT model.
    """
    try:
        # Download model and tokenizer
        model = BertModel.from_pretrained(model_name)
        tokenizer = BertTokenizer.from_pretrained(model_name)

        # Save the downloaded model and tokenizer
        model.save_pretrained(save_directory)
        tokenizer.save_pretrained(save_directory)
    except Exception as e:
        print(f"Error downloading and saving the model: {e}")
        return None, None

    return tokenizer, model

def load_bert_model(save_directory: Path):
    """
    Load the saved BERT model and tokenizer from the local directory.
    
    Parameters:
            save_directory (str): The directory containing the saved model and tokenizer.
    
    Returns:
            tokenizer (BertTokenizer): The loaded tokenizer.
            model (BertModel): The loaded BERT model.
    """
    try:
        # Load the saved tokenizer and model
        tokenizer = BertTokenizer.from_pretrained(save_directory)
        model = BertModel.from_pretrained(save_directory)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None, None

    return tokenizer, model

# Set the name of the model and the directory to save the model and tokenizer
model_name = 'bert-base-uncased'
save_directory = Path('../data/bert_model')

# Check if the model and tokenizer files exist
if not os.path.exists(os.path.join(save_directory, 'pytorch_model.bin')) or \
    not os.path.exists(os.path.join(save_directory, 'vocab.txt')):
    download_and_save_bert_model(model_name=model_name, save_directory=save_directory)

# Load pre-trained tokenizer and model
tokenizer, model = load_bert_model(save_directory=save_directory)

class BERTEmbeddingFunction(EmbeddingFunction[Documents]):
    def __call__(self, input: Documents) -> Embeddings:
        
        # Add your custom implementation here
        pass

        """
        Custom embedding function for chroma.
        It assumes that the tokenizer and model are already loaded.

        Parameters:
                Documents (stringt): The input text for which the embeddings need to be created.

        Returns:
                embeddings (numpy.ndarray) (768x1): The BERT embeddings for the input text.
        """

        assert len(input) == 1, "The input should be a single string."

        # Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for each model.
        input_ids = tokenizer.encode(input[0], add_special_tokens=True) 
        input_ids = torch.tensor([input_ids])  # Add batch dimension

        with torch.no_grad():
            last_hidden_states = model(input_ids)[0]  # Models outputs are now tuples

        # Take the embeddings from the first token (CLS), which can be used as sentence embeddings
        sentence_embedding = last_hidden_states[0][0]

        return [sentence_embedding.numpy()]
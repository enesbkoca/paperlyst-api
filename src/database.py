import chromadb


class Database:

    def __init__(self):
        self.client = chromadb.Client()

    def create_collections(self):
        self.collection = self.client.create_collection(
            name="abstract",
            embedding_function=emb_fn
        )
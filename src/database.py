import chromadb


class Database:

    def __init__(self):
        # change Client to PersistentClient when want to keep database fixed
        self.client = chromadb.Client()
        self.collection = None
        self.embedding_function = None

    def create_collections(self):
        self.collection = self.client.create_collection(
            name="abstract",
            embedding_function=self.embedding_function
        )

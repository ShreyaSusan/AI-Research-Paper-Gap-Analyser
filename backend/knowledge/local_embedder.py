from sentence_transformers import SentenceTransformer


class LocalEmbedder:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # MiniLM embedding dimensions
        self.dimensions = 384

    def get_embedding(self, text: str):

        embedding = self.model.encode(text)

        return embedding.tolist()
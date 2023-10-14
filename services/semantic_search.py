import os
import uuid
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class SemanticSearch:
    def __init__(self, 
                 host: str = None, 
                 port: int = None, 
                 collection: str = 'documents',
                 embedding_model: str = 'all-mpnet-base-v2',
                 similarity: str = 'cosine'):
        
        host = host if host else os.environ.get('CHROMADB_HOST')
        port = port if port else os.environ.get('CHROMADB_PORT')
        settings = Settings(allow_reset=True, anonymized_telemetry=False)
        
        if host and port:
            client = chromadb.HttpClient(host=host, port=port, settings=settings)
        else:
            client = chromadb.Client()

        while True:
            try:
                self.collection = client.get_or_create_collection(name=collection, metadata={"hnsw:space": similarity})
                break
            except Exception as e:
                print(e)
                continue

        self.embedding_model = SentenceTransformer(embedding_model)

    def add(self, documents: list[str]):
        embeddings = [self.embedding_model.encode(doc).tolist() for doc in documents]
        ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        self.collection.add(documents=documents, embeddings=embeddings, ids=ids)

    def query(self, query_text: str, n_results: int = 1):
        query_embedding = self.embedding_model.encode(query_text).tolist()
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)

        
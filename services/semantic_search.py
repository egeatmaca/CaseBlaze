import os
import uuid
import chromadb
from chromadb.config import Settings
import time
from services.transformer_factory import TransformerFactory

class SemanticSearch:
    
    def __init__(self, 
                 host: str = None, 
                 port: int = None, 
                 collection: str = 'documents',
                 model_name: str = 'bert-base-german-cased',
                 similarity: str = 'cosine'):
        
        self.model = TransformerFactory.get_model('sentence_transformer', model_name)
        
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
                time.sleep(5)
                continue

    def add(self, documents: list[str], metadatas: list[str] = [], ids: list[str] = None):
        embeddings = [self.model.encode(doc).tolist() for doc in documents]
        ids = [str(uuid.uuid4()) for _ in range(len(documents))] if not ids else ids
        self.collection.add(documents=documents, 
                            embeddings=embeddings, 
                            metadatas=metadatas,
                            ids=ids)

    def query(self, query_text: str, n_results: int = 1):
        query_embedding = self.model.encode(query_text).tolist()
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)

        
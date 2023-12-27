import nltk
from sentence_transformers import util
import numpy as np
from services.transformer_factory import TransformerFactory
from gpt4all import GPT4All
from sklearn_extra.cluster import KMedoids

nltk.download('punkt')


class ExtractiveSummarizer:
    def __init__(self, model_name='bert-base-german-cased') -> None:
        self.model = TransformerFactory.get_model('sentence_transformer', model_name)

    def pagerank_scores(self, graph_matrix, damping_factor=0.85, max_iterations=100, tol=1e-6):
        row_sums = graph_matrix.sum(axis=1, keepdims=True)
        transition_matrix = graph_matrix / row_sums
        num_nodes = len(graph_matrix)
        pagerank_scores = np.ones(num_nodes) / num_nodes

        for _ in range(max_iterations):
            new_pagerank = (1 - damping_factor) / num_nodes + damping_factor * np.dot(transition_matrix.T, pagerank_scores)

            if np.linalg.norm(new_pagerank - pagerank_scores) < tol:
                return new_pagerank

            pagerank_scores = new_pagerank

        return pagerank_scores
    
    def cluster_sentences(self, embeddings, n_clusters=10):
        kmedoids = KMedoids(n_clusters=n_clusters, metric='cosine', init='k-medoids++')
        kmedoids.fit(embeddings)
        clusters = kmedoids.predict(embeddings)
        cluster_centers = kmedoids.cluster_centers_
        return clusters, cluster_centers

    def summarize_with_pagerank(self, document, n_sentences=10):
        # Split the document into sentences
        sentences = nltk.sent_tokenize(document)

        # Update n_sentences if greater than the number of sentences
        n_sentences = np.min([n_sentences, len(sentences)])

        # Compute the sentence embeddings
        embeddings = self.model.encode(sentences, convert_to_tensor=True)

        # Compute the pair-wise cosine similarities
        cosine_similarities = util.cos_sim(embeddings, embeddings).numpy()

        # Compute the centrality for each sentence using pagerank
        pagerank_scores = self.pagerank_scores(cosine_similarities)

        # Get the most central indices
        most_central_sentence_indices = np.argsort(-pagerank_scores)[0:n_sentences]

        # Sort most central indices chronologically
        most_central_sentence_indices = np.sort(most_central_sentence_indices)

        # Print the 5 sentences with the highest scores
        most_central_sentences = []
        for idx in most_central_sentence_indices:
            most_central_sentences.append(sentences[idx].strip())
        
        summary = ' '.join(most_central_sentences)

        return summary
    
    def summarize_with_clustering(self, document, n_sentences=10):
        # Split the document into sentences
        sentences = nltk.sent_tokenize(document)

        # Update n_sentences if greater than the number of sentences
        n_sentences = np.min([n_sentences, len(sentences)])

        # Compute the sentence embeddings
        embeddings = self.model.encode(sentences, convert_to_tensor=True)

        # Compute clusters
        clusters, cluster_centers = self.cluster_sentences(embeddings, n_clusters=n_sentences)

        # Get the most central indices
        most_central_sentence_indices = []
        for cluster_idx in range(n_sentences):
            cluster_indices = np.where(clusters == cluster_idx)[0]
            cluster_embeddings = embeddings[cluster_indices].numpy().astype(np.float32)
            cluster_center = cluster_centers[cluster_idx].reshape(1, -1).astype(np.float32)
            cluster_cosine_similarities = util.cos_sim(cluster_embeddings, cluster_center).numpy()
            cluster_most_central_idx = cluster_indices[np.argmax(cluster_cosine_similarities)]
            most_central_sentence_indices.append(cluster_most_central_idx)

        # Sort most central indices chronologically
        most_central_sentence_indices = np.sort(most_central_sentence_indices)

        # Concatenate the most central sentences
        most_central_sentences = []
        for idx in most_central_sentence_indices:
            most_central_sentences.append(sentences[idx].strip())

        summary = ' '.join(most_central_sentences)

        return summary
    
    def summarize(self, document, n_sentences=10, method='clustering'):
        if method == 'pagerank':
            return self.summarize_with_pagerank(document, n_sentences)
        elif method == 'clustering':
            return self.summarize_with_clustering(document, n_sentences)
        else:
            raise ValueError('Invalid summarization method')


class AbstractiveSummarizer:
    def __init__(self, model_name='mistral-7b-instruct-v0.1.Q4_0') -> None:
        self.model_name = model_name
        self.model = GPT4All(model_name=model_name, n_threads=4)

    def _summarize(self, text, max_tokens=100):
        return self.model.generate('Zusammenfassen: ' + text, max_tokens=max_tokens)

    def chunk_text(self, text, chunk_size=500):
        chunks = []

        current_chunk = ''
        for i, word in enumerate(nltk.wordpunct_tokenize(text)):
            current_chunk += word + ' '
            if (i + 1) % chunk_size == 0:
                current_chunk = current_chunk.strip()
                chunks.append(current_chunk)
                current_chunk = ''

        if current_chunk != '':
            current_chunk = current_chunk.strip()
            chunks.append(current_chunk)

        print('Chunks:', chunks)

        return chunks
    
    def summarize(self, text, chunk_size=500, max_tokens=50):
        chunks = self.chunk_text(text, chunk_size=chunk_size)
        summary = ''
        for chunk in chunks:
            summary += self._summarize(chunk, max_tokens=max_tokens) + ' '
        return summary
    

if __name__ == '__main__':
    # Test extractive summarizer
    summarizer = AbstractiveSummarizer()
    
    # Read a document
    with open('./documents/I ZB 108-22.txt', 'r') as f:
        document = f.read()
    
    summary = summarizer.summarize_long_text(document)
    print(summary)



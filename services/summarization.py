import nltk
from sentence_transformers import SentenceTransformer, util
import numpy as np

nltk.download('punkt')


class ExtractiveSummarizer:

    def __init__(self, model_name='T-Systems-onsite/cross-en-de-roberta-sentence-transformer') -> None:
        self.model = SentenceTransformer(model_name)

    def pagerank_scores(self, graph_matrix, damping_factor=0.85, max_iterations=100, tol=1e-6):
        row_sums = graph_matrix.sum(axis=1, keepdims=True)
        transition_matrix = graph_matrix / row_sums
        num_nodes = len(graph_matrix)
        pagerank_scores = np.ones(num_nodes) / num_nodes

        for _ in range(max_iterations):
            new_pagerank = (1 - damping_factor) / num_nodes + damping_factor * np.dot(transition_matrix, pagerank_scores)

            if np.linalg.norm(new_pagerank - pagerank_scores) < tol:
                return new_pagerank

            pagerank_scores = new_pagerank

        return pagerank_scores

    def summarize(self, document, n_sentences=5):
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
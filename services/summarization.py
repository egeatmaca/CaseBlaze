import nltk
from sentence_transformers import util
import numpy as np
from services.transformer_factory import TransformerFactory

nltk.download('punkt')


class ExtractiveSummarizer:
    def __init__(self, model_name='T-Systems-onsite/cross-en-de-roberta-sentence-transformer') -> None:
        self.model = TransformerFactory.get_model('sentence_transformer', model_name)

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

    def summarize(self, document, n_sentences=10):
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


class AbstractiveSummarizer:
    def __init__(self, 
                 factory_func_name='bart_for_conditional_generation', 
                 model_name='Shahm/bart-german') -> None:
        self.model = TransformerFactory.get_model(factory_func_name, model_name)
        self.tokenizer = TransformerFactory.get_tokenizer(model_name)

    def chunk_text(self, text, max_input_length=200):
        words = text.split(' ')
        chunks = []
        chunk_start = 0
        chunk_end = max_input_length
        while chunk_start < len(words):
            chunk_words = words[chunk_start:chunk_end]
            chunk = ' '.join(chunk_words)
            chunks.append(chunk)
            chunk_start = chunk_end
            chunk_end += max_input_length
        return chunks

    def summarize_chunk(self, chunk, max_output_length=50):
        # Add summary prefix to text
        chunk = 'zusammenfassen: ' + chunk

        # Get input tokens
        inputs = self.tokenizer([chunk], return_tensors="pt")

        # Generate text using tokens
        outputs = self.model.generate(inputs['input_ids'], max_length=max_output_length)

        # Decode tokens
        summary = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        
        return summary[0]

    def summarize(self, text, max_input_length=300, max_output_length=75):
        chunks = self.chunk_text(text=text, max_input_length=max_input_length)
        chunk_summaries = [self.summarize_chunk(chunk, max_output_length=max_output_length)
                           for chunk in chunks]
        summary = ' '.join(chunk_summaries)
        return summary

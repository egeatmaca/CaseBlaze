import os
from services.semantic_search import SemanticSearch
from services.summarization import ExtractiveSummarizer


if __name__ == '__main__':
    search_query = 'Landlord is asking for an extremely high rent increase.'

    semantic_search = SemanticSearch()
    for doc_name in os.listdir('documents'):
        doc_path = os.path.join('documents', doc_name)
        doc_id = doc_name.replace('.txt', '')
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as doc:
            semantic_search.add([doc.read()], [doc_id])       
    result = semantic_search.query(search_query)['documents'][0][0]
    print('\nResult:', result)

    summarizer = ExtractiveSummarizer()
    summary = summarizer.summarize(result, n_sentences=10)
    print('\nSummary:', summary)
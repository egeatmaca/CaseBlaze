import os
from services.scraping import CaseScraper
from services.semantic_search import SemanticSearch
from services.summarization import ExtractiveSummarizer


def inject_cases():
    scraper = CaseScraper()
    scraper.scrape_cases()
    
    semantic_search = SemanticSearch()
    summarizer = ExtractiveSummarizer()
    for doc_name in os.listdir(scraper.documents_dir):
        doc_path = os.path.join(scraper.documents_dir, doc_name)
        doc_id = doc_name.replace('.txt', '').strip()
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as doc:
            document = doc.read()
            summary = summarizer.summarize(document)
            semantic_search.add(
                documents = [document], 
                metadatas = [{'summary': summary}],
                ids = [doc_id]
            )
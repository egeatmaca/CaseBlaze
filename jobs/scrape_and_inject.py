import os
from services.scraping import CaseScraper
from services.semantic_search import SemanticSearch


def scrape_and_inject():
    scraper = CaseScraper()
    scraper.scrape_cases()
    
    semantic_search = SemanticSearch()
    for doc_name in os.listdir(scraper.documents_dir):
        doc_path = os.path.join(scraper.documents_dir, doc_name)
        doc_id = doc_name.replace('.txt', '').strip()
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as doc:
            semantic_search.add([doc.read()], [doc_id])
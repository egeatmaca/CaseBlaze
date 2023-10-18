from services.semantic_search import SemanticSearch
from services.summarization import ExtractiveSummarizer
from jobs.scrape_and_inject import scrape_and_inject


if __name__ == '__main__':
    scrape_and_inject()

    search_query = 'Landlord is asking for an extremely high rent increase.'

    semantic_search = SemanticSearch()
    result = semantic_search.query(search_query)['documents'][0][0]
    print('\nResult:', result)

    summarizer = ExtractiveSummarizer()
    summary = summarizer.summarize(result, n_sentences=10)
    print('\nSummary:', summary)
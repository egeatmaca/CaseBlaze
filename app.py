from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from services.semantic_search import SemanticSearch
from services.summarization import ExtractiveSummarizer


app = FastAPI()
templates = Jinja2Templates(directory='templates')
static_files = StaticFiles(directory='static')
app.mount('/static', static_files, name='static')

semantic_search = SemanticSearch()
summarizer = ExtractiveSummarizer()

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get('/query')
def query(request: Request):
    query = request.query_params.get('query')
    n_results = request.query_params.get('n_results', 5)

    if not query:
        return Response(status_code=400, content="'query' parameter should be provided!")
    
    try:
        n_results = int(n_results)
    except ValueError:
        return Response(status_code=400, content="'n_results' parameter should be an integer!")
    
    search_results = semantic_search.query(query, n_results)
    documents = search_results['documents'][0]
    summaries = [metadata['summary'] for metadata in search_results['metadatas'][0]]
    
    return {
        'documents': documents,
        'summaries': summaries
    }

def run_app():
    uvicorn.run(app, host='0.0.0.0', port=3000)
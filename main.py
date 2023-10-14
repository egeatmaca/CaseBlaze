from services.semantic_search import SemanticSearch


if __name__ == '__main__':
    s = SemanticSearch()
    s.add(['This is my first document about tigers.', 
           'This is another document containing information about pets you can keep at home. Some good example would be cats or dogs.',
           'Germany is in Europe.'])
    results = s.query('Can you keep dogs at home?')
    print('results:', results)
import io
import os
import uuid
from PyPDF2 import PdfReader
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

class CaseScraper:
    base_url = 'https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/'
    list_url = base_url + 'list.py?Gericht=bgh&Art=en&Datum=Aktuell&Sort=12288'

    def __init__(self, documents_dir='documents') -> None:
        self.webdriver = Firefox()
        self.documents_dir = documents_dir

    def get_document_links(self, search_query, search_pages=10):
        self.webdriver.get(self.list_url)
        search_form_fields = self.webdriver.find_elements(By.CSS_SELECTOR, 'input.SuchFormFeld')
        search_form_button = self.webdriver.find_element(By.CSS_SELECTOR, 'input.SuchFormButton')
        
        if len(search_form_fields) < 3:
            raise Exception('Invalid search form!')
        
        search_form_input = search_form_fields[2]
        search_form_input.send_keys(search_query)
        search_form_button.click()
        
        for _ in range(search_pages):
            document_link_elements = self.webdriver.find_elements(By.CSS_SELECTOR, 'a.doklink')
            document_links = []
            for link in document_link_elements:
                document_links.append(link.get_attribute('href'))

            next_page_button = self.webdriver.find_element(By.CSS_SELECTOR, 'td.rechts')
            if next_page_button:
                next_page_button.click()
            else:
                break

        return document_links
    
    def download_document(self, document_link):
        # Get pdf link
        self.webdriver.get(document_link)
        pdf_embed = self.webdriver.find_element(By.CSS_SELECTOR, 'iframe')
        pdf_link = pdf_embed.get_attribute('src')
        
        # Download pdf
        response = requests.get(pdf_link)
        pdf_io = io.BytesIO(response.content)

        # Extract text from pdf
        pdf = PdfReader(pdf_io)
        document = ''
        for page in pdf.pages:
            document += page.extract_text()

        # Save extracted text
        document_path = os.path.join(self.documents_dir, str(uuid.uuid4())+'.txt')
        with open(document_path, 'w') as document_txt:
            document_txt.write(document)

    def scrape_cases(self, search_query='Mietrecht', search_pages=10):
        os.makedirs(self.documents_dir, exist_ok=True)
        document_links = self.get_document_links(search_query, search_pages)
        for doc_link in document_links:
            self.download_document(doc_link)


if __name__ == '__main__':
    scraper = CaseScraper()
    scraper.scrape_cases()
import io
import os
from PyPDF2 import PdfReader
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class CaseScraper:
    base_url = 'https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/'
    list_url = base_url + 'list.py?Gericht=bgh&Art=en&Datum=Aktuell&Sort=12288'

    def __init__(self, documents_dir='documents') -> None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(GeckoDriverManager().install())
        self.webdriver = Firefox(options=options, service=service)
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
        
        document_links = {}
        for _ in range(search_pages):
            document_link_elements = self.webdriver.find_elements(By.CSS_SELECTOR, 'a.doklink')
            for link in document_link_elements:
                document_links[link.get_attribute('innerText')] = link.get_attribute('href')

            next_page_image = self.webdriver.find_element(By.CSS_SELECTOR, 'img[src="/rechtsprechung/bgh/pics/weiter.gif"]')
            next_page_link = next_page_image.find_element(By.XPATH, '..')
            if next_page_link and next_page_link.tag_name == 'a':
                next_page_link.click()
            else:
                break

        return document_links
    
    def save_document(self, document_name, document_link):
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

        # Merge line breaks
        document = document.replace('-\n', '')

        # Save extracted text
        document_name = document_name.replace('/', '-')
        document_path = os.path.join(self.documents_dir, document_name+'.txt')
        with open(document_path, 'w', encoding='utf-8') as document_txt:
            document_txt.write(document)

    def scrape_cases(self, search_query='Mietrecht', search_pages=10):
        os.makedirs(self.documents_dir, exist_ok=True)
        
        document_links = self.get_document_links(search_query, search_pages)
        for doc_name, doc_link in document_links.items():
            self.save_document(doc_name, doc_link)

        self.webdriver.close()


if __name__ == '__main__':
    scraper = CaseScraper()
    scraper.scrape_cases()
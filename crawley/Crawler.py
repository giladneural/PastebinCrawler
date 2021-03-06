import requests
import urllib
import logging
from bs4 import BeautifulSoup
from crawley.DBHandler import DBHandler
from crawley.PasteHandler import PasteHandler

logger = logging.getLogger(__name__)


class Crawler:
    """
    This class represents a fully functional crawler.
    It implements the flow of fetching the data,
    crawl to each paste and insert it to the database.
    """
    def __init__(self, url):
        self._url = url

    @staticmethod
    def fetch_page(url: str):
        code = requests.get(url)
        plain = code.text
        code.raise_for_status()
        return BeautifulSoup(plain, 'html.parser')

    def crawl(self):
        soup = self.fetch_page(self._url)
        menu = soup.find('div', {'id': 'menu_2'})

        for link in menu.findAll('a'):
            paste_link = link.get('href')
            crawl_link = urllib.parse.urljoin(self._url, paste_link)
            self._crawl_to_paste(crawl_link)

    def _crawl_to_paste(self, crawl_link: str):
        print('crawling to: {}'.format(crawl_link))
        logger.info('crawling to: {}'.format(crawl_link))
        soup = self.fetch_page(crawl_link)
        paste = PasteHandler.extract_data_scheme(soup)
        db = DBHandler()
        db.insert(paste)

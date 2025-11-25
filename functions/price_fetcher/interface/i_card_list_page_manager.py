from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class ICardListPageManager(ABC):
    @abstractmethod
    def fetch_card_list_pages(self, soup: BeautifulSoup):
        pass

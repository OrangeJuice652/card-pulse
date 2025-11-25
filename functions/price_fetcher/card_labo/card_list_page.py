from bs4 import BeautifulSoup
from interface import ICardListPage
from card_labo import CardElement


class CardListPage(ICardListPage):
    @classmethod
    def from_html_str(cls, card_list_page_html: str):
        return cls(BeautifulSoup(card_list_page_html, 'lxml'))

    def __init__(self, card_list_page_soup: BeautifulSoup):
        self._card_list_page_soup = card_list_page_soup

    def card_elements(self):
        result = [
            CardElement(card_element_dom)
            for card_element_dom in self._card_list_page_soup.find_all(
                class_='item_data'
            )
        ]
        return result

    @property
    def pager_urls(self):
        result = []
        for pager_btn in self._card_list_page_soup.find_all(class_='pager_btn', href=True):
            if pager_btn.attrs['href'] not in result:
                # TODO: ドメインを頭につける
                result.append(
                    pager_btn.attrs['href']
                )
        return result

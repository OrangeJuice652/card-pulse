from abc import ABC, abstractmethod


class ICardElement(ABC):
    @abstractmethod
    def __init__(self, card_element_dom):
        pass

    @property
    @abstractmethod
    def card_id(self):
        pass

    @property
    @abstractmethod
    def card_name(self):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @property
    @abstractmethod
    def rarity(self):
        pass

    @property
    @abstractmethod
    def card_detail_page_url(self):
        pass

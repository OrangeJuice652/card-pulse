from abc import ABC, abstractmethod
from interface import ICardElement
from typing import List


class ICardListPage(ABC):
    @property
    @abstractmethod
    def card_elements() -> List[ICardElement]:
        pass

    @property
    @abstractmethod
    def pager_urls():
        pass

from bs4 import BeautifulSoup
from interface import ICardElement
import re


class CardElement(ICardElement):
    """
    Example
    ------
    self._card_element_domが、受け取るhtmlの例
    <div class="item_data">
        <a href="https://www.c-labo-online.jp/product/350079" class="item_data_link">
            <div class="inner_item_data">

                <div class="list_item_photo">
                    <div class="inner_list_item_photo">
                        <div class="global_photo item_image_box itemph_itemlist_350079 async_image_box loading_photo portrait_item_image_box" data-src="https://www.c-labo-online.jp/data/c-labo/_/70726f647563742f77736b2d2d776535305f3038312e6a70670032343000534f4c44204f55540074006669745f686569676874.jpg" data-alt="" data-class="item_image" data-width="87" data-height="120">
                            <img src="https://www.c-labo-online.jp/res/touch003/img/all/spacer.gif" width="87" style="aspect-ratio: 87 / 120" class="spacer_image item_image" alt="" />
                        </div>
                    </div>
                </div>
                <div class="list_item_data">
                    <p class="item_name">
                        <span class="goods_name">【WS】※プレイ用特価品※海の家の看板娘 紬&amp;静久(箔押し)【PRR】Ksm/WE50-57PRR</span>
                    </p>
                    <p class="common_icon">
                    </p>

                    <div class="item_info">
                        <div class="price">
                            <p class="selling_price">
                                <span class="figure">120<span class="currency_label after_price">円</span></span><span class="tax_label list_tax_label">(税込)</span>
                            </p>
                        </div>
                        <p class="stock soldout">在庫なし</p>
                    </div>
                </div>
            </div>
        </a>
    </div>
    """
    _PATTERN = r"【([\x21-\x7E]+)】.*【([\x21-\x7E]+)】([\x21-\x7E]+)"
    def __init__(self, card_element_dom):
        self._card_element_dom: BeautifulSoup = card_element_dom
        self._card_id = None
        self._card_name = None
        self._price = None
        self._rarity = None
        self._card_detail_page_url = None
        self._card_name_match = re.search(self._PATTERN, self.card_name)

    @property
    def card_id(self) -> str:
        """
        Return Example:
            Ksm/WE50-57PRR
        """
        return self._card_name_match.group(3) if self._card_name_match else ""

    @property
    def card_name(self) -> str:
        """
        Return Example:
            【WS】※プレイ用特価品※海の家の看板娘 紬&静久(箔押し)【PRR】Ksm/WE50-57PRR
        """
        if self._card_name is not None:
            return self._card_name

        name_span = self._card_element_dom.select_one(".goods_name")
        self._card_name = name_span.get_text(strip=True) if name_span else ""
        return self._card_name

    @property
    def price(self) -> int:
        """
        Return Example:
            120
        """
        if self._price is not None:
            return self._price

        figure = self._card_element_dom.select_one(".selling_price .figure")
        if not figure:
            self._price = 0
        else:
            price_text = figure.get_text(strip=True)
            digits = "".join(ch for ch in price_text if ch.isdigit())
            self._price = int(digits) if digits else 0

        return self._price

    @property
    def rarity(self) -> str:
        """
        Return Example:
            PRR
        """
        return self._card_name_match.group(2) if self._card_name_match else ""

    @property
    def card_detail_page_url(self) -> str:
        """
        Return Example:
            https://www.c-labo-online.jp/product/350079
        """
        if self._card_detail_page_url is not None:
            return self._card_detail_page_url

        a_tag = self._card_element_dom.select_one("a.item_data_link")
        self._card_detail_page_url = a_tag["href"] if a_tag and a_tag.get("href") else ""
        return self._card_detail_page_url

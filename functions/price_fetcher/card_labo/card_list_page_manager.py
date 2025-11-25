import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from interface import ICardListPageManager
from card_labo import CardListPage


class CardListPageManager(ICardListPageManager):
    def __init__(self, domain: str = ''):
        self._domain = domain

    async def agenerate_card_list_page(self, pager_urls):
        result = []
        async with aiohttp.ClientSession() as session:
            # すべてのURLに対して非同期リクエストを投げる
            tasks = [
                self._fetch(session, urljoin(self._domain, url))
                for url in pager_urls
            ]
            for coro in asyncio.as_completed(tasks):
                html, url = await coro
                result.append(
                    CardListPage.from_html_str(html)
                )
        return result

    async def _fetch(self, session, url):
        async with session.get(url, timeout=15) as response:
            try:
                response.raise_for_status()
                return await response.text(), url
            except Exception as e:
                return None, url

    def fetch_card_list_pages(self, first_page_html: str):
        # 最初のページのスープを入れる
        card_list_page = CardListPage.from_html_str(first_page_html)
        card_list_pages = [card_list_page]
        card_list_pages.extend(
            asyncio.run(
                self.agenerate_card_list_page(card_list_page.pager_urls)
            )
        )
        return card_list_pages
        

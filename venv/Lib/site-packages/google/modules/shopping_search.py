from __future__ import unicode_literals

from utils import get_html, normalize_query
from bs4 import BeautifulSoup
import re
from unidecode import unidecode


class ShoppingResult:

    """Represents a shopping result."""

    def __init__(self):
        self.name = None
        self.link = None
        self.thumb = None
        self.subtext = None
        self.description = None
        self.compare_url = None
        self.store_count = None
        self.min_price = None

    def __repr__(self):
        return unidecode(self.name)


def shopping(query, pages=1):
    results = []
    for i in range(pages):
        url = _get_shopping_url(query, i)
        html = get_html(url)
        if html:
            j = 0
            soup = BeautifulSoup(html)

            products = soup.findAll("li", "g")
            for prod in products:
                res = ShoppingResult()

                divs = prod.findAll("div")
                for div in divs:
                    match = re.search(
                        "from (?P<count>[0-9]+) stores", div.text.strip())
                    if match:
                        res.store_count = match.group("count")
                        break

                h3 = prod.find("h3", "r")
                if h3:
                    a = h3.find("a")
                    if a:
                        res.compare_url = a["href"]
                    res.name = h3.text.strip()

                psliimg = prod.find("div", "psliimg")
                if psliimg:
                    img = psliimg.find("img")
                    if img:
                        res.thumb = img["src"]

                f = prod.find("div", "f")
                if f:
                    res.subtext = f.text.strip()

                price = prod.find("div", "psliprice")
                if price:
                    res.min_price = price.text.strip()

                results.append(res)
                j = j + 1
    return results


def _get_shopping_url(query, page=0, per_page=10):
    return "http://www.google.com/search?hl=en&q={0}&tbm=shop&start={1}&num={2}".format(normalize_query(query), page * per_page, per_page)

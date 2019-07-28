from __future__ import unicode_literals

from utils import get_html
from bs4 import BeautifulSoup


# PUBLIC
def convert(amount, from_currency, to_currency):
    """Method to convert currency.

    Args:
        amount: numeric amount to convert
        from_currency: currency denomination of the amount to convert
        to_currency: target currency denomination to convert to
    """

    # same currency, no conversion
    if from_currency == to_currency:
        return amount * 1.0

    req_url = _get_currency_req_url(amount,
                                    from_currency, to_currency)
    response = get_html(req_url)
    rate = _parse_currency_response(response, to_currency)

    return rate


def exchange_rate(from_currency, to_currency):
    """Gets the exchange rate of one currency to another.

    Args:
        from_currency: starting currency denomination (1)
        to_currency: target currency denomination to convert to (rate)

    Returns:
        rate / 1 to convert from_currency in to_currency
    """
    return convert(1, from_currency, to_currency)


# PRIVATE
def _get_currency_req_url(amount, from_currency, to_currency):
    return "https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(
        amount, from_currency.replace(" ", "%20"),
        to_currency.replace(" ", "%20"))


def _parse_currency_response(response, to_currency):
    bs = BeautifulSoup(response)
    str_rate = bs.find(id="currency_converter_result").span.get_text()
    rate = float(str_rate.replace(to_currency, "").strip())
    return rate

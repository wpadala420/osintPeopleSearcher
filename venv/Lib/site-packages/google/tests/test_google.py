import unittest
import nose
from google import google
from google import currency, images
from mock import Mock
import os


def load_html_file(path):
    """Call test with a html file of the same name.

    Args:
        path: Relative path where the html file is located."""

    def test_decorator(fn):
        base_path = os.path.join(os.path.dirname(__file__), path)
        file_name = fn.__name__ + ".html"
        file_path = os.path.join(base_path, file_name)

        html_f = open(file_path, "r")

        def test_decorated(self):
            fn(self, html_f)

        return test_decorated
    return test_decorator


class GoogleTest(unittest.TestCase):

    @load_html_file("html_files")
    # @unittest.skip("skip")
    def test_search_images(self, html_f):
        """Test method to search images."""

        class MockBrowser(object):

            """Mock browser to replace selenium driver."""

            def __init__(self, html_f):
                self.page_source = html_f.read().decode('utf8')

            def get(self, url):
                pass

            def quit(self):
                pass

        google.images.get_browser_with_url = \
            Mock(return_value=MockBrowser(html_f))

        res = google.search_images("apple", num_images=10)
        self.assertEqual(len(res), 10)

    @load_html_file("html_files")
    def test_calculator(self, html_f):
        """Test method to calculate in google."""

        # replace method to get html from a test html file
        google.calculator.get_html_from_dynamic_site = \
            Mock(return_value=html_f.read().decode('utf8'))

        calc = google.calculate("157.3kg in grams")
        self.assertEqual(calc.value, 157300)

    @load_html_file("html_files")
    def test_exchange_rate(self, html_f):
        """Test method to get an exchange rate in google."""

        # replace method to get html from a test html file
        google.currency.get_html = \
            Mock(return_value=html_f.read().decode('utf8'))

        usd_to_eur = google.exchange_rate("USD", "EUR")
        self.assertGreater(usd_to_eur, 0.0)

    @load_html_file("html_files")
    def test_convert_currency(self, html_f):
        """Test method to convert currency in google."""

        # replace method to get html from a test html file
        google.currency.get_html = \
            Mock(return_value=html_f.read().decode('utf8'))

        euros = google.convert_currency(5.0, "USD", "EUR")
        self.assertGreater(euros, 0.0)

    @load_html_file("html_files")
    def test_standard_search(self, html_f):
        """Test method to search in google."""

        # replace method to get html from a test html file
        google.standard_search.get_html = \
            Mock(return_value=html_f.read().decode('utf8'))

        search = google.search("github")
        self.assertNotEqual(len(search), 0)

    @load_html_file("html_files")
    def test_shopping_search(self, html_f):
        """Test method for google shopping."""

        # replace method to get html from a test html file
        google.shopping_search.get_html = \
            Mock(return_value=html_f.read().decode('utf8'))

        shop = google.shopping("Disgaea 4")
        self.assertNotEqual(len(shop), 0)


class ConvertCurrencyTest(unittest.TestCase):

    def test_get_currency_req_url(self):
        """Test method to get currency conversion request url."""

        amount = 10
        from_currency = "USD"
        to_currency = "EUR"
        req_url = currency._get_currency_req_url(amount, from_currency,
                                                 to_currency)

        exp_req_url = "https://www.google.com/finance/converter?a=10&from=USD&to=EUR"

        self.assertEqual(req_url, exp_req_url)

    # @unittest.skip("skip")
    def test_parse_currency_response(self):
        """Test method to parse currency response. TODO!"""
        pass

# @unittest.skip("skip")


class SearchImagesTest(unittest.TestCase):

    def test_get_images_req_url(self):

        query = "banana"
        options = images.ImageOptions()
        options.image_type = images.ImageType.CLIPART
        options.larger_than = images.LargerThan.MP_4
        options.color = "green"
        options.license = images.License.REUSE_WITH_MOD

        req_url = images._get_images_req_url(query, options)

        exp_req_url = 'https://www.google.com.ar/search?q=banana&es_sm=122&source=lnms&tbm=isch&sa=X&ei=DDdUVL-fE4SpNq-ngPgK&ved=0CAgQ_AUoAQ&biw=1024&bih=719&dpr=1.25&tbs=itp:clipart,isz:lt,islt:4mp,ic:specific,isc:green,sur:fmc'

        self.assertEqual(req_url, exp_req_url)

    def test_repr(self):
        res = images.ImageResult()
        assert repr(res) == 'ImageResult(index=None, page=None, domain=None, link=None)'
        res.page = 1
        res.index = 11
        res.name = 'test'
        res.thumb = 'test'
        res.format = 'test'
        res.domain = 'test'
        res.link = 'http://aa.com'
        assert repr(res) == 'ImageResult(index=11, page=1, domain=test, link=http://aa.com)'

    def test_download(self):
        pass

    def test_fast_download(self):
        pass


if __name__ == '__main__':
    # nose.main()
    nose.run(defaultTest=__name__)

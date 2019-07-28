from __future__ import unicode_literals

import time
from selenium import webdriver
import urllib2
from functools import wraps
#import requests
from urllib import urlencode


def measure_time(fn):

    def decorator(*args, **kwargs):
        start = time.time()

        res = fn(*args, **kwargs)

        elapsed = time.time() - start
        print fn.__name__, "took", elapsed, "seconds"

        return res

    return decorator


def normalize_query(query):
    return query.strip().replace(":", "%3A").replace("+", "%2B").replace("&", "%26").replace(" ", "+")


def _get_search_url(query, page=0, per_page=10, lang='en'):
    # note: num per page might not be supported by google anymore (because of
    # google instant)

    params = {'nl': lang, 'q': query.encode(
        'utf8'), 'start': page * per_page, 'num': per_page}
    params = urlencode(params)
    url = u"http://www.google.com/search?" + params
    # return u"http://www.google.com/search?hl=%s&q=%s&start=%i&num=%i" %
    # (lang, normalize_query(query), page * per_page, per_page)
    return url


def get_html(url):
    header = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
    try:
        request = urllib2.Request(url)
        request.add_header("User-Agent", header)
        html = urllib2.urlopen(request).read()
        return html
    except urllib2.HTTPError as e:
        print "Error accessing:", url
        if e.code == 503 and 'CaptchaRedirect' in e.read():
            print "Google is requiring a Captcha. " \
                  "For more information see: 'https://support.google.com/websearch/answer/86640'"
        return None
    except Exception as e:
        print "Error accessing:", url
        print e
        return None


def write_html_to_file(html, filename):
    of = open(filename, "w")
    of.write(html.encode("utf-8"))
    # of.flush()
    of.close()


def get_browser_with_url(url, timeout=120, driver="firefox"):
    """Returns an open browser with a given url."""

    # choose a browser
    if driver == "firefox":
        browser = webdriver.Firefox()
    elif driver == "ie":
        browser = webdriver.Ie()
    elif driver == "chrome":
        browser = webdriver.Chrome()
    else:
        print "Driver choosen is not recognized"

    # set maximum load time
    browser.set_page_load_timeout(timeout)

    # open a browser with given url
    browser.get(url)

    time.sleep(0.5)

    return browser


def get_html_from_dynamic_site(url, timeout=120,
                               driver="firefox", attempts=10):
    """Returns html from a dynamic site, opening it in a browser."""

    RV = ""

    # try several attempts
    for i in xrange(attempts):
        try:
            # load browser
            browser = get_browser_with_url(url, timeout, driver)

            # get html
            time.sleep(2)
            content = browser.page_source

            # try again if there is no content
            if not content:
                browser.quit()
                raise Exception("No content!")

            # if there is content gets out
            browser.quit()
            RV = content
            break

        except:
            print "\nTry ", i, " of ", attempts, "\n"
            time.sleep(5)

    return RV


def timeit(func=None, loops=1, verbose=False):
    if func:
        def inner(*args, **kwargs):

            sums = 0.0
            mins = 1.7976931348623157e+308
            maxs = 0.0
            print '====%s Timing====' % func.__name__
            for i in range(0, loops):
                t0 = time.time()
                result = func(*args, **kwargs)
                dt = time.time() - t0
                mins = dt if dt < mins else mins
                maxs = dt if dt > maxs else maxs
                sums += dt
                if verbose:
                    print '\t%r ran in %2.9f sec on run %s' % (func.__name__, dt, i)
            print '%r min run time was %2.9f sec' % (func.__name__, mins)
            print '%r max run time was %2.9f sec' % (func.__name__, maxs)
            print '%r avg run time was %2.9f sec in %s runs' % (func.__name__, sums / loops, loops)
            print '==== end ===='
            return result

        return inner
    else:
        def partial_inner(func):
            return timeit(func, loops, verbose)
        return partial_inner


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
            (f.__name__, args, kw, te - ts)
        return result
    return wrap

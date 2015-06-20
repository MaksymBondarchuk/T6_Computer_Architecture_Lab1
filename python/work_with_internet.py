__author__ = 'max'

from lxml import html
import requests
import gevent


# Downloads data from url
# XPath_list - list of strings
# Returns list of  strings as data from XPath_list
def get_data_from_url_with_xpathes(url):
    page = requests.get(url['url'])
    page_tree = html.fromstring(page.text)
    return {'buy': float(page_tree.xpath('%s/text()' % url['buy'])[0].replace(',', '.')),
            'sale': float(page_tree.xpath('%s/text()' % url['sale'])[0].replace(',', '.')),
            'name': url['name']}


def get_data_from_urls_with_xpathes(urls, download_mode):
    if download_mode == 'simple':
        return [get_data_from_url_with_xpathes(url) for url in urls]
    if download_mode == 'gevent':
        work = [gevent.spawn(get_data_from_url_with_xpathes, url) for url in urls]
        gevent.joinall(work)
        return [thread.value for thread in work]

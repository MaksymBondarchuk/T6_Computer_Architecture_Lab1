import time

import gevent

from common import *



# Gets data from url and then calls itself
def get_data_from_url(url, depth):
    emails_and_urls = get_data_from_url_common(url, depth)  # Dictionary
    emails_list = emails_and_urls['emails']
    urls_list = emails_and_urls['urls']

    work = [gevent.spawn(get_data_from_url, url, depth + 1) for url in urls_list]
    gevent.joinall(work)
    emails_list.extend(thread.value for thread in work)

    if not emails_list:
        return []
    return emails_list[0]


# Gets data from urls. Returns emails list
def get_data_from_urls(urls_list):
    work = [gevent.spawn(get_data_from_url, url, 1) for url in urls_list]
    gevent.joinall(work)
    emails_list = []
    emails_list.extend(thread.value for thread in work)
    return emails_list[0]


start_time = time.time()
urls_lst = get_data_from_xml('input.xml')
emails_lst = get_data_from_urls(urls_lst)
print_to_xml('output.xml', emails_lst)
print('Time of program work is %s seconds' % (time.time() - start_time))

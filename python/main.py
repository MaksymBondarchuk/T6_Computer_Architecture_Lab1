import time

from python.common import *


# Gets data from url and then calls itself
def get_data_from_url(url, depth):
    emails_and_urls = get_data_from_url_common(url, depth)  # Dictionary
    emails_list = emails_and_urls['emails']
    urls_list = emails_and_urls['urls']

    for _url in urls_list:
        emails = get_data_from_url(_url, depth + 1)
        emails_list.extend(emails)

    return emails_list


# Gets data from urls. Returns emails list
def get_data_from_urls(urls_list):
    emails_list = []
    for url in urls_list:
        emails_list.extend(get_data_from_url(url, 1))
    return emails_list


if __name__ == '__main__':
    start_time = time.time()
    urls_lst = get_data_from_xml('../xml/input.xml')
    emails_lst = get_data_from_urls(urls_lst)
    print_to_xml('../xml/output.xml', emails_lst)
    print('Time of program work is %s seconds' % (time.time() - start_time))

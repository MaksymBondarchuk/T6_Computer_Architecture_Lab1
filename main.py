import xml.etree.ElementTree as ET
import time
import re
import sys

import requests


def get_data_from_url(url, depth):
    for i in range(2, depth + 1):
        sys.stdout.write('\t')
    print("On url: %s, depth: %d" % (url, depth))

    try:
        page = requests.get(url)
    except:
        return []

    emails_list = []
    emails = re.findall('[\w\.-]+@[\w\.-]+', page.text)
    for email in emails:
        emails_list.append(email)
        for i in range(1, depth + 1):
            sys.stdout.write('\t')
        print(email)

    if depth == 2:
        return []

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page.text)
    for _url in urls:
        if _url != url:
            emails = get_data_from_url(_url, depth + 1)
            emails_list.extend(emails)

    return emails_list


def get_data_from_xml(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()

    urls = []
    for url in root.findall('url'):
        urls.extend(url.text)
        emails = get_data_from_url(url.text, 1)
        print_to_xml('output.xml', emails)
    return urls


def print_to_xml(xml_name, emails):
    root = ET.Element('emails')
    for email in emails:
        mail = ET.SubElement(root, 'email')
        mail.text = email
    tree = ET.ElementTree(root)
    tree.write(xml_name, 'utf-8')


start_time = time.time()
get_data_from_xml('input.xml')

# if isinstance([1, 2, 3], list):
# print("Yes")
# else:
#     print('No')

print('Time of program work is %s seconds' % (time.time() - start_time))

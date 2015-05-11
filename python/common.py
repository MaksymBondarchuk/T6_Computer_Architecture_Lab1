import xml.etree.ElementTree as ET
import re
import sys

import requests


max_depth = 2
# If you don't want program to print current state
# to terminal, switch to False
print_to_terminal = True


# Gets data from xml file. Returns urls list
def get_data_from_xml(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()

    urls = []
    for url in root.findall('url'):
        urls.append(url.text)
    return urls


# Prints data (emails list) to xml-file
def print_to_xml(xml_name, emails):
    root = ET.Element('emails')
    for email in emails:
        mail = ET.SubElement(root, 'email')
        mail.text = email
    tree = ET.ElementTree(root)
    tree.write(xml_name, 'utf-8')


def get_data_from_url_common(url, depth):
    # Print to terminal
    if print_to_terminal:
        for i in range(2, depth + 1):
            sys.stdout.write('\t')
        print("On url: %s, depth: %d" % (url, depth))

    # Trying to download page. If error occurred, returns empty list
    try:
        page = requests.get(url).text
    except:
        return []

    # Getting all emails on this page
    emails_list = []
    emails = re.findall('[\w\.-]+@[\w\.-]+', page)
    for email in emails:
        emails_list.append(email)

        # Print to terminal
        if print_to_terminal:
            for i in range(1, depth + 1):
                sys.stdout.write('\t')
            print(email)

    # If we cannot go to links on this page
    if depth == max_depth:
        return {'emails': emails_list, 'urls': []}

    # Going to all links on this page
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                      '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)

    # Removing current url from list
    try:
        urls.remove(url)
    except:
        pass

    return {'emails': emails_list, 'urls': urls}

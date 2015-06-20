__author__ = 'max'

import xml.etree.ElementTree as eT
from arithmetics import *


# Download data from xml-file
# xml-file must be like:
# <string>
#   <bank name='string'>
#       <url>bank_url</url>
#       <buy>XPath</buy>
#       <sale>XPath</sale>
#   </bank>
#   ... (oother banks)
# </string>
# Returns list of dictionaries like
# {'name':<string>, 'buy':<float>, 'sale':<float>}
def get_data_from_xml(xml_name):
    tree = eT.parse(xml_name)
    root = tree.getroot()

    urls_with_xpathes = []
    for bank in root.findall('bank'):
        name = bank.get('name')
        url = bank.find('url').text
        buy = bank.find('buy').text
        sale = bank.find('sale').text
        one_bank_url = {'name': name, 'url': url, 'buy': buy, 'sale': sale}
        urls_with_xpathes.append(one_bank_url)
    return urls_with_xpathes


# Prints data to xml file. banks - list of dictionaries like
# {'name':<string>, 'buy':<float>, 'sale':<float>}
def print_to_xml(xml_name, data):
    root = eT.Element('data')
    usd = eT.SubElement(root, 'usd')

    # Calculating data for buy
    buy = eT.SubElement(usd, 'buy')
    min_buy = eT.SubElement(buy, 'min')
    min_buy_bank = get_min(data, 'buy')
    eT.SubElement(min_buy, 'bank').text = min_buy_bank['name']
    eT.SubElement(min_buy, 'value').text = str(min_buy_bank['buy'])

    max_buy = eT.SubElement(buy, 'max')
    max_buy_bank = get_max(data, 'buy')
    eT.SubElement(max_buy, 'bank').text = max_buy_bank['name']
    eT.SubElement(max_buy, 'value').text = str(max_buy_bank['buy'])
    eT.SubElement(buy, 'average').text = str(get_average(data, 'buy'))

    # Calculating data for sale
    sale = eT.SubElement(usd, 'sale')
    min_sale = eT.SubElement(sale, 'min')
    min_sale_bank = get_min(data, 'sale')
    eT.SubElement(min_sale, 'bank').text = min_sale_bank['name']
    eT.SubElement(min_sale, 'value').text = str(min_sale_bank['sale'])

    max_sale = eT.SubElement(sale, 'max')
    max_sale_bank = get_max(data, 'sale')
    eT.SubElement(max_sale, 'bank').text = max_sale_bank['name']
    eT.SubElement(max_sale, 'value').text = str(max_sale_bank['sale'])
    eT.SubElement(sale, 'average').text = str(get_average(data, 'sale'))

    # Print it to xml-file
    tree = eT.ElementTree(root)
    tree.write(xml_name, 'utf-8')

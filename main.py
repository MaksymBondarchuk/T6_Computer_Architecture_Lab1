import xml.etree.ElementTree as ET
import time

from lxml import html
import requests



# Downloads data from url
# XPath_list - list of strings
# Returns list of  strings as data from XPath_list
def get_data_from_url(url, XPath_list):
    page = requests.get(url)
    page_tree = html.fromstring(page.text)
    data_lst = []
    for XPath in XPath_list:
        data_lst.append(page_tree.xpath('%s/text()' % XPath)[0])
    return data_lst


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
    tree = ET.parse(xml_name)
    root = tree.getroot()

    banks = []
    for bank in root.findall('bank'):
        name = bank.get('name')
        url = bank.find('url').text
        buy = bank.find('buy').text
        sale = bank.find('sale').text
        one_bank = {}
        one_bank_data = get_data_from_url(url, [buy, sale])
        one_bank['name'] = name
        one_bank['buy'] = float(one_bank_data[0].replace(',', '.'))
        one_bank['sale'] = float(one_bank_data[1].replace(',', '.'))
        banks.append(one_bank)
    return banks


# Returns minimal buy or sell proposition
# buy_or_sell == 'buy' || 'sale'
def get_min(banks, buy_or_sale):
    min_item = banks[0]
    for bank in banks:
        if bank[buy_or_sale] < min_item[buy_or_sale]:
            min_item = bank
    return min_item


# Returns maximal buy or sell proposition
# buy_or_sell == 'buy' || 'sale'
def get_max(banks, buy_or_sale):
    max_item = banks[0]
    for bank in banks:
        if max_item[buy_or_sale] < bank[buy_or_sale]:
            max_item = bank
    return max_item


# Returns average buy or sell cost
# buy_or_sell == 'buy' || 'sale'
def get_average(banks, buy_or_sale):
    average = 0
    for bank in banks:
        average += bank[buy_or_sale]
    return average / len(banks)


# Prints data to xml file. banks - list of dictionaries like
# {'name':<string>, 'buy':<float>, 'sale':<float>}
def print_to_xml(xml_name, banks):
    root = ET.Element('data')
    usd = ET.SubElement(root, 'usd')

    # Calculating data for buy
    buy = ET.SubElement(usd, 'buy')
    min_buy = ET.SubElement(buy, 'min')
    min_buy_bank = get_min(banks, 'buy')
    ET.SubElement(min_buy, 'bank').text = min_buy_bank['name']
    ET.SubElement(min_buy, 'value').text = str(min_buy_bank['buy'])

    max_buy = ET.SubElement(buy, 'max')
    max_buy_bank = get_max(banks, 'buy')
    ET.SubElement(max_buy, 'bank').text = max_buy_bank['name']
    ET.SubElement(max_buy, 'value').text = str(max_buy_bank['buy'])
    ET.SubElement(buy, 'average').text = str(get_average(banks, 'buy'))

    # Calculating data for sale
    sale = ET.SubElement(usd, 'sale')
    min_sale = ET.SubElement(sale, 'min')
    min_sale_bank = get_min(banks, 'sale')
    ET.SubElement(min_sale, 'bank').text = min_sale_bank['name']
    ET.SubElement(min_sale, 'value').text = str(min_sale_bank['sale'])

    max_sale = ET.SubElement(sale, 'max')
    max_sale_bank = get_max(banks, 'sale')
    ET.SubElement(max_sale, 'bank').text = max_sale_bank['name']
    ET.SubElement(max_sale, 'value').text = str(max_sale_bank['sale'])
    ET.SubElement(sale, 'average').text = str(get_average(banks, 'sale'))

    # Print it to xml-file
    tree = ET.ElementTree(root)
    tree.write(xml_name, 'utf-8')

start_time = time.time()
print_to_xml('output.xml', get_data_from_xml('input.xml'))
print('Time of program work is %s seconds' % (time.time() - start_time))

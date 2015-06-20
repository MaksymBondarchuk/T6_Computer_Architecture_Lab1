__author__ = 'max'

import time
from python.work_with_internet import get_data_from_urls_with_xpathes
from work_with_xml import *
import ConfigParser

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('../lab1.config')
    if not config.has_section('network') or not config.has_option('network', 'mode'):
        print ('Configuration file must have "network" section with "lib" option ("gevent" or "simple")')
        exit()
    if not config.has_section('xml') or not config.has_option('xml', 'input') or not config.has_option('xml', 'output'):
        print ('Configuration file must have "xml" section with "input" and "output" options (file names)')
        exit()
    mode = config.get('network', 'mode')
    input_file = config.get('xml', 'input')
    output_file = config.get('xml', 'output')

    start_time = time.time()
    urls = get_data_from_xml('../xml/%s' % input_file)
    data = get_data_from_urls_with_xpathes(urls, mode)
    print_to_xml('../xml/%s' % output_file, data)
    print('Time of program work is %s seconds' % (time.time() - start_time))

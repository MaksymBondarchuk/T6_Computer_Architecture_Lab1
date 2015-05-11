import unittest

from mock import *

from python import common


class Test(unittest.TestCase):
    def test_get_data_from_xml(self):
        name = 'test_input.xml'
        data = common.get_data_from_xml(name)
        self.assertEqual(data, ['html'])

    def test_print_to_xml(self):
        name = 'test_output.xml'
        emails = ['dliubych@gmail.com', 'pashko@gmail.com']
        common.print_to_xml(name, emails)
        f = open(name, 'r')
        text = f.read()
        self.assertEqual(text, '<emails><email>dliubych@gmail.com</email><email>pashko@gmail.com</email></emails>')

    @patch('requests.get')
    def test_get_data_from_url_common(self, request_function):
        mock = Mock()

        f = open('html_page.html', 'r')
        html_code = f.read()

        class HTML:
            def __init__(self):
                pass

            text = html_code

        pseudo_html_page = HTML()
        pseudo_html_page.text = html_code

        mock.return_value = pseudo_html_page
        request_function.return_value = mock.return_value

        res = common.get_data_from_url_common('http://www.cvk.gov.ua/pls/vnd2014/wp312?PT001F01=910', 1)
        self.assertEqual(res['emails'], ['post@cvk.gov.ua'])


if __name__ == '__main__':
    unittest.main()
import unittest

from python import common


class Test(unittest.TestCase):
    def test_get_data_from_xml(self):
        name = 'test_input.xml'
        data = common.get_data_from_xml(name)
        self.assertEqual(data, ['html'])


if __name__ == '__main__':
    unittest.main()
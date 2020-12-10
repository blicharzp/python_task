"""Banking data parser unit tests
Run command:  python3 -m unittest -v tests_data_parser.py
"""


import unittest
import data_parser
from unittest.mock import patch, ANY


class TestDataFormatter(unittest.TestCase):

    def test_property_content(self):
        data_formatter = data_parser.DataFormatter()
        self.assertEqual(data_formatter.content, {})

    def test_direction_parser_valid(self):
        data_formatter = data_parser.DataFormatter()
        self.assertEqual(data_formatter.direction_parser("42"), "42")

    def test_direction_parser_notvalid(self):
        data_formatter = data_parser.DataFormatter()
        with self.assertRaises(ValueError):
            data_formatter.direction_parser("foo")

    def test_amount_parser_without_subunit(self):
        data_formatter = data_parser.DataFormatter()
        self.assertEqual(data_formatter.amount_parser("42"), "42.00")

    def test_amount_parser_with_subunit(self):
        data_formatter = data_parser.DataFormatter()
        self.assertEqual(data_formatter.amount_parser("42", "43"), "42.43")

    def test_amount_parser_notvalid(self):
        data_formatter = data_parser.DataFormatter()
        with self.assertRaises(ValueError):
            data_formatter.amount_parser("foo")

    def test_transaction_parser_valid(self):
        data_formatter = data_parser.DataFormatter()
        self.assertEqual(data_formatter.transaction_parser("add"), "add")

    def test_transaction_parser_notvalid(self):
        data_formatter = data_parser.DataFormatter()
        with self.assertRaises(ValueError):
            data_formatter.transaction_parser("foo")

    def test_date_parser_valid(self):
        RAW_DATES = ["Oct 1 2019", "01-10-2019", "1 Oct 2019"]
        EXPECTED_DATE = "01-10-2019"
        data_formatter = data_parser.DataFormatter()
        for date in RAW_DATES:
            self.assertEqual(data_formatter.date_parser(date), EXPECTED_DATE)

    def test_date_parser_notvalid(self):
        data_formatter = data_parser.DataFormatter()
        with self.assertRaises(ValueError):
            data_formatter.date_parser("01/10/2019")


class TestDataParser(unittest.TestCase):
    INPUT = [{"foo": 1234}]
    PATH = "bar"
    TYPE = "csv"

    def test_save_to_file_add_extension(self):
        with patch("data_parser.save_to_csv_file") as save_to_csv_file:
            data_parser.save_to_file(self.INPUT, self.PATH, self.TYPE)
            save_to_csv_file.assert_called_once_with(
                self.INPUT, self.PATH + ".csv")

    def test_save_to_file_not_add_extension(self):
        PATH_WITH_EXTENSION = self.PATH + ".csv"
        with patch("data_parser.save_to_csv_file") as save_to_csv_file:
            data_parser.save_to_file(
                self.INPUT, PATH_WITH_EXTENSION, self.TYPE)
            save_to_csv_file.assert_called_once_with(
                self.INPUT, PATH_WITH_EXTENSION)

    def test_save_to_csv_file(self):
        with patch("builtins.open") as op:
            with patch("csv.DictWriter") as dict_writer:
                data_parser.save_to_csv_file(self.INPUT, self.PATH)
                dict_writer.assert_called_once_with(
                    ANY, fieldnames=self.INPUT[0].keys())
            op.assert_called_once_with(self.PATH, "w")

    def test_save_to_json_file(self):
        with patch("builtins.open") as op:
            with patch("json.dump") as dump:
                data_parser.save_to_json_file(self.INPUT, self.PATH)
                dump.assert_called_once_with(self.INPUT, ANY, indent=4)
            op.assert_called_once_with(self.PATH, "w")

    def test_save_to_xml_file(self):
        with patch("builtins.open") as op:
            with patch("xml.etree.ElementTree.Element") as et_element:
                with patch("xml.etree.ElementTree.tostring") as tostring:
                    with patch("xml.dom.minidom.parseString") as parse_string:
                        data_parser.save_to_xml_file(self.INPUT, self.PATH)
                        self.assertEqual(et_element.call_count, 3)
                    tostring.assert_called_once()
                parse_string.assert_called_once()
            op.assert_called_once_with(self.PATH, "w")


if __name__ == '__main__':
    unittest.main()

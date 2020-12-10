"""Data parser and unifier for various bank entires.
supported version of python: 3.7 or higher. It is related to the ordering mechanism of elements in dict
usage: data_parser.py [-h] [-t {csv,json,xml}] [-p PATH] input_files [input_files ...]
example usage: python3 data_parser.py bank1.csv bank2.csv bank3.csv -t csv
"""


import csv
import datetime
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import logging
from argument_parser import argument_parser
from typing import List


class DataFormatter:
    """DataFormatter is a base class which provides parser methods for
    each input parameters of its children. Each metchod check if input
    parameter can be converted and convert them to the unified format.
    DataFormatter is introduced to standardize layout for various input.
    """

    def __init__(self) -> None:
        """Initializer, provide empty _content dict for children classes
        """
        self._content = {}

    @staticmethod
    def date_parser(date: str) -> str:
        """date_parser parses various date formats into %d-%m-%Y
        :param date: date in one of the supported formats: %b %d %Y, %d-%m-%Y, %d %b %Y
        :type date: str
        :raises ValueError: Raises when inputted format is not in the supported one
        :return: date in %d-%m-%Y format
        :rtype: str
        """
        TIMEFORMATS = ["%b %d %Y", "%d-%m-%Y", "%d %b %Y"]
        for format in TIMEFORMATS:
            try:
                date = datetime.datetime.strptime(date, format)
                return date.strftime("%d-%m-%Y")
            except ValueError:
                continue
        raise ValueError(f"Date: {date} is a not in supported format.")

    @staticmethod
    def transaction_parser(transaction: str) -> str:
        """transaction_parser when input is add or remove returns input otherwise
        throw exception
        :param transaction: transaction with one of the supported values: add or remove
        :type transaction: str
        :raises ValueError: Raises when inputted transaction is not add or remove
        :return: add or remove
        :rtype: str
        """
        OPERATIONS = ["add", "remove"]
        if transaction in OPERATIONS:
            return transaction
        raise ValueError(f"Transaction: {transaction} is not supported value.")

    @staticmethod
    def amount_parser(unit: str = "", subunit: str = "") -> str:
        """amount_parser check is amount unit and subunit parameters are numeric
        fill with zero(s) the unit and subunit parts to receive 1 and 2 digits output
        :param unit: unit part of an amount
        :type unit: str
        :param subunit: subunit part of an amount
        :type subunit: str
        :raises ValueError: Raises when inputted unit or subunit are not numeric and not empty strings
        :return: amount in format unit.subunit
        :rtype: str
        """
        if not unit.isnumeric() and unit:
            raise ValueError(
                f"Amount unit part: {unit} is not numeric.")
        if not subunit.isnumeric() and subunit:
            raise ValueError(
                f"Amount subunit part: {subunit} is not numeric.")
        return f"{unit.zfill(1)}.{subunit.zfill(2)}"

    @staticmethod
    def direction_parser(direction: str) -> str:
        """direction_parser check if direction is a number
        :param direction: direction numeric
        :type direction: str
        :raises ValueError: Raises when inputted direction is not numeric
        :return: direction
        :rtype: str
        """
        if not direction.isnumeric():
            raise ValueError(
                f"Direction: {direction} is not numeric.")
        return direction

    @property
    def content(self) -> dict:
        """content returns formatted content
        :return: formatted content
        :rtype: dict
        """
        return self._content


class Bank1Formatter(DataFormatter):
    def __init__(self, timestamp: str, type_: str, amount: str, from_: str, to: str) -> None:
        """Initializer, fills the field in specified by Bank1 format
        :param timestamp: input timestamp field in Bank1 format saved as date
        :type timestamp: str
        :param type_: input type field in Bank1 format saved as transaction
        :type type_: str
        :param amount: input amount field in Bank1 format saved as amounts
        :type amount: str
        :param from_: input from field in Bank1 format saved as from
        :type from_: str
        :param to: input to field in Bank1 format saved as to
        :type to: str
        """
        super().__init__()
        self._content["date"] = self.date_parser(timestamp)
        self._content["transaction"] = self.transaction_parser(type_)
        self._content["amounts"] = self.amount_parser(*amount.split("."))
        self._content["from"] = self.direction_parser(from_)
        self._content["to"] = self.direction_parser(to)


class Bank2Formatter(DataFormatter):
    def __init__(self, date: str, transaction: str, amounts: str, to: str, from_: str) -> None:
        """Initializer, fills the field in specified by Bank2 format
        :param date: input date field in Bank2 format saved as date
        :type date: str
        :param transaction: input transaction field in Bank2 format saved as transaction
        :type transaction: str
        :param amounts: input amounts field in Bank2 format saved as amounts
        :type amounts: str
        :param to: input to field in Bank2 format saved as to
        :type to: str
        :param from_: input from field in Bank2 format saved as from
        :type from_: str
        """
        super().__init__()
        self._content["date"] = self.date_parser(date)
        self._content["transaction"] = self.transaction_parser(transaction)
        self._content["amounts"] = self.amount_parser(*amounts.split("."))
        self._content["to"] = self.direction_parser(to)
        self._content["from"] = self.direction_parser(from_)


class Bank3Formatter(DataFormatter):
    def __init__(self, date_readable: str, type_: str, euro: str, cents: str, to: str, from_: str) -> None:
        """Initializer, fills the field in specified by Bank3 format
        :param date_readable: input date_readable field in Bank3 format saved as date
        :type date_readable: str
        :param type_: input type field in Bank3 format saved as transaction
        :type type_: str
        :param euro: input euro field in Bank3 format saved as unit part of amounts
        :type euro: str
        :param cents: input cents field in Bank3 format saved as subunit part of amounts
        :type cents: str
        :param to: input to field in Bank3 format saved as to
        :type to: str
        :param from_: input from field in Bank3 format saved as from
        :type from_: str
        """
        super().__init__()
        self._content["date"] = self.date_parser(date_readable)
        self._content["transaction"] = self.transaction_parser(type_)
        self._content["amounts"] = self.amount_parser(euro, cents)
        self._content["to"] = self.direction_parser(to)
        self._content["from"] = self.direction_parser(from_)


BANK_FORMATTERS = {
    ("timestamp", "type", "amount", "from", "to"): Bank1Formatter,
    ("date", "transaction", "amounts", "to", "from"): Bank2Formatter,
    ("date_readable", "type", "euro", "cents", "to", "from"): Bank3Formatter
}


def save_to_file(content: List[dict], path: str, type_: str) -> None:
    """save_to_file formats to specific type content and save it to inputted path output
    :param content: content to save
    :type content:  List[dict]
    :param path: path where to save content
    :type path: str
    :param type_: select type of output, supported types: [csv, json, xml]
    :type type_: str
    """
    save = {
        "csv": save_to_csv_file,
        "json": save_to_json_file,
        "xml": save_to_xml_file
    }[type_]
    extension = f".{type_}"
    if not path.endswith(extension):
        path += extension
    save(content, path)


def save_to_csv_file(content: List[dict], path: str) -> None:
    """save_to_csv_file saves formmated content to inputted path output as csv file
    :param content: content to save
    :type content:  List[dict]
    :param path: path where to save content
    :type path: str
    """
    with open(path, "w") as fp:
        header = content[0].keys()
        writer = csv.DictWriter(fp, fieldnames=header)
        writer.writeheader()
        for row in content:
            writer.writerow(row)


def save_to_json_file(content: List[dict], path: str) -> None:
    """save_to_json_file saves formmated content to inputted path output as json file
    :param content: content to save
    :type content:  List[dict]
    :param path: path where to save content
    :type path: str
    """
    with open(path, "w") as fp:
        json.dump(content, fp, indent=4)


def save_to_xml_file(content: List[dict], path: str) -> None:
    """save_to_xml_file saves formmated content to inputted path output as xml file
    :param content: content to save
    :type content:  List[dict]
    :param path: path where to save content
    :type path: str
    """
    root = ET.Element("root")
    for row in content:
        item = ET.Element("item")
        for key, value in row.items():
            child = ET.Element(key)
            child.text = value
            item.append(child)
        root.append(item)
    formatted_xml = minidom.parseString(ET.tostring(
        root, xml_declaration=True)).toprettyxml(indent="    ")
    with open(path, "w") as fp:
        fp.write(formatted_xml)


def main() -> None:
    args = argument_parser()
    formatted_output = []
    for filename in args.input_files:
        with open(filename) as fp:
            csvreader = csv.reader(fp, delimiter=",")
            header = tuple(next(csvreader))
            try:
                bank_formatter = BANK_FORMATTERS[header]
                for row in csvreader:
                    formatted_output.append(bank_formatter(*row).content)
            except KeyError:
                logging.warning(f"File: {filename} has not supported header.")
    if formatted_output:
        save_to_file(formatted_output, args.path, args.type)
    else:
        logging.warning("No data to save.")


if __name__ == "__main__":
    main()

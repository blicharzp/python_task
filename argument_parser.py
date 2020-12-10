import argparse
import os.path


def argument_parser() -> argparse.Namespace:
    """Argument parser for banking data parser
    usage: data_parser.py [-h] [-t {csv,json,xml}] [-p PATH] input_files [input_files ...]
    :return: Script input parameters
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description='Bank statements unifier script')
    parser.add_argument('input_files', type=str, nargs='+',
                        help='Input csv filenames.')
    parser.add_argument("-t", "--type", type=str, choices=["csv", "json", "xml"], default="csv",
                        help='Output file type.')
    parser.add_argument("-p", "--path", type=str, default=f"./output",
                        help='Output file path.')
    args = parser.parse_args()
    for filename in args.input_files:
        if not os.path.exists(filename):
            parser.error(f"File: {filename} does not exist.")
    return args

#!/usr/bin/env python3
"""Convert AMISR Array Status XML to JSON."""

##########################################################################
#
#   AMISR Array Status XML to JSON converter application
#
#   2024-01-29  Todd Valentic
#               Initial implementation
#
##########################################################################

import argparse
import json
import pathlib

import amisr_toolkit as atk


def parse_command_line():
    """Parse the command line arguments."""
    desc = "AMISR Array Status XML to JSON Converter"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "filename", type=pathlib.Path, help="Input filename (may be compressed)"
    )

    parser.add_argument(
        "-c", "--compact",
        action="store_true", 
        help="Remove little used fields"
    )

    parser.add_argument(
        "-n", "--ndigits",
        nargs="?",
        const=1,
        type=int,
        help="Round floats to n digits"
    )

    args = parser.parse_args()

    return args


def main():
    """Program entry point."""
    args = parse_command_line()

    options = {
        "ndigits": args.ndigits,
        "compact": args.compact,
    }

    buffer = args.filename.read_bytes()
    results = atk.parse_array_status_xml(buffer, **options)

    print(json.dumps(results))

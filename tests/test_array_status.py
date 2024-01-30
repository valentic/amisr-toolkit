"""AEUStatus Unit Tests"""

import bz2
from pathlib import Path
import pytest

import amisr_toolkit as atk

def test_parse():
    filename = Path("20240126-025800-pfisr.xml.bz2")
    buffer = bz2.decompress(filename.read_bytes())
    status = atk.parse_array_status_xml(buffer) 

    assert status
 


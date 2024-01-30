#!/usr/bin/env python3

##########################################################################
#
#   AMISR Array XML Status Parser
#
#   Convert a byte stream representing the AMISR array status into a 
#   dictionary. The byte stream may be compressed (bz2, gzip, lzma)
#
#   2024-01-29  Todd Valentic
#               Initial implementation
#
##########################################################################

import bz2
import gzip
import lzma
import magic

import xml.etree.ElementTree as ET
from . import aeustatus

compact_key_filter = [
    "firmware_major",
    "firmware_minor",
    "firmware_patch",
    "signal_count",
    "signal_voltage",
    "beamcodes",
    "interrupt_count",
    "status_format"
]

def round_floats(values, ndigits):

    results = {}

    if isinstance(values, list):
        return [round_floats(v, ndigits) for v in values]

    elif isinstance(values, float):
        return round(values, ndigits)
    
    elif isinstance(values, dict):
        return { k: round_floats(v, ndigits) for k,v in values.items() }

    else:
        return values


def parse_array_status_xml(buffer, compact=False, ndigits=None): 

    filetype = magic.Magic(mime=True).from_buffer(buffer)

    if filetype == "text/plain":
        contents = buffer
    elif filetype == "application/x-bzip2":
        contents = bz2.decompress(buffer)
    elif filetyle == "application/gzip":
        contents = gzip.decompress(buffer)
    elif filetyle == "application/x-xz":
        contents = lzma.decompress(buffer)
    else:
        raise ValueError("Unknown data format: %s", filetype)

    tree = ET.ElementTree(ET.fromstring(contents))
    root = tree.getroot()
    power = root.find(".//power")

    results = {}

    metadata = {
        "timestamp": root.get("timestamp"),
        "face": root.get("face"),
        #"device_id": entry["device_id"]
    }

    summary = {
        "good": int(power.get("good")),
        "bad": int(power.get("bad")),
        "ugly": int(power.get("ugly")), 
        "total": int(power.get("total")), 
        "peak_power": round(float(power.get("peak")),1), 
        "rf_enabled": bool(int(power.get("rf")))
    }

    results = {
        "metadata": metadata,
        "summary": summary,
    }

    panels = {} 

    for panel in root.findall(".//panel"):
        aeus = {}

        for aeu in panel.findall("aeu"):
            values = {}
            values["pwatts"] = float(aeu.get("pwatts"))
            
            try:
                status = aeustatus.AEUStatus(aeu.text)
            except:
                status = None

            if status:
                values = vars(status)

                if compact: 
                    values["firmware"] = (
                        f"{values['firmware_major']}."
                        f"{values['firmware_minor']}."
                        f"{values['firmware_patch']}"
                    )
                    values = {k:v for k,v in values.items() if k not in compact_key_filter}

                if ndigits is not None:
                    values = round_floats(values, ndigits)

            position = int(aeu.get("position"))
            aeus[position] = values

        panel_name = panel.get("id")
        panels[panel_name] = aeus 

    results["panels"] = panels

    return results



#!/usr/bin/env python

""" content generator """

from multiprocessing import Pool
import os
from pathlib import Path

DATADIR = "data"
OUTPUT_DIR = "docs"

PROTOCOLS = [ 'tcp', 'udp' ]
NUM_PROCESSES = 4

POST_TEMPLATE = """---
title: "{protocol}/{port}"
tags: [ "{protocol}" ]
categories : [ "{protocol}" ]
url: /{protocol}/{port}
---

[Home](/) - [{protocol}](/{protocol}/) - {port}
"""

def do_content(input_data):
    """ takes a protocol and port tuple and does the processing for that combination """

    protocol, port = input_data
    portdir = f"{DATADIR}/{protocol}/{port}"
    portfile = f"{OUTPUT_DIR}/{protocol}/{port}.md"
    if os.path.isdir(portdir):
        info = {'protocol' : protocol, 'port' : port}
        # base template
        portdata = POST_TEMPLATE.format(**info)
        notes = ianadata = False
        notesfile = Path("{portdir}/notes.md")
        if notesfile.exists():
            # notes file exists
            portdata += "\n"+notesfile.read_bytes()
            notes = True
        ianafile = Path(f"{portdir}/iana.md")
        if ianafile.exists():
            # iana data exists
            portdata += "\n# IANA Data\n\n"+ianafile.read_bytes()
            ianadata = True
        if True not in (notes, ianadata):
            # die if there's no notes and data, that's weird.
            raise ValueError(f"No notes/ianadata for {protocol}/{port}")
        # check if we need to write to disk
        writefile = False
        portfile_ref = Path(portfile)
        if portfile_ref.exists():
            if portdata != portfile_ref.read_bytes():
                writefile = True
        else:
            writefile = True
        if writefile:
            portfile_ref.write_bytes(portdata)


for proto in PROTOCOLS:
    proto_output_dir = Path(f"{OUTPUT_DIR}/{proto}")
    protodatadir = Path(f"{DATADIR}/{proto}")
    # die if can't find protocol data, probably something going horribly wrong
    if not protodatadir.exists():
        raise FileNotFoundError(f"Can't find protocol data dir for '{proto}'")
    # did you nuke the output dir? let's create it.
    if not proto_output_dir.exists():
        #os.mkdir(proto_output_dir)
        proto_output_dir.mkdir()
        print("Created protocol directory")
    print((f"Processing {proto}"))
    # do all the ports!
    with Pool(processes=NUM_PROCESSES) as pool:
        inputdata = [(proto, port) for port in os.listdir(protodatadir.as_posix())]
        for i in pool.imap_unordered(do_content, inputdata):
            pass

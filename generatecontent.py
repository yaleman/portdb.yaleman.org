#!/usr/local/bin/python3


import os
import sys
from multiprocessing import Pool

DATADIR = "data"
OUTPUT_DIR = "content"

PROTOCOLS = [ 'tcp', 'udp' ]
NUM_PROCESSES = 4

POST_TEMPLATE = """+++
title = "{protocol}/{port}"
tags = [ "{protocol}" ]
categories = [ "{protocol}" ]
+++
"""

def do_content(inputdata):
    """ takes a protocol and port tuple and does the processing for that combination """

    protocol, port = inputdata
    portdir = "{}/{}/{}".format(DATADIR, protocol, port)
    portfile = "{}/{}/{}.md".format(OUTPUT_DIR, protocol, port)
    if os.path.isdir(portdir):
        info = {'protocol' : protocol.upper(), 'port' : port}
        # base template
        portdata = POST_TEMPLATE.format(**info)
        notes = ianadata = False
        if os.path.exists("{}/notes.md".format(portdir)):
            # notes file exists
            portdata += "\n"+open("{}/notes.md".format(portdir), 'r').read()
            notes = True
        if os.path.exists("{}/iana.md".format(portdir)):
            # iana data exists
            portdata += "\n# IANA Data\n\n"+open("{}/iana.md".format(portdir)).read()
            ianadata = True
        if True not in (notes, ianadata):
            # die if there's no notes and data, that's weird.
            sys.exit("No notes/ianadata for {}/{}".format(protocol, port))
        # check if we need to write to disk
        writefile = False
        if os.path.exists(portfile):
            if portdata != open(portfile, 'r').read():
                writefile = True
        else:
            writefile = True
        if writefile:
            with open(portfile, 'w') as file_handle:
                file_handle.write(portdata)


for proto in PROTOCOLS:
    proto_output_dir = "{}/{}".format(OUTPUT_DIR, proto)
    protodatadir = "{}/{}".format(DATADIR, proto)
    # die if can't find protocol data, probably something going horribly wrong
    if not os.path.exists(protodatadir):
        sys.exit("Can't find protocol data dir for '{}'".format(proto))
    # did you nuke the output dir? let's create it.
    if not os.path.exists(proto_output_dir):
        os.mkdir(proto_output_dir)
        print("Created protocol directory")
    print("Processing {}".format(proto))
    # do all the ports!
    with Pool(processes=NUM_PROCESSES) as pool:
        inputdata = [(proto, port) for port in os.listdir(protodatadir)]
        for i in pool.imap_unordered(do_content, inputdata):
            pass


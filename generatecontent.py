#!/usr/bin/env python

""" content generator """

import asyncio
from datetime import datetime
import json
import os
from pathlib import Path

TODAY = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

DATADIR = "./data"
OUTPUT_DIR = "content"

PROTOCOLS = [ 'tcp', 'udp' ]
NUM_PROCESSES = 4

SEARCHFILE = Path("./themes/Just-Read/static/searchdata.json")


POST_TEMPLATE = """title: {port}
category: {protocol}
date: {TODAY}
slug: {protocol}/{port}

[portdb](/) / [{protocol}](/category/{protocol}.html) / {port}

"""

ALLDATA = []

async def do_content(protocol, port, show: bool):
    """ takes a protocol and port tuple and does the processing for that combination """

    portdir = f"{DATADIR}/{protocol}/{port}"
    portfile = f"{OUTPUT_DIR}/{protocol}/{port}.md"
    if os.path.isdir(portdir):
        info = {'protocol' : protocol, 'port' : port, "TODAY" : TODAY }
        # base template
        portdata = POST_TEMPLATE.format(**info)
        notes = ianadata = False
        notesfile = Path(f"{portdir}/notes.md").resolve()
        if notesfile.exists():
            # notes file exists
            portdata += f"\n{notesfile.read_text(encoding='utf8')}"
            if show:
                print(f"Notes for {protocol}/{port}:\n{notesfile.read_text(encoding='utf8')}")
            notes = True
        elif show:
            print(f"Notes file {notesfile} not found")
        ianafile = Path(f"{portdir}/iana.md")
        if ianafile.exists():
            # iana data exists
            portdata += f"\n## IANA Data\n\n{ianafile.read_text(encoding='utf8')}"
            ianadata = True
        if True not in (notes, ianadata):
            # die if there's no notes and data, that's weird.
            print(f"No notes/ianadata for {protocol}/{port}")
            return False
        # check if we need to write to disk
        writefile = False
        portfile_ref = Path(portfile)
        if portfile_ref.exists():
            if portdata != portfile_ref.read_text(encoding='utf8'):
                writefile = True
        else:
            writefile = True
        if writefile:
            portfile_ref.write_text(portdata, encoding="utf8")

        ALLDATA.append(f"{protocol}/{port}")


async def main():
    """ main func """
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

        show = False
        for port in os.listdir(protodatadir.as_posix()):
            await do_content(proto, port, show=show)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

SEARCHFILE.write_text(json.dumps(ALLDATA), encoding="utf8")

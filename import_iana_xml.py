#!/usr/bin/python

# pylint: disable=invalid-name


"""
takes the iana port numbers xml file and exports it as need be
last updated 2016-07-30 JH

TODO: needs a serious clean-up

"""


import os
from pathlib import Path
from typing import Any, Dict, Optional
import re
import sys

import requests

FILENAME = Path("service-names-port-numbers.xml").resolve()

if not FILENAME.exists():
    print(f"Can't find {FILENAME.as_posix()}, trying to download it.")
    try:

        filecontent = requests.get(
            "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml", # pylint: disable=line-too-long
            timeout=30,
            )
        filecontent.raise_for_status()
    # pylint: disable=broad-except
    except Exception as error:
        print(f"Failed to grab XML: {error}")
        sys.exit(1)
    FILENAME.write_bytes(filecontent.content)

data = FILENAME.read_text(encoding="utf8")

find_records = re.compile( r"(?P<record><record[^>]*>(.*?)</record>)", re.DOTALL )

def writefile( filetowrite, contents ):
    """ open and write a file """

    with Path(filetowrite).open('w', encoding="utf8" ) as file_hanlde:
        file_hanlde.write( contents )

def mkservicedir( servicedata ):
    """ generate a service dir """
    return f"data/{servicedata['protocol']}/{servicedata['port'] }/"

def ianafilename( iana_service ):
    """ generate an iana service filename """
    return f"{mkservicedir( iana_service )}iana.md"

def buildmd( servicedata ):
    """ generate a markdown file """
    markdown = f"_Name:_ {service['name']}\n\n"
    if servicedata['description'] is not None :
        markdown += f"_Description:_ {servicedata['description']}\n\n"
    if servicedata['note'] is not None:
        markdown += f"_Note:_ {servicedata['note']}\n\n"

    return markdown

re_name = re.compile( r"<name>(.*?)</name>", re.DOTALL )
protocol_searcher = re.compile( r"<protocol>(.*?)</protocol>", re.DOTALL )
description_searcher = re.compile( r"<description>(.*?)</description>", re.DOTALL )
number_searcher = re.compile( r"<number>(.*?)</number>", re.DOTALL )
note_searcher = re.compile( r"<note>(.*?)</note>", re.DOTALL )
info: Dict[str, Any] = {}

for record_found in find_records.finditer( data ):
    groupdict = record_found.groupdict()
    if "record" not in groupdict:
        continue
    record = groupdict["record"]
    # make sure port and protocol are at least defined, ignore unassigned ports
    if "<number" in record and "<protocol" in record and "<description>Unass" not in record.lower():
        namesearch = re_name.search( record )

        if namesearch is not None:
            psearch = protocol_searcher.search( record )
            protocol = None
            if psearch is not None:
                protocol = str(psearch.group( 1 ))

            dsearch = description_searcher.search( record )
            description = None
            if dsearch is not None:
                description = str(dsearch.group( 1 ))

            note: Optional[str] = None
            noteresult = note_searcher.search( record )
            if noteresult is not None:
                note = noteresult.group( 1 )

            numbersearch = number_searcher.search( record )
            number_data = None
            if numbersearch is not None:
                number_data = numbersearch.group( 1 )

            # add the service data to the stored list of services
            info[ f"{protocol}/{number_data}"] = {
                'name' : str(namesearch.group( 1 )),
                'protocol' : protocol,
                'description' : description,
                'note' : note,
                'port' : number_data,
            }



updated = 0
noupdate = 0
ignored = 0
services: Dict[str, Any] = {}
ignored_services = []
# check you're running from the right directory
if os.path.exists( "data/" ):
    print( "Data directory exists, starting to process.")
    for _, service in info.items():

        # pull the service info
        # service = info[item]

        if os.path.exists( mkservicedir( service )):
            # where we'll store the iana info
            ianafile = Path(ianafilename( service ))
            md = buildmd( service )

            if ianafile.exists():
                # if the ianafile already exists, check if it's the same as what we're trying to add
                ianafile_contents = ianafile.read_bytes()
                if ianafile_contents == md:
                    noupdate += 1
                # if the data's different, write it out
                else:
                    writefile( ianafile, md )
                    updated += 1
            else:
                writefile( ianafile, md )
                updated += 1
        else:
            ignored += 1
            if (service['protocol'] in ['tcp', 'udp']) and ("-" not in service.get('port', "")):
                ignored_services.append( {
                    'protocol' : service['protocol'],
                    'port' : service['port'],
                    'name': service['name'],
                    'description' : service['description'],
                    'note' : service['note'],
                } )
print(f"Updated: {updated}/{updated + noupdate}")
print(f"Ignored: {ignored}")

if updated == 0 and len( ignored_services ) > 0:

    while len( ignored_services ) > 0:
        service = ignored_services.pop()
        servicedir = Path(mkservicedir(service))
        if not servicedir.exists():
            servicedir.mkdir()
        writefile( ianafilename( service ), buildmd( service ) )
        print(f"Added {servicedir.as_posix()}")

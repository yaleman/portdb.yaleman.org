#!/usr/bin/python

import os
import sys


datadir = "data"
outputdir = "content"

protocols = [ 'tcp', 'udp' ]


post_template = """+++
title = "{protocol}/{port}"
tags = [ "{protocol}" ]
categories = [ "{protocol}" ]
+++
"""

for protocol in protocols:
    proto_output_dir = "{}/{}".format(outputdir, protocol)
    protodatadir = "{}/{}".format( datadir, protocol )
    # die if can't find protocol data, probably something going horribly wrong
    if os.path.exists( protodatadir ) == False: 
        sys.exit( "Can't find protocol data dir for '{}'".format( protocol ))        
    # did you nuke the output dir? let's create it.
    if os.path.exists( proto_output_dir ) == False:
        os.mkdir( proto_output_dir)
        print( "Created protocol directory" )
    print( "Processing {}".format( protocol  ) )
    # do all the ports!
    for port in os.listdir( protodatadir ):
        portdir = "{}/{}/{}".format( datadir, protocol, port )
        portfile = "{}/{}.md".format( proto_output_dir, port )
        if os.path.isdir( portdir ):
            info = { 'protocol' : protocol.upper(), 'port' : port }
            # base template
            portdata = post_template.format( **info )
            notes = ianadata = False
            if os.path.exists( "{}/notes.md".format( portdir ) ):
                # notes file exists
                portdata += "\n"+open( "{}/notes.md".format( portdir ), 'r' ).read()
                notes = True
            if os.path.exists( "{}/iana.md".format( portdir ) ):
                # iana data exists
                portdata += "\n# IANA Data\n\n"+open( "{}/iana.md".format( portdir ) ).read()
                ianadata = True
            if notes + ianadata == False:
                # die if there's no notes and data, that's weird.
                sys.exit( "No notes/ianadata for {}/{}".format( protocol, port ) )
            # check if we need to write to disk
            writefile = False
            if os.path.exists( portfile ):
                if portdata != open(portfile, 'r').read():
                    writefile = True
            else:
                writefile = True
            if writefile:
                fh = open( portfile, 'w' )
                fh.write( portdata )
                fh.close()
            


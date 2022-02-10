""" publish-time configuration

This file is only used if you use `make publish` or
explicitly specify it as your config file.
"""

import os
import sys
sys.path.append(os.curdir)

#pylint: disable=wildcard-import,wrong-import-position,unused-wildcard-import
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://portdb.yaleman.org'
RELATIVE_URLS = True

# FEED_ALL_ATOM = 'feeds/all.atom.xml'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
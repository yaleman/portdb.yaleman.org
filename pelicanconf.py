""" pelican config """

AUTHOR = 'James Hodgkinson'
SITENAME = 'portDB'
SITEURL = 'https://portdb.yaleman.org'

PATH = 'content'

TIMEZONE = 'Australia/Brisbane'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "themes/Just-Read"
# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
        #  ('Python.org', 'https://www.python.org/'),
        #  ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
        #  ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
        #   ('Another social link', '#'),)
LOAD_CONTENT_CACHE = False
DEFAULT_PAGINATION = 50

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{category}/{slug}/'
PAGE_SAVE_AS = '{category}/{slug}/index.html'

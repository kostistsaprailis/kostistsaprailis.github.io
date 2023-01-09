# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

AUTHOR = 'Kostis Tsaprailis'
SITENAME = 'Kostis Tsaprailis'

PATH = 'content'

TIMEZONE = 'Europe/Athens'

DEFAULT_LANG = 'en'

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://tsaprailis.com'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
SOCIAL = (('twitter', 'https://twitter.com/ktsaprailis'),
          ('github', 'https://github.com/kostistsaprailis/'),
          ('linkedin', 'https://www.linkedin.com/in/konstantinostsaprailis/'))

DEFAULT_PAGINATION = 10
FILENAME_METADATA = '(?P<title>.*)'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html/'
SITELOGO = '/images/profile.png'
FAVICON = '/images/favicon.ico'
SITESUBTITLE = 'Full Stack Breaker'
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
# THEME = 'themes/Peli-Kiera'
THEME = 'themes/Flex'
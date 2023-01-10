AUTHOR = 'Kostis Tsaprailis'
SITENAME = 'Kostis Tsaprailis'
SITEURL = 'https://tsaprailis.com'

PATH = 'content'

TIMEZONE = 'Europe/Athens'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('You can modify those links in your config file', '#'),)

# Social widget
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
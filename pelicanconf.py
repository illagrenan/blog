#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys

sys.path.append('.')

AUTHOR = 'Vašek Dohnal'
SITENAME = 'Vašek Dohnal &mdash; blog'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Prague'

DEFAULT_LANG = 'cs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
THEME = 'vd-theme'

AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
TAG_SAVE_AS = ''
DIRECT_TEMPLATES = ['index']

# ==============================

# Static files
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/humans.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

# JINJA_FILTERS = {'linkpeek': xtypo}
TYPOGRIFY = True
DISQUS_SITENAME = "vaekdohnalblog"

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', ]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

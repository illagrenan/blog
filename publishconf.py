#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)

# noinspection PyUnresolvedReferences
from pelicanconf import *

SITEURL = os.getenv('PELICAN_SITEURL', 'https://blog.vaclavdohnal.cz')
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "vaekdohnalblog"
GOOGLE_ANALYTICS = "UA-30490552-13"

ARTICLE_URL = 'posts/{slug}'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = 'pages/{slug}'
PAGE_SAVE_AS = 'pages/{slug}.html'
# AUTHOR_URL = 'author/{slug}/'
# AUTHOR_SAVE_AS = 'author/{slug}.html'
# CATEGORY_URL = 'category/{slug}'
# CATEGORY_SAVE_AS = 'category/{slug}.html'
# TAG_URL = 'tag/{slug}'
# TAG_SAVE_AS = 'tag/{slug}.html'

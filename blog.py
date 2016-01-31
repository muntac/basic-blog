import os
import cgi
import hmac
import json
import time
import pickle
import random
import hashlib
import logging
from string import letters
import jinja2
import webapp2
from google.appengine.ext import db
#from google.appengine.api import memcache

from handlers.BaseHandler import BaseHandler
from handlers.Post import NewPost, PostPage
from handlers.Home import HomePage, BlogPage
from handlers.UserAccount import SignUp, LogIn, LogOut
from handlers.Json import JsonBlogPage, JsonPostPage
from handlers.cacheflush import Flush

DEBUG = bool(os.environ['SERVER_SOFTWARE'].startswith('Development'))
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)

app = webapp2.WSGIApplication([(r'/blog/', HomePage),
                               (r'/blog', HomePage),
                               (r'/blog/welcome', HomePage),
                               (r'/', HomePage),
                               (r'/blog/signup', SignUp),
                               (r'/blog/login', LogIn),
                               (r'/blog/logout', LogOut),
                               (r'/blog/home', BlogPage),
                               (r'/blog/newpost', NewPost),
                               (r'/blog/([0-9]+)', PostPage),
                               (r'/blog/.json', JsonBlogPage),
                               (r'/blog/([0-9]+).json', JsonPostPage),
                               (r'/blog/flush', Flush),
                               ],
                              debug = True)

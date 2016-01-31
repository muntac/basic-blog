import webapp2
from BaseHandler import BaseHandler
from google.appengine.api import memcache

class Flush(BaseHandler):
    def get(self):
        memcache.flush_all()


import webapp2
import time
from google.appengine.ext import db
from BaseHandler import BaseHandler
from google.appengine.api import memcache
from db.BlogPost import BlogPost

#Handler Class: Home page
class HomePage(BaseHandler):
    def get(self):
        if self.user:
            #self.write("Welcome, " + self.user.username + "!")
            self.redirect('/blog/home')
        else:
            self.redirect('/blog/login')
        #res = db.GqlQuery("select * from BlogPost order by creationtime desc limit 10")
        #self.render("home.html", posts = res)

class BlogPage(BaseHandler):
    def get(self):
        ls = []
        timelast = 0
        #memcache.flush_all()
        if memcache.get("home") is None:
            res = db.GqlQuery("select * from BlogPost order by creationtime desc limit 10")
            for post in res:
                ls.append( (post.subject, post.content, post.creationtime) )
            memcache.set("home", (ls,time.time()))
        else:
            cacheval = memcache.get("home")
            ls = cacheval[0]
            timelast = time.time() - cacheval[1]
        lspost = []
        for x in ls:
            lspost.append(BlogPost(subject = x[0], content = x[1], creationtime = x[2]))
        self.render("home.html", posts = lspost, lasttime = timelast)


import webapp2
import time
from BaseHandler import BaseHandler
from google.appengine.api import memcache
from db.BlogPost import BlogPost

#Handler Class: Post Page
class PostPage(BaseHandler):
    def get(self, post_id):
        mempost = memcache.get(post_id)
        last_queried = 0
        if mempost is None:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                self.error(404)
                return
            memcache.set(post_id,( (post.subject,post.content,post.creationtime), time.time() ) )
        else:
            last_queried = time.time() - mempost[1]
            post = BlogPost(subject = mempost[0][0], content = mempost[0][1], creationtime = mempost[0][2])
        self.render("permalink.html", post = post, lasttime = last_queried)

#Handler Class: New post
class NewPost(BaseHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        #Enter blog post in database
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            a = BlogPost(subject = subject, content = content)
            keyblog = a.put()
            memcache.set("home",None)
            self.redirect("/blog/" + str(keyblog.id()) )
        else:
            error = "Post must have BOTH a subject and a content"
            self.render(subject = subject, content = content, error = error)

import webapp2
from BaseHandler import BaseHandler
from google.appengine.api import memcache

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


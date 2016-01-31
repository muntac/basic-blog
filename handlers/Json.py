import webapp2
from BaseHandler import BaseHandler

class JsonBlogPage(BaseHandler):
    def get(self):
        res = db.GqlQuery("select * from BlogPost order by creationtime desc limit 10")
        ls = []
        for post in res:
            ls.append({"content": post.content, "created": post.creationtime.strftime("%b %d %Y"), "last_modified": post.creationtime.strftime("%b %d %Y"), "subject": post.subject})
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json.dumps(ls))
            
class JsonPostPage(BaseHandler):
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        if not post:
            self.error(404)
            return
        jsdict = {"content": post.content, "created": post.creationtime.strftime("%b %d %Y"), "last_modified": post.creationtime.strftime("%b %d %Y"), "subject": post.subject}
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json.dumps(jsdict))


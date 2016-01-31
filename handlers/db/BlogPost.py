from google.appengine.ext import db
import webapp2
import jinja2
import os

#DataStore Entity: BlogPost
class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    creationtime = db.DateTimeProperty(auto_now_add = True)
    #Path variables/jinja initialization
    current_path = os.path.dirname(__file__)
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
    parent_parent_path = os.path.abspath(os.path.join(parent_path, os.pardir))
    ancestor_dir = os.path.join(parent_parent_path, 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(ancestor_dir), autoescape = True)
    
    def render_str(self, template, **params):
        t = self.jinja_env.get_template(template)
        return t.render(params)

    def render(self):#Formatting the user's input
        self._render_text = self.content.replace('\n', '<br>')
        return self.render_str("post.html", p = self)


import webapp2
import jinja2
import os
from db.User import User
from utils.validation import validation

class BaseHandler(webapp2.RequestHandler):
    #Path variables/jinja initialization
    current_path = os.path.dirname(__file__)
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))    
    parent_dir = os.path.join(parent_path, 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(parent_dir), autoescape = True)

    def write(self, *a, **kw):#shortcut for self.response.write
        self.response.write(*a, **kw)

    def render_str(self, template, **kw):#Uses Jinja render() to render template and return it as a unicode string
        jinja_tempobj = self.jinja_env.get_template(template) #loads template from the environment
        return jinja_tempobj.render(kw)

    def render(self, template, **kw):#Simply calls write on the Jinja template string
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = validation.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return validation.check_secure_val(cookie_val)

    def login(self, userobj):
        self.set_secure_cookie('user_id', str(userobj.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        #if there are other user related cookies those need to be deleted too
    
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        if uid:
            self.user = User.get_by_id(int(uid))
        else:
            self.user = None


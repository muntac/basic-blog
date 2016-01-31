from google.appengine.ext import db
import sys
sys.path.insert(0, '/home/muntac/GoogleApps/wiki/handlers')
from utils.validation import validation


#DataStore Entity: User
class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_name(cls, uname):
        usr = cls.all().filter('name =', uname).get()
        return usr

    @classmethod
    def register(cls, reg_username, reg_password, reg_email):
        hashed_pwd = validation.hash_password(reg_username, reg_password)
        usr = User(username = reg_username, password = hashed_pwd, email = reg_email)
        usr.put()
        return usr


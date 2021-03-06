import webapp2
from db.User import User
#from google.appengine.ext import db
from utils.validation import validation
from BaseHandler import BaseHandler
from google.appengine.api import memcache

#Handler Class: SignUp
class SignUp(BaseHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        params = dict(username = username, email = email)
        error_flag = False

        if validation.valid_username(username) is None:
            params['error_username'] = "Invalid username"
            error_flag = True
        else:
            if User.by_name(username) is not None:
                params['error_username'] = "Invalid username"
                error_flag = True
        if validation.valid_password(password) is None:
            params['error_password'] = "Invalid password"
            error_flag = True
        elif password != verify:
            params['error_verify'] = "Passwords don't match"
            error_flag = True
        if validation.valid_email(email) is None:
            params['error_email'] = "Email is invalid"
            error_flag = True
        if error_flag:
            self.render("signup.html", **params)
        else:
            usrobj = User.register(username, password, email)
            self.login(usrobj)
            self.redirect('/blog/')

#Handler Class: LogIn
class LogIn(BaseHandler):
    def get(self):
        if not self.user:
            self.render("login.html")
        else:
            self.redirect('home')
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        params = dict(username=username)
        error_flag = False

        if username == "":
            params['error_username'] = "Username cannot be empty"
            error_flag = True
        if password == "":
            params['error_password'] = "Password cannot be empty"
            error_flag = True

        if error_flag:
            self.render("login.html", **params)
        else:
            usr_details = User.all().filter('username =', username).get()
            if (usr_details is not None) and (validation.hash_password(username, password, usr_details.password.split(",")[0]) == usr_details.password):
                self.login(usr_details)
                self.redirect('/')
            else:
                self.render("login.html", username=username, error_validation="Invalid login details")
                
class LogOut(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('signup')


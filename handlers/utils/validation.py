import re
import random
import hmac
import hashlib
from string import letters

#Validation Class
class validation:
    USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    PASS_RE = re.compile(r'^.{3,20}$')
    EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')    
    secret = 'peskapolowitz'

    @classmethod
    def valid_username(cls, username):
        if username and cls.USER_RE.match(username):
            return username

    @classmethod
    def valid_password(cls, password):
        return password and cls.PASS_RE.match(password)

    @classmethod
    def valid_email(cls, email):
        return not email or cls.EMAIL_RE.match(email)

    @classmethod
    def get_salt(cls, length = 5):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def hash_password(cls, username, password, salt=None):
        if salt is None:
            salt = cls.get_salt()
        hashed_pwd = hashlib.sha256(username + password + salt).hexdigest()
        return '%s,%s' % (salt, hashed_pwd)

    @classmethod
    def make_secure_val(cls, val):
        secure_val = hmac.new(cls.secret, val).hexdigest()
        return '%s|%s' % (val, secure_val)

    @classmethod
    def check_secure_val(cls, read_val):
        read_val_front = read_val.split('|')[0]
        new_val = cls.make_secure_val(read_val_front)
        if new_val == read_val:
            return read_val_front


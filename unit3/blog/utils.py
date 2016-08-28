
import re
import hashlib
import hmac
import random
import string


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)


PW_RE = re.compile(r"^.{3,20}$")
def valid_password(pw):
    return PW_RE.match(pw)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)


SECRET = 'Setec Astronomy - Too Many Secters'
def make_secure_val(s):
    return "%s|%s" % (s, hmac.new(SECRET, s).hexdigest())


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


def make_pw_hash(name, pw, salt=None):
    if salt == None:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split(",")[1]
    return make_pw_hash(name, pw, salt) == h


def make_salt(length=8):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])
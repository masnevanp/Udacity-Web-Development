#!/usr/bin/env python

import webapp2
import re
from collections import defaultdict

form = """
<!DOCTYPE html>
<html>
<body>

<h2>Signup (yes yes... messy form....)</h1>

<form method="post">
    <label>Username</label>
    <input type="text" name="username" value="%(username)s">
    <label style="color: red">%(username_err)s</label>
    <br>
    
    <label>Password</label>
    <input type="password" name="password" value="">
    <label style="color: red">%(password_err)s</label>
    <br>
    
    <label>Verify Password</label>
    <input type="password" name="verify" value="">
    <label style="color: red">%(verify_err)s</label>
    <br>
    
    <label>Email (optional)</label>
    <input type="text" name="email" value="%(email)s">
    <label style="color: red">%(email_err)s</label>
    <br>
    
	<input type="submit">
</form>

</body>
</html>
"""

            
class SignUp(webapp2.RequestHandler):
    def write_form(self, params=defaultdict(str)):
        self.response.out.write(form % params)
        
    def get(self):
        self.write_form()
	
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        params = defaultdict(str)
        params['username'] = username
        params['email'] = email
        
        valid = True
        
        if not valid_username(username):
            params['username_err'] = "That's not a valid username."
            valid = False
        
        if not valid_password(password):
            params['password_err'] = "That wasn't a valid password."
            valid = False
        elif password != verify:
            params['verify_err'] = "Your passwords didn't match."
            valid = False
        
        if email and not valid_email(email):
            params['email_err'] = "That's not a valid email."
            valid = False
        
        if valid:
            self.redirect("/unit2/welcome?username=" + username)
        else:
            self.write_form(params)

class Welcome(webapp2.RequestHandler):
    def get(self):
        welcome = """
            <div style="color: blue"><b>Welcome, %s!</b></div>
        """
        user = self.request.get('username')
        if valid_username(user):
            self.response.out.write(welcome % user)
        else:
            self.redirect("/unit2/signup")


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(pw):
    return PW_RE.match(pw)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)
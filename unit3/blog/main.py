#!/usr/bin/env python

import os

import webapp2
import jinja2
from google.appengine.ext import db

from collections import defaultdict

import utils


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=True)


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        t = jinja_env.get_template('blogpost.html')
        return t.render(blogpost=self)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class FrontPage(Handler):
    def get(self):
        blogposts = db.GqlQuery(
            "SELECT * FROM BlogPost ORDER BY created DESC LIMIT 10")
        self.render("front.html", blogposts=blogposts)


class NewPost(Handler):
    def render_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_form()

    def post(self):
        subj = self.request.get("subject")
        cont = self.request.get("content")

        if subj and cont:
            post_id = BlogPost(subject=subj, content=cont).put().id()
            self.redirect("/unit3/blog/" + str(post_id))
        else:
            err = "subject and content, please!"
            self.render_form(subj, cont, err)


class PermaLink(Handler):
    def get(self, link_id):
        blogpost = BlogPost.get_by_id(int(link_id))
        if blogpost:
            self.render("perma.html", blogpost=blogpost)
        else:
            self.render("perma_404.html")


class SignUp(Handler):
    def render_form(self, params=defaultdict(str)):
        self.render("signup.html", **params)

    def get(self):
        self.render_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = defaultdict(str)
        params['username'] = username
        params['email'] = email

        valid = True

        if not utils.valid_username(username):
            params['username_err'] = "That's not a valid username."
            valid = False

        if not utils.valid_password(password):
            params['password_err'] = "That wasn't a valid password."
            valid = False
        elif password != verify:
            params['verify_err'] = "Your passwords didn't match."
            valid = False

        if email and not utils.valid_email(email):
            params['email_err'] = "That's not a valid email."
            valid = False

        if valid:
            user_cookie = 'user=%s; Path=/' % utils.make_secure_val(username)
            self.response.headers.add_header('Set-Cookie', str(user_cookie))
            self.redirect("/unit3/blog/welcome")
        else:
            self.render_form(params)


class Welcome(Handler):
    def get(self):
        user = None
        user_cookie = self.request.cookies.get('user')
        if user_cookie:
            user = utils.check_secure_val(user_cookie)
        
        if user:
            self.write("Welcome, %s!" % user)
        else:
            self.redirect("/unit3/blog/signup")
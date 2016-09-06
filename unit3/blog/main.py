#!/usr/bin/env python

import os

import webapp2
import jinja2
from google.appengine.api import memcache
from google.appengine.ext import ndb

from collections import defaultdict
from collections import OrderedDict
import json
import time
import logging

import utils


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=True)


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=False)
    
    @staticmethod
    def add_user(name, hash, email=""):
        User(name=name, hash=hash, email=email).put()
    
    @staticmethod
    def user_exists(username):
        return User.query(User.name == username).get() != None
    
    @staticmethod
    def valid_user(username, password):
        if username and password:
            user = User.query(User.name == username).get()
            return user and utils.valid_pw(username, password, user.hash)


class BlogPost(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    def render(self):
        t = jinja_env.get_template('blogpost.html')
        return t.render(blogpost=self)
    
    def to_dict(self):
        return OrderedDict([
            ("subject", self.subject),
            ("content", self.content),
            ("created", self.created.strftime("%a %b %d %X %Y"))
        ])
    
    @staticmethod
    def store_post(subject, content):
        post_id = BlogPost(subject=subject, content=content).put().id()
        BlogPost.get_latest(update=True)
        return post_id

    @staticmethod
    def get_post(id):
        return BlogPost.get_by_id(int(id))
    
    @staticmethod
    def get_latest(update=False, count=10):
        key = 'latest_posts'

        if not update:
            val = memcache.get(key)
            if val:
                (posts, cached_count, qry_time) = val
                if cached_count != count:
                    # ISSUE: Unnecessary update when cached_count > count
                    update = True
            else:
                update = True
        
        if update:
            posts = BlogPost.query().order(-BlogPost.created).fetch(count)
            qry_time = time.time()
            memcache.set(key, (posts, count, qry_time))
        
        return (posts, qry_time)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.cur_user = self.get_cookie('username')
        #username = self.read_secure_cookie('user')
        #self.user = uid and User.by_id(int(uid))
    
    def set_cookie(self, name, val):
        cookie = str('%s=%s; Path=/' % (name, utils.make_secure_val(val)))
        self.response.headers.add_header('Set-Cookie', cookie)
    
    def get_cookie(self, name):
        cookie = self.request.cookies.get(name)
        if cookie:
            return utils.check_secure_val(cookie)
         
    def login(self, username):
        self.set_cookie('username', username)
        self.redirect('/unit3/blog/welcome')

    def logout(self):
        self.set_cookie('username', '')
        self.redirect('/unit3/blog/signup')
    

class FrontPage(Handler):
    def get(self):
        (posts, qry_time) = BlogPost.get_latest()
        query_age = int(round(time.time() - qry_time));
        self.render("front.html", blogposts=posts, query_age=query_age)


class FrontPageJson(Handler):
    def get(self):
        (posts, _) = BlogPost.get_latest();
        json_txt = json.dumps([bp.to_dict() for bp in posts])
        self.response.headers['content-type'] = "application/json; charset=UTF-8"
        self.write(json_txt)


class NewPost(Handler):
    def render_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_form()

    def post(self):
        subj = self.request.get("subject")
        cont = self.request.get("content")

        if subj and cont:
            post_id = BlogPost.store_post(subj, cont)
            self.redirect("/unit3/blog/" + str(post_id))
        else:
            err = "subject and content, please!"
            self.render_form(subj, cont, err)


class PermaLink(Handler):
    def get(self, id):
        blogpost = BlogPost.get_post(id)
        if blogpost:
            self.render("perma.html", blogpost=blogpost)
        else:
            self.response.set_status(404)
            self.render("perma_404.html")


class PermaLinkJson(Handler):
    def get(self, id):
        blogpost = BlogPost.get_post(id)
        if blogpost:
            json_txt = json.dumps(blogpost.to_dict())
            self.response.headers['content-type'] = "application/json; charset=UTF-8"
            self.write(json_txt)
        else:
            self.response.set_status(404)
            self.write(json.dumps({"error": "unknown id"}))


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
        
        if User.user_exists(username):
            params['username_err'] = "User already exists."
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
            hash = utils.make_pw_hash(username, password)
            User.add_user(username, hash, email)
            self.login(username)
        else:
            self.render_form(params)


# TODO: User already logged in (redirect to 'welcome'?)
class Login(Handler):
    def render_form(self, login_err=""):
        self.render("login.html", login_err=login_err)

    def get(self):
        self.render_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        if User.valid_user(username, password):
            self.login(username)
        else:
            self.render_form(login_err="Invalid login.")


class Logout(Handler):
    def get(self):
        self.logout()


class Welcome(Handler):
    def get(self):
        if self.cur_user:
            self.render("welcome.html", username=self.cur_user)
        else:
            self.redirect("/unit3/blog/signup")
    

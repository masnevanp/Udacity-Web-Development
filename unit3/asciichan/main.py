#!/usr/bin/env python

import os
import time

import webapp2
import jinja2

from google.appengine.api import memcache
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def top_arts(update=False):
        key = 'top_arts'
        arts = memcache.get(key)
        if arts is None or update:
            arts = db.GqlQuery(
                "SELECT * FROM Art ORDER BY created DESC")
            arts = list(arts)
            memcache.set(key, arts)
        
        return arts



class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = Art.top_arts()
        self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)
            a.put()
            time.sleep(0.5)
            # Without the delay the newly added art will not show up when
            # we redirect below. There must be a better way, but this
            # will do for now...
            Art.top_arts(True)
            self.redirect("/unit3/asciichan")
        else:
            error = "We need both the title and the art!"
            self.render_front(title, art, error)

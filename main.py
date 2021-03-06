#!/usr/bin/env python

import os
import webapp2
import unit1.main
import unit2.rot13.main
import unit2.signup.main
import unit2a.main
import unit3.asciichan.main
import unit3.blog.main

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Development')

app = webapp2.WSGIApplication([
            ('/unit1', unit1.main.MainHandler),
            ('/unit2/rot13', unit2.rot13.main.MainPage),
            ("/unit2/signup", unit2.signup.main.SignUp),
            ("/unit2/welcome", unit2.signup.main.Welcome),
            ("/unit2a", unit2a.main.MainPage),
            ("/unit2a/fizzbuzz", unit2a.main.FizzBuzzHandler),
            ("/unit3/asciichan", unit3.asciichan.main.MainPage),
            ('/unit3/blog/?', unit3.blog.main.FrontPage),
            ('/unit3/blog/?\.json', unit3.blog.main.FrontPageJson),
            ('/unit3/blog/newpost', unit3.blog.main.NewPost),
            (r'/unit3/blog/([0-9]+)', unit3.blog.main.PermaLink),
            (r'/unit3/blog/([0-9]+)\.json', unit3.blog.main.PermaLinkJson),
            ('/unit3/blog/signup', unit3.blog.main.SignUp),
            ('/unit3/blog/login', unit3.blog.main.Login),
            ('/unit3/blog/logout', unit3.blog.main.Logout),
            ('/unit3/blog/welcome', unit3.blog.main.Welcome),
            ('/unit3/blog/flush', unit3.blog.main.FlushCache)
        ],
        debug=DEBUG)

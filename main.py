#!/usr/bin/env python

import webapp2
import unit1.main
import unit2.rot13.main
import unit2.signup.main
import unit2a.main
import unit3.asciichan.main
import unit3.blog.main

app = webapp2.WSGIApplication([
            ('/unit1', unit1.main.MainHandler),
            ('/unit2/rot13', unit2.rot13.main.MainPage),
            ("/unit2/signup", unit2.signup.main.SignUp),
            ("/unit2/welcome", unit2.signup.main.Welcome),
            ("/unit2a", unit2a.main.MainPage),
            ("/unit2a/fizzbuzz", unit2a.main.FizzBuzzHandler),
            ("/unit3/asciichan", unit3.asciichan.main.MainPage),
            ('/unit3/blog', unit3.blog.main.FrontPage),
            ('/unit3/blog/', unit3.blog.main.FrontPage),
            ('/unit3/blog/newpost', unit3.blog.main.NewPost),
            (r'/unit3/blog/([0-9]+)', unit3.blog.main.PermaLink),
            ('/unit3/blog/signup', unit3.blog.main.SignUp),
            ('/unit3/blog/welcome', unit3.blog.main.Welcome)
        ],
        debug=True)

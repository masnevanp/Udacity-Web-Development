#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
            ('/unit3/blog/newpost', unit3.blog.main.NewPost),
            (r'/unit3/blog/(\d+)', unit3.blog.main.PermaLink)
        ],
        debug=True)

#!/usr/bin/env python

import webapp2
import cgi
from rot13 import rot13

form = """
<!DOCTYPE html>
<html>
<body>

<h1>Enter some text to ROT13:</h1>

<form method="post">
    <textarea name="text" rows="10" cols="80">%(text)s</textarea>
    <br>
	<input type="submit">
</form>

</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {"text": text})
        
    def get(self):
        self.write_form()
	
    def post(self):
        user_text = self.request.get('text')
        self.write_form(cgi.escape(rot13(user_text), quote=True))

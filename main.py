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
import cgi
import re

head= """
<head>
    <title>Sign Up</title>
    <style type="text/css">
        .error {
            color: red;
        }

    </style>
</head>
<body>
    <h1>
        <a href="/">Sign Up</a>
    </h1>
"""

form = """
    <form method="post">
        <label>Username <input type="text" name="username" value="%(username)s" required /> <span class="error">%(username_error)s</span></label><br>
        <label>Password <input type="password" name="password" required /><span class="error">%(password_error)s</span></label><br>
        <label>Verify Password <input type="password" name="verify" required /><span class="error">%(verify_error)s</span></label><br>
        <label>Email (Optional) <input type="email" name="email" value="%(email)s" /><span class="error">%(email_error)s</span></label><br>
        <button type="submit">Sign Up!</button>
    </form>
    """

foot= """
    </body>
</html>
"""

def ver_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def ver_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)

def password_match(password, verify):
    return password == verify

def ver_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_page(self, username="", username_error="", password_error="", verify_error="", email="", email_error=""):
        response = head + form + foot
        self.response.out.write(response % {"username": cgi.escape(username, quote=True),
                                            "username_error": username_error,
                                            "password_error": password_error,
                                            "verify_error": verify_error,
                                            "email": cgi.escape(email, quote=True),
                                            "email_error": email_error})

    def get(self):
        self.write_page()

    def post(self):
        username = self.request.get("username")
        if not username:
            username_error = "Please enter a username"
        elif not ver_username(username):
            username_error = "That is not a valid username"
        else:
            username_error = ""

        password = self.request.get("password")
        if not password:
            password_error = "Please enter a password"
        elif not ver_password(password):
            password_error = "That is not a valid password"
        else:
            password_error = ""

        verify = self.request.get("verify")
        if not verify:
            verify_error = "Please verify your password"
        elif not password_match(password, verify):
            verify_error = "Your passwords do not match"
        else:
            verify_error = ""

        email = self.request.get("email")
        if not ver_email(email):
            email_error = "That is not a valid email"
        else:
            email_error = ""

        if not (username_error == "" and password_error == "" and verify_error == "" and email_error == ""):
            self.write_page(username, username_error, password_error, verify_error, email, email_error)
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome_element = """
            <h2>Welcome <strong>%(username)s</strong>!</h2>
            <p>Thank you for signing up. Enjoy!
            """

        content = head + welcome_element + foot

        self.response.out.write(content % {"username" : cgi.escape(username)})

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)

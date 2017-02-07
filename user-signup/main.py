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
import re
import cgi

USER_RE_username = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
USER_RE_password = re.compile(r"^.{3,20}$")
USER_RE_email = re.compile(r"^[\S]+@[\S]+.[\S]+$")

#error_user = "Username must have at least 3 characters and no spaces."
#error_pass = "bad password"
#error_check = "bad check"
#error_email = "bad email"

#body variable  is the HTML for the form
body = """<!DOCTYPE html><head><title>Sign Up</title><style>.error{color: red;}</style></head>
<body>
    <h1>User Signup</h1>
        <form method="post">
            <table>
                <tbody><tr>
                    <td><label for="username">Username</label></td>
                    <td><input name="username" type="text" value="%(username)s" required="">
                        <span class="error">%(error_user)s</color></span></td></tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td><input name="password" type="password" required="">
                        <span class="error">%(error_pass)s</span></td></tr>
                <tr>
                    <td><label for="check">Verify Password</label></td>
                    <td><input name="check" type="password" required="">
                        <span class="error">%(error_check)s</span></td></tr>
                <tr>
                <td><label for="email">Email (optional)</label></td>
                    <td><input name="email" type="email" value="%(email)s">
                        <span class="error">%(error_email)s</span></td></tr>
            </tbody></table>
            <input type="submit">
        </form></body>
        </html>"""

def valid_username(username):
    #USER_RE_username = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
#    if username and username.isalpha():
    if USER_RE_username.match(username):
        return username

def valid_password(password):
    #USER_RE_password = re.compile(r"^.{3,20}$")
    #if password == check:
        #return USER_RE.match(password, check)
    if USER_RE_password.match(password):
        return password

def valid_check(check):
    if check:
        return check

def valid_email(email):
    if not email:
        return ""
    if USER_RE_email.match(email):
        return email

#def valid_email(email):
#    USER_RE_email = re.compile(r"^[\S]+@[\S]+.[\S]+$")
#        return USER_RE_email.match(email)

def escape_html(s):
    return cgi.escape(s, quote=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        error_user = ""
        error_pass = ""
        error_check = ""
        error_email = ""
        username = ""
        email = ""
        self.response.out.write(body % {'username': username,'error_user': error_user, 'error_pass': error_pass, 'error_check': error_check, 'email': email, 'error_email': error_email})

    def post(self):
        error_user = ""
        error_pass = ""
        error_check = ""
        error_email = ""
        user_username = self.request.get('username')#username string is stored here, and can be sued again
        user_password = self.request.get('password')
        user_check = self.request.get('check')
        user_email = self.request.get('email')

        user_username_val = valid_username(user_username)#these are stored as true/false, sort of
        user_password_val = valid_password(user_password)
        user_check_val = valid_check(user_check)
        user_email_val = valid_email(user_email)

        if (user_username_val and (user_password_val == user_check) and (not user_email or user_email_val)):
            #if not user_username and user_password and check:
                self.redirect('/thanks?username=%s'% user_username)#% is string substitution
        else:
            if not user_username_val:
                error_user = "Username must have 3 to 20 characters and no spaces."
            if not user_password_val:
                error_pass = "Password must have 3 to 20 characters and no spaces."
            if not user_check == user_password:
                error_check = "Your passwords do not match."
            if user_email and not user_email_val:
                error_email = "Please enter a valid email address."
            self.response.out.write(body % {'username': user_username, 'error_user': error_user, 'error_pass': error_pass, 'error_check': error_check,'email': user_email,  'error_email': error_email})



class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        
        user_username = self.request.get('username')#new page needs new get request
        self.response.out.write("Welcome, %s" % user_username)#string substitution

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', ThanksHandler)
], debug=True)

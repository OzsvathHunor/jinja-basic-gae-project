#!/usr/bin/env python
#-*- coding: utf-8-*-

import os
import jinja2
import webapp2
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

fovarosok = {u"Horvátország":"Zágráb", u"Magyarország":"Budapest"}

class MainHandler(BaseHandler):
    def get(self):
        country = fovarosok.keys()[random.randint(0, 1)]
        return self.render_template("askforage.html", {"country": country})

    def post(self):
        country = self.request.get("country")
        guess = self.request.get("guess")
        if guess == fovarosok[country]:
            success = True
        else:
            success = False
        params = {"success": success}
        return self.render_template("hello.html", params)


class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog', BlogHandler),
], debug=True)


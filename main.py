#!/usr/bin/env python
import os
import jinja2
import webapp2


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


class MainHandler(BaseHandler):
    def get(self):
        #http://127.0.0.1:8080/?age=20
        age_str = self.request.get("age")
        if age_str == "":
            return self.render_template("askforage.html")
        else:
            age = int(age_str)
            drinks = {"wine", "beer", "whiskey"}
            params = {"age": age, "drinks": drinks}
            return self.render_template("hello.html", params)


class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog', BlogHandler),
], debug=True)

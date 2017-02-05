import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
	subject = db.StringProperty(required = True)
	body = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
		

	def get(self):
		self.render("blog.html")
	def post(self):
		subject = self.request.get("subject")
		body = self.request.get("body")

		if subject and body:
			a = Blog(subject = subject, body = body)
			a.put()

			self.redirect("/Content.html")
		else:
			error = "we need some text bro"
			self.render_front(subject, body, error)

class ContentHandler(Handler):
	def render_front(self, subject="", body="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
		self.render("Content.html", subject=subject, body=body, error=error, blogs=blogs)

	def get(self):
		self.render("Content.html")

	def post(self):
		if subject and body:
			


app = webapp2.WSGIApplication([('/', MainPage), ('/Content.html', ContentHandler)], debug=True)
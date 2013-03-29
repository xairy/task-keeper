import os
import cgi
import datetime

import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Task(db.Model):
    owner = db.UserProperty()
    caption = db.StringProperty()
    description = db.TextProperty()
    date = db.DateProperty(auto_now_add = True)

def tasks_key(user_name):
    return db.Key.from_path('Tasks', user_name)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_name = user.email()
            
            tasks = Task.all().ancestor(tasks_key(user_name)).order('date').order('caption')
            logout_url = users.create_logout_url(self.request.uri)

            template_values = {
                'tasks': tasks,
                'logout_url': logout_url,
                'user': user_name,
            }

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

class AddTaskHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_name = user.email()

            task = Task(parent=tasks_key(user_name))
            task.owner = user
            task.caption = cgi.escape(self.request.get('caption'))
            task.description = cgi.escape(self.request.get('description')).replace('\r\n', '<br>')
            try:
                task.date = datetime.datetime.strptime(self.request.get('date'), '%d.%m.%Y').date()
            except ValueError:
                task.date = datetime.datetime.today().date()
            task.put()

            self.redirect('/')
        
class RemoveTaskHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_name = user.email()
            
            if Task.all().ancestor(tasks_key(user_name)).filter('author =', user).count() > 0:
                key = self.request.get('id')
                task = db.delete(key)

            self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add-task', AddTaskHandler),
    ('/remove-task', RemoveTaskHandler),
], debug = True)

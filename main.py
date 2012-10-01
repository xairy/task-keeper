import os
import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

# TODO: make it possible to edit entries.
# TODO: add multiple tables.

# POINT: think about focus.
# POINT: think about ancestor conception in the datastore.
# POINT: Missed (red), Today (orange), Tomorrow (green), Planned (green), Done (blue), Whenever-you-get-a-chance (grey)

class Task(db.Model):
    author = db.UserProperty()
    caption = db.StringProperty(multiline = True)
    description = db.TextProperty()
    date = db.DateProperty(auto_now_add = True)

def tasks_key(user_name):
    return db.Key.from_path('Tasks', user_name)

class MainPage(webapp.RequestHandler):
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

            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, template_values))

class AddTaskHandler(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_name = user.email()

            task = Task(parent = tasks_key(user_name))
            task.author = user
            task.caption = self.request.get('caption')
            task.description = self.request.get('description').replace('\r\n', '<br>')
            try:
                task.date = datetime.datetime.strptime(self.request.get('date'), '%d.%m.%Y').date()
            except ValueError:
                task.date = datetime.datetime.today().date()
            task.put()

            self.redirect('/')
        
class RemoveTaskHandler(webapp.RequestHandler):
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

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/add-task', AddTaskHandler),
    ('/remove-task', RemoveTaskHandler),
], debug = True);

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

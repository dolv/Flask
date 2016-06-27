# all the imports
import os
#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.contrib.cache import SimpleCache
from basehash import base56
from random import randint
from urllib.parse import urlparse


# create our little application :)
app = Flask(__name__)
# Check Configuring Flask-Cache section for more details
cache = SimpleCache()

app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG=True
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

ALLOWED_SCHEMES = {'http', 'https', 'ftp'}

def random_key():
    return base56().encode(randint(0, 0xffffffff))

def get_random_string(CSRF_KEY_LENGTH=128):
    return base56(length=CSRF_KEY_LENGTH).hash(randint(0, base56(length=CSRF_KEY_LENGTH).maximum))

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = get_random_string()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        frm = urlparse(request.form['url'])
        ctx = {'schema': frm.scheme,
               'allowed_schemes': ALLOWED_SCHEMES
               }
        if frm.scheme in ALLOWED_SCHEMES:
            key = random_key()
            cache.add(key, request.form['url'])
            ctx['url'] = key
        else:
            ctx['error_message'] = "Supported schemes are: " + ", ".join(ALLOWED_SCHEMES)

        return render_template('index.html', **ctx)
    else:
        return Abort(400)

@app.route('/<key>/', methods=['GET'])
def redirect_view(key):
    redirect_url = cache.get(key) or "/"
    return redirect(redirect_url, code=302)

from flask_testing.utils import TestCase
class url_shortener_cache_Test(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'index.html')

    def test_index_post(self):
        from xml.etree import cElementTree as ET
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        root = ET.fromstring(response.get_data().decode("utf-8").replace("<!DOCTYPE html>",""))

        csrf = root.find(".//*input[@name='_csrf_token']").attrib['value']

        response = self.app.post('/', data={'url': 'http://example.com/',
                                            '_csrf_token': csrf})
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/', data={'url': 'mailto:admin@google.com'})
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'http')
        self.assertTrue(response.data.count(bytes('http', 'utf-8')))
        #self.assertContains(response, 'https')
        self.assertTrue(response.data.count(bytes('https', 'utf-8')))
        #self.assertContains(response, 'ftp')
        self.assertTrue(response.data.count(bytes('ftp', 'utf-8')))

    def test_redirect(self):
        response = self.app.get('/randomnonsense/')
        self.assertRedirects(response, '/')


if __name__ == "__main__":
    app.run()
from flask import request, redirect, abort,render_template
from werkzeug.contrib.cache import SimpleCache
from basehash import base56
from random import randint
from urllib.parse import urlparse
from __init__ import app
from forms import URLForm
from werkzeug.datastructures import MultiDict

cache = SimpleCache()
ALLOWED_SCHEMES = {'http', 'https', 'ftp'}

def random_key():
    return base56().encode(randint(0, 0xffffffff))

@app.route('/', methods=['POST', 'GET'])
def index():
    form = URLForm()
    if request.method == 'GET':
        # form.process(MultiDict())
        return render_template('index.html', form=form)
    if request.method == 'POST':
        frm = urlparse(request.form['url'])
        ctx = {'schema': frm.scheme,
               'allowed_schemes': ALLOWED_SCHEMES,
               }
        if frm.scheme in ALLOWED_SCHEMES:
            key = random_key()
            cache.add(key, request.form['url'])
            ctx['url'] = key
        else:
            ctx['error_message'] = "Supported schemes are: " + ", ".join(ALLOWED_SCHEMES)
        return render_template('index.html', **ctx, form=form)
    else:
        return abort(400)

@app.route('/<key>/', methods=['GET'])
def redirect_view(key):
    redirect_url = cache.get(key) or "/"
    return redirect(redirect_url, code=302)
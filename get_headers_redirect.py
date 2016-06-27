from flask import Flask, Response, redirect
from flask import make_response
from flask import request, abort
from flask import json, jsonify

app = Flask(__name__)

@app.route("/headers/<name>/")
#@app.route("/headers/<name>")
@app.route("/headers/")
#@app.route("/headers")
def headers_(name=None):
    if request.method == "GET" and name is not None:
        data = {}
        try:
            data['HTTP_' + name.upper()] = request.headers.environ['HTTP_' + name.upper()]
        except KeyError:
            abort(404)
        return Response(json.dumps(data), status=200, mimetype='application/json')
    if request.method == "GET":
        data = {}
        for k, v in request.headers.environ.items():
            # if type(v) in [str, bool, int, tuple]:
            if type(v) == str and k.startswith('HTTP'):
                data[k] = v
        return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route("/get", methods=['GET', 'POST'])
def get():
    if request.method == "GET":
        return Response(json.dumps(request.args), status=200, mimetype='application/json')
    if request.method == "POST":
        abort(400)

@app.route("/redirect/<n>/<count>")
@app.route("/redirect/<n>/")
@app.route("/redirect/<n>")
def redirecttion( n, count=0):
    if request.method == "GET":
        if int(n):
            return redirect("/redirect/" + str(int(n)-1) + "/" + str(int(count)+1), code=302)
        else:
            return Response(count, 200, mimetype="text/plain")
    else:
        return abort(404)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == "GET":
        resp = make_response("My custom text here", 200)
        return resp

from flask_testing.utils import TestCase
class Homework3Test(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_get(self):
        from werkzeug.datastructures import MultiDict
        params = {'a': '1', 'b': '2'}
        url='/get?'+"&".join("{!s}={!s}".format(key,val) for (key,val) in params.items())
        #response = self.app.get('/get', params)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        #self.assertJSONEqual(str(response.content, encoding='utf8'), params)
        self.assertEquals(json.loads(response.get_data(as_text=True)), params)
        #response = self.client.post('/get', params)
        response = self.app.post(url)
        self.assertEqual(response.status_code, 400)

    def test_headers(self):
        response = self.app.get('/headers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        headers = {'HTTP_USER_AGENT': 'r2d2'}
        response = self.app.get('/headers/USER_AGENT',environ_base=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEquals(json.loads(response.get_data(as_text=True)), headers)

    def test_redirect(self):
        response = self.app.get('/redirect/10/')
        self.assertRedirects(response, '/redirect/9/1')
        response = self.app.get('/redirect/0/10')
        #self.assertContains(response, '10')
        self.assertTrue(response.data.count(bytes('10', 'utf-8')))

if __name__ == "__main__":
    app.run()
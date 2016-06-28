from flask import Flask
from flask_wtf import CsrfProtect
csrf = CsrfProtect()

app = Flask(__name__)
app.config.from_object('settings')
csrf.init_app(app)

import views
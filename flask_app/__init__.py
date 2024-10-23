from flask import Flask
from .filters import format_date
from flask_bcrypt import Bcrypt
from os import environ

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY_URLSAFE')

bcrypt = Bcrypt(app)
app.add_template_filter(format_date)
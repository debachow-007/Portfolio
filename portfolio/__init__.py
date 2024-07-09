from flask import Flask
from flask_mail import Mail  # type: ignore
from portfolio.config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

with open('portfolio/data.json') as f:
    data = json.load(f)
mail = Mail(app)

from portfolio import routes
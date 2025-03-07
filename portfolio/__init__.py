from flask import Flask
from flask_wtf import CSRFProtect # type: ignore
from flask_mail import Mail  # type: ignore
from portfolio.config import Config
import json
from flask_cors import CORS # type: ignore

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

csrf = CSRFProtect(app)
with open('portfolio/data.json') as f:
    data = json.load(f)
mail = Mail(app)

from portfolio import routes
from flask import Flask # type: ignore
from flask_wtf import CSRFProtect # type: ignore
from flask_mail import Mail  # type: ignore
from portfolio.config import Config
import json
from flask_cors import CORS # type: ignore
import google.generativeai as genai
import cohere

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.config.from_object(Config)
CORS(app)
genai.configure(api_key=Config.API_KEY)
co = cohere.Client(Config.COHERE_API_KEY)
csrf = CSRFProtect(app)

with open('portfolio/data.json') as f:
    data = json.load(f)

mail = Mail(app)

from portfolio import routes
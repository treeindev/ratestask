import os
from dotenv import load_dotenv
from flask import Flask
from controllers.routes import api

load_dotenv()
app = Flask(__name__)
app.register_blueprint(api)
app.run(port=5000, debug=True)
import config
from flask import Flask
from exts import db

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

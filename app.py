from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, db)

db.init_app(app)

from views import *

if __name__ == '__main__':
    app.run()


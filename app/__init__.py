from flask import Flask
from config import Config
from .site.routes import site
from .auth.routes import auth
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

# initialize app
app = Flask(__name__)

CORS(app)

# register blueprints & link config
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.config.from_object(Config)

# register and initialize packages
app.JSONEncoder = JSONEncoder
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

# ensure only one app running at a time
if __name__ == "__main__":
    app.run(debug=True)
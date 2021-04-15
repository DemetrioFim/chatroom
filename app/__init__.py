from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
login = LoginManager()
login.login_view = 'login'
login.init_app(app)


from app import routes, models

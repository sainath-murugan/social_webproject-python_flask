from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail


app = Flask(__name__)

app.config["SECRET_KEY"] = "11c07514a6d98364ac6f129d49cf7e57"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdata.db"
app.config["SQLALCHEMY_ECHO"] = False
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=365)
app.config["REMEMBER_COOKIE_NAME"] = "6f7g8fdn4g9h6gtt74fhb8gh648th"
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

#app.config["REMEMBER_COOKIE_REFRESH_EACH_REQUEST"] = True


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "you have not logged in, please login to access"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "demoappflask@gmail.com"
app.config["MAIL_PASSWORD"] = "demo@flask"
mail = Mail(app)


from flaskblog import routes


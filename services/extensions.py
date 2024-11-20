import os

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager



db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

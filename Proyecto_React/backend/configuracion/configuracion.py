from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modelos import *
from configuracion.extensiones import db
from dotenv import load_dotenv
load_dotenv()  
import os

def crear_app():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(__name__,static_folder=os.path.join(base_dir, 'static'),template_folder=os.path.join(base_dir, 'templates'))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

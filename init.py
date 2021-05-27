from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spells.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from main import *


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

import sqlite3 #only needed for testing, SQLAlchemy will do heavy lifting later on. 

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/spells")
def all_spells():
    return render_template("all_spells.html")

@app.route("/spell/<id>")
def spell(id):
    return render_template("spell.html", id=id)

@app.route("/casters")
def all_casters():
    return render_template("all_casters.html")

@app.route("/caster/<id>")
def caster(id):
    return render_template("caster.html")



if __name__ == "__main__":
    app.run(debug=True)
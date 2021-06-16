from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spells.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


import models

@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/spells")
def all_spells():
    spells = models.Spell.query.all()

    return render_template("all_spells.html", spells = spells)

@app.route("/spell/<int:id>")
def spell(id):
    spell = models.Spell.query.filter_by(id=id).first_or_404()

    return render_template("spell.html", spell=spell)

@app.route("/casters")
def all_casters():
    casters = models.Caster.query.all()

    return render_template("all_casters.html", casters=casters)

@app.route("/caster/<id>")
def caster(id):
    caster = models.Caster.query.filter_by(id=id).first_or_404()
    spells = models.Spell.query.filter(models.Spell.casters.any(id=id)).all()
    return render_template("caster.html", caster=caster, spells=spells)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404







if __name__ == "__main__":
    app.run(debug=True)
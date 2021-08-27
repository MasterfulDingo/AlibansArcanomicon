from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

#initialising the app under which the site runs
app = Flask(__name__) 

#configuring the app for use, this will need to be changed before release
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spells.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creating the object db, which is used by SQLAlchemy to access the database
db = SQLAlchemy(app)


import models


@app.route("/") #home/landing page
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/spells") #spells page, shows all spells and has links to their individual pages
def all_spells():
    spells = models.Spell.query.order_by(models.Spell.name).all()

    return render_template("all_spells.html", spells = spells)

@app.route("/spell/<int:id>") #spell page, shows all information for a single spell (decided by the id in the url)
def spell(id):
    spell = models.Spell.query.filter_by(id=id).first_or_404()
    # tags = models.Tag.query.filter(models.Tag.spells.any(id=id)).all() #for use when I have data in my tag table, currently it will just slow things down.
    return render_template("spell.html", spell=spell)

@app.route("/casters") #casters page, shows all casters, links to their individual pages and has a brief blurb
def all_casters():
    casters = models.Caster.query.order_by(models.Caster.name).all()

    return render_template("all_casters.html", casters=casters)

@app.route("/caster/<id>") #caster page, shows all spells available to a single caster decided by the id in the url
def caster(id):
    caster = models.Caster.query.filter_by(id=id).first_or_404()
    spells = models.Spell.query.filter(models.Spell.casters.any(id=id)).all()
    return render_template("caster.html", caster=caster, spells=spells)

@app.route("/search", methods=("GET","POST"))
def search():
    spells = models.Spell.query.order_by(models.Spell.name).all()
    return render_template("search.html", spells=spells)



@app.errorhandler(404) #404 handler, if a url for the page is not found the 404 page will be returned
def page_not_found(e):
    return render_template('404.html'), 404







if __name__ == "__main__":
    app.run(debug=True)
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
    schools = models.School.query.order_by(models.School.name).all()
    casters = models.Caster.query.order_by(models.Caster.name).all()
    if request.method == "POST":
        params = request.form.getlist("param")

        if bool(params) == False: #if no parameters are submitted, return full results
            return render_template("search.html", spells=spells, schools=schools, casters=casters)

        else:
            #defining variables
            spellslists = []
            spellsets = []
            levelspellslists = []
            schoolspellslists = []
            concentrationspellslists = [] #both concentration and ritual are binary values, every spell either has them or doesn't. this means that if both boxes are ticked, either no spells will be returned (filter by intersection, 1st iteration), or all spells will be returned (probably what the user wants, what i decided to make). this could be avoided by searching the params list and if two values of either concentration or ritual are returned, simply discounting those parameters, as they do not filter anything in this case. While this would be more efficient, I could find no efficient or pretty way to do so, and so have decided to simply take the spells they return and process them like everything else.
            ritualspellslists = []
            intersection = True #if user wants intersection, not union

            for param in params: #loops through each parameter returned and split it into the category being filtered and the filter itself
                param = param.split("_")

                if param[0] == "Union": #this tells the function whether to take only items that meet all of the multiple paramaters, or to take any that meet one or more of multiple paramaters. this provides users more freedom and flexibility in finding spells they need.
                    intersection = False

                if param[0] == "level" or param[0] == "school" or param[0] == "concentration" or param[0] == "ritual": #these are discrete variables with no overlap, as you cannot have a spell that is both level 1 and 4 or that is both transmutation and evocation (as defined by the game rules). Because of this, we turn the returned spell lists into sets and combine them so all results are shown.
                    if param[0] == "level":
                        templist = models.Spell.query.filter_by(level=param[1]).all()
                        levelspellslists.append(templist)

                    if param[0] == "school":
                        templist = models.Spell.query.filter_by(school=int(param[1])).all()
                        schoolspellslists.append(templist)

                    if param[0] == "concentration":
                        templist = models.Spell.query.filter_by(concentration=int(param[1])).all()
                        concentrationspellslists.append(templist)

                    if param[0] == "ritual":
                        templist = models.Spell.query.filter_by(ritual=int(param[1])).all()
                        ritualspellslists.append(templist)

                if param[0] == "caster": #each spell can be cast by multiple casters, so I take a list of all the spells available to each caster here, and the user can then decide if they want to filter them by union or intersection.
                    templist = models.Spell.query.filter(models.Spell.casters.any(id=param[1])).all()
                    spellslists.append(templist)
            spellsets = set_maker(spellslists) #this function turns a list of lists into a list of sets

            if bool(levelspellslists) != False:
                levelsets = set_maker(levelspellslists)
                levelspells = levelsets[0].union(*levelsets)
                spellsets.append(levelspells)

            if bool(schoolspellslists) != False:
                schoolsets = set_maker(schoolspellslists)
                schoolspells = schoolsets[0].union(*schoolsets)
                spellsets.append(schoolspells)

            if bool(concentrationspellslists) != False:
                concentrationsets = set_maker(concentrationspellslists)
                concentrationspells = concentrationsets[0].union(*concentrationsets)
                spellsets.append(concentrationspells)

            if bool(ritualspellslists) != False:
                ritualsets = set_maker(ritualspellslists)
                ritualspells = ritualsets[0].union(*ritualsets)
                spellsets.append(ritualspells)

            if bool(spellsets) == True:
                if intersection == True:
                    spells = list(spellsets[0].intersection(*spellsets))
                if intersection == False:
                    spells = list(spellsets[0].union(*spellsets))
                spells.sort(key=sort_key)
                return render_template("search.html", spells=spells, schools=schools, casters=casters)

            if bool(spellsets) == False:
                return render_template("search.html", spells=spells, schools=schools, casters=casters)
    return render_template("search.html", spells=spells, schools=schools, casters=casters)


def set_maker(inputlists): #this function takes a list of lists and turns it into a list of sets
    outputsets = []
    for inputlist in inputlists:
        outputset = set(inputlist)
        outputsets.append(outputset)
    return outputsets


def sort_key(spell): #this function creates a key by which a list can be filtered.
    return spell.name


@app.route("/search/instructions")
def searchinstructions():
    return render_template('searchinstructions.html')


@app.errorhandler(404) #404 handler, if a url for the page is not found the 404 page will be returned
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
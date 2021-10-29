'''
Lachlan Row
3/05/2021 - 29/10/2021

D&D spell compendium website, built with flask and SQLAlchemy
this website is for my year 13 software engineering project, being graded against the database, programming, and media standards

'''

from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# initialising the app under which the site runs
app = Flask(__name__) 

# configuring the app for use, this will need to be changed before release
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spells.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creating the object db, which is used by SQLAlchemy to access the database
db = SQLAlchemy(app)

# importing models for queries
import models

# home/landing page
@app.route("/") 
@app.route("/home")
def home():
    user = current_user() # every route which returns a web page also returns the user object, which tells the browser if a user is logged in, and alters the options available on the nav bar if there is.
    return render_template("home.html", user=user)

# function for finding information on any current user session
def current_user(): 
    if session.get("user"): # if a user session is found return the data sorrounding that user
        return models.User.query.get(session['user'])
    else: 
        return False

# function to create a user session
@app.context_processor
def add_current_user(): 
    if session.get('user'): 
        return dict(current_user=models.User.query.get(session['user']))
    return dict(current_user=None)

# login page, takes username and password inputs and compares them to values in the database. if there is a match, a user session is created.
@app.route("/login", methods=['GET', 'POST'])
def login():
    user = current_user()
    if request.method == 'POST':  # if POST method then the form data will be compared to whats in the db, user will be logged in if inputted data matches
        user = models.User.query.filter(models.User.name == request.form.get('username')).first() # checks the username input against database
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user'] = user.id
            return redirect(url_for('userpage', user=user))  # redirect to user's page, so they can start making spellbooks right away
        else:
            return render_template("login.html", error='username or password incorrect', user=user)
    return render_template("login.html", user=user)

# logoute route, has no actual page, just removes the current user session
@app.route("/logout")
def logout():
    user = current_user()
    try:
        session.pop('user')  # removes user session
    except:  # returns an error if the user tries to type in logout route whilst not logged in
        return redirect(url_for('login', error='not currently logged in', user=user)) 
    return redirect(url_for('home', user=user))

# account creation page, makes a new user account with a username and password, salts and hashes the password before storing it in the database for security
@app.route("/createaccount", methods=['GET', 'POST']) 
def createaccount():
    user = current_user()
    if request.method == 'POST':
        if 5 > len(request.form.get('username')) > 20:  # the username must be between 4 and 21 characters
            return render_template("createaccount.html", error='username must be between 5 and 12 characters', user=user) 
        elif models.User.query.filter(models.User.name == request.form.get('username')).first():  # usernames cannot double up
            return render_template("createaccount.html", error='username already in use', user=user) 
        elif len(request.form.get('password')) < 7:  # if length of inputted password is less than 7 it will not be accepted. The longer a password, the harder it is to find through brute force.
            return render_template("createaccount.html", error='password must be a minimum of 7 characters', user=user) 
        else:
            user_info = models.User (
                name = request.form.get('username'),  # takes username from form
                password = generate_password_hash(request.form.get('password'), salt_length=10),  # takes password inputted in form and salts and hashes it for encryption
                validation = 0,
                )
            db.session.add(user_info)
            db.session.commit()
            return render_template("login.html", error="please login in :)", user=user)
    return render_template("createaccount.html", user=user)

# function for editing the name of a spellbook, used in both spellbook creation and name changing
def editspellbookname(user,spellbookname,spellbooknumber):
    if bool(spellbookname) == False:  #check to see if null result was submitted
        return "nullname"
    elif  len(spellbookname) < 5 or len(spellbookname) > 30:  #making sure the name isn't too big or small
        return "namelen"
    else:
        userspellbook = models.User.query.filter_by(name=user.name).first()
        if spellbooknumber == 1:
            userspellbook.spellbook1 = spellbookname
        elif spellbooknumber == 2:
            userspellbook.spellbook2 = spellbookname
        elif spellbooknumber == 3:
            userspellbook.spellbook3 = spellbookname
        elif spellbooknumber == 4:
            userspellbook.spellbook4 = spellbookname
        elif spellbooknumber == 5:
            userspellbook.spellbook5 = spellbookname
        db.session.merge(userspellbook)
        db.session.commit()
        return "okay"

# user page, shows username and a list of links to user spellbooks, also allows users to create new spellbooks (up to 5)
@app.route("/user", methods = ['GET', 'POST'])
def userpage():
    user = current_user()
    if user == False:
        return redirect(url_for("login", error='not currently logged in', user=user))
    if request.method == 'POST':
        spellbookname = request.form.get('spellbook')
        spellbooknumber = int(request.form.get('spellbooknum'))  #if users alter this value so it cannot be converted into an integer this will break, possibly badly. this will require inspect to do
        action = editspellbookname(user,spellbookname,spellbooknumber)
        if action == "nullname":
            return render_template("userpage.html", error='Please enter a name into the text field', user=user)
        elif action == "namelen":
            return render_template("userpage.html", error='name must be between 5 and 30 characters!', user=user)
        elif action == "okay":
            return render_template("userpage.html", user=user)
    return render_template("userpage.html", user=user)

# spellbook page, shows the spells present in one of the user's spellbooks and allows them to change the spellbook name.
@app.route("/user/<int:spellbook>", methods = ['GET', 'POST'])
def spellbook(spellbook):
    user = current_user()
    if user == False:
        return redirect(url_for("login", error='not currently logged in', user=user))
    spellbooklist = [user.spellbook1, user.spellbook2, user.spellbook3, user.spellbook4, user.spellbook5]  # this gives an iterable list, the user object has too many fields to iterate through
    for i in range(1,6):
        if i == spellbook and bool(spellbooklist[i-1]) != False:  #adjusting for zero indexing between list and url
            spells = models.Spell.query.filter(models.Spell.users.any(models.UserSpells.userbookid==i), models.Spell.users.any(uid=user.id)).all()
            if request.method == 'POST':
                spellbookname = request.form.get('spellbook')
                spellbooknumber = int(request.form.get('spellbooknum'))  #if users alter this value so it cannot be converted into an integer this will break, possibly badly. this will require inspect to do
                action = editspellbookname(user,spellbookname,spellbooknumber)
                if action == "nullname":
                    return render_template("spellbook.html", spellbook=spellbooklist[i-1], spells=spells, id=spellbook, error='Please enter a name before creating that spellbook', user=user)
                elif action == "namelen":
                    return render_template("spellbook.html", spellbook=spellbooklist[i-1], spells=spells, id=spellbook, error='name must be between 5 and 30 characters!', user=user)
                elif action == "okay":
                    user = current_user()
                    spellbooklist = [user.spellbook1, user.spellbook2, user.spellbook3, user.spellbook4, user.spellbook5]  # this is to refresh the spellbook name, so the new name is presented straight away for the user
                    return render_template("spellbook.html", spellbook=spellbooklist[i-1], spells=spells, id=spellbook, user=user)
            return render_template("spellbook.html", spellbook=spellbooklist[i-1], spells=spells, id=spellbook, user=user)
    return render_template("404.html", error = 'This spellbook has not, or cannot, be created.', user=user), 404

# spells page, shows all spells and has links to their individual pages
@app.route("/spells") 
def all_spells():
    user = current_user()
    spells = models.Spell.query.order_by(models.Spell.name).all()
    return render_template("all_spells.html", spells=spells, user=user)

# spell page, shows all information for a single spell (decided by the id in the url)
@app.route("/spell/<int:id>") 
def spell(id):
    user = current_user()
    spell = models.Spell.query.filter_by(id=id).first_or_404()
    # tags = models.Tag.query.filter(models.Tag.spells.any(id=id)).all() #for use when I have data in my tag table, currently it will just slow things down.
    return render_template("spell.html", spell=spell, user=user)

# casters page, shows all casters, links to their individual pages and has a brief blurb
@app.route("/casters") 
def all_casters():
    user = current_user()
    casters = models.Caster.query.order_by(models.Caster.name).all()
    return render_template("all_casters.html", casters=casters, user=user)

# caster page, shows all spells available to a single caster decided by the id in the url
@app.route("/caster/<int:id>") 
def caster(id):
    user = current_user()
    caster = models.Caster.query.filter_by(id=id).first_or_404()
    spells = models.Spell.query.filter(models.Spell.casters.any(id=id)).all()
    return render_template("caster.html", caster=caster, spells=spells, user=user)

# search page, allows users to filter all spells by different parameters
@app.route("/search", methods=("GET","POST"))
def search():
    user = current_user()
    spells = models.Spell.query.order_by(models.Spell.name).all()
    schools = models.School.query.order_by(models.School.name).all()
    casters = models.Caster.query.order_by(models.Caster.name).all()
    if request.method == "POST":
        params = request.form.getlist("param")
        if bool(params) == False: # if no parameters are submitted, return full results
            return render_template("search.html", spells=spells, schools=schools, casters=casters, user=user)
        else:
            spellslists = []
            spellsets = []
            levelspellslists = []
            schoolspellslists = []
            concentrationspellslists = []
            ritualspellslists = []
            intersection = True  # if user wants intersection, not union
            for param in params:  # loops through each parameter returned and split it into the category being filtered and the filter itself
                param = param.split("_")
                if param[0] == "Union": # this tells the function whether to take only items that meet all of the multiple paramaters, or to take any that meet one or more of multiple paramaters. this provides users more freedom and flexibility in finding spells they need.
                    intersection = False
                if param[0] == "level" or param[0] == "school" or param[0] == "concentration" or param[0] == "ritual":  #these are discrete variables with no overlap, as you cannot have a spell that is both level 1 and 4 or that is both transmutation and evocation (as defined by the game rules). Because of this, we turn the returned spell lists into sets and combine them so all results are shown.
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
                if param[0] == "caster":  # each spell can be cast by multiple casters, so I take a list of all the spells available to each caster here, and the user can then decide if they want to filter them by union or intersection.
                    templist = models.Spell.query.filter(models.Spell.casters.any(id=param[1])).all()
                    spellslists.append(templist)
            spellsets = set_maker(spellslists)  # this function turns a list of lists into a list of sets
            if bool(levelspellslists) != False:  # each of these if statements checks to see the list has anything in it, and then turn the conjugate lists into sets and remove any double ups by taking the union of them all
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
                spells.sort(key = sort_key)
                return render_template("search.html", spells=spells, schools=schools, casters=casters, user=user)
            if bool(spellsets) == False:
                return render_template("search.html", spells=spells, schools=schools, casters=casters, user=user)
    return render_template("search.html", spells=spells, schools=schools, casters=casters, user=user)

# this function takes a list of lists and turns it into a list of sets
def set_maker(inputlists): 
    outputsets = []
    for inputlist in inputlists:
        outputset = set(inputlist)
        outputsets.append(outputset)
    return outputsets

# this function creates a key by which a list can be filtered.
def sort_key(spell): 
    return spell.name

# search instructions page, purely presents list of 
@app.route("/search/instructions")
def searchinstructions():
    user = current_user()
    return render_template('searchinstructions.html', user=user)

# 404 handler, if a url for the page is not found the 404 page will be returned
@app.errorhandler(404) 
def page_not_found(e):
    user = current_user()
    return render_template('404.html', user=user), 404

# runs the site
if __name__ == "__main__":
    app.secret_key = 'super secret key'  # the secret key is used for initialising encrypted communications between server and browser. this key would not be good for a production app, but for testing it is adequate
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
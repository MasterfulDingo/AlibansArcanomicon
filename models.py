from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spells.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Spell (db.Model):
    __tablename__ = "Spell"
    id = db.Column(db.Integer, unique = True, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)
    level = db.Column(db.Integer)
    components = db.Column(db.String())
    concentration = db.Column(db.Integer)
    ritual = db.Column(db.Integer)
    damage = db.Column(db.String())
    range = db.Column(db.Integer, db.ForeignKey('Range.id'))
    duration = db.Column(db.Integer, db.ForeignKey('Duration.id'))
    castingtime = db.Column(db.Integer, db.ForeignKey('Castingtime.id'))
    school = db.Column(db.Integer, db.ForeignKey('School.id'))

    ranges = db.relationship('Range', backref='spell')
    durations = db.relationship('Duration', backref='spell')
    castingtimes = db.relationship('Castingtime', backref='spell')
    schools = db.relationship('School', backref='school')

class Range (db.Model):
    __tablename__ = "Range"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())

class Duration (db.Model):
    __tablename__ = "Duration"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())

class Castingtime (db.Model):
    __tablename__ = "Castingtime"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())

class School (db.Model):
    __tablename__ = "School"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)

class Caster (db.Model):
    __tablename__ = "Caster"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)

class Tag (db.Model):
    __tablename__ = "Tag"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)

class User (db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    bio = db.Column(db.Text(280))
    validation = db.Column(db.Integer)
    spellbook1 = db.Column(db.String(80))
    spellbook2 = db.Column(db.String(80))
    spellbook3 = db.Column(db.String(80))
    spellbook4 = db.Column(db.String(80))
    spellbook5 = db.Column(db.String(80))

SpellCaster = db.Table('SpellCaster',
    db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
    db.Column('cid', db.Integer, db.ForeignKey('Caster.id'))
)

SpellTag = db.Table('SpellTag',
    db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
    db.Column('tid', db.Integer, db.ForeignKey('Tag.id'))
)

UserSpells = db.Table('UserSpells',
    db.Column('uid', db.Integer, db.ForeignKey('User.id')),
    db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
    db.Column('userbookid', db.Integer)
)
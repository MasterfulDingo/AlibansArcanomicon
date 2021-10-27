from main import db

#these are my bridging tables, I define these at the top so I get no errors from referencing things not created later in the doc

SpellCaster = db.Table('SpellCaster', #joining table between Spell and Caster
    db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
    db.Column('cid', db.Integer, db.ForeignKey('Caster.id'))
)

SpellTag = db.Table('SpellTag', #joining table between Spell and Tag
    db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
    db.Column('tid', db.Integer, db.ForeignKey('Tag.id'))
)

# UserSpells = db.Table('UserSpells', #joining table between Spell and User
#     db.Column('uid', db.Integer, db.ForeignKey('User.id')),
#     db.Column('sid', db.Integer, db.ForeignKey('Spell.id')),
#     db.Column('userbookid', db.Integer)
# )

class UserSpells (db.Model):
    __tablename__ = "UserSpells"

    sid = db.Column(db.Integer, db.ForeignKey('Spell.id'), primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

    userbookid = db.Column(db.Integer)

    spell = db.relationship('Spell', back_populates="users")
    user = db.relationship('User', back_populates="spells")



class Spell (db.Model): #main table in my database, this is the main table I query for information on all my spells.
    __tablename__ = "Spell"

    #these are the columns present in the Spell table in the database object
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

    #these are objects created with SQLAlchemy to facilitate one-many queries (based on the foreign keys in my database)
    ranges = db.relationship('Range', backref='spell')
    durations = db.relationship('Duration', backref='spell')
    castingtimes = db.relationship('Castingtime', backref='spell')
    schools = db.relationship('School', backref='school')

    #these are objects created with SQLAlchemy to facilitate many-many queries. note that the syntax is different to one-many relationships, they reference a secondary table (defined at the top of this file.)
    casters = db.relationship('Caster', secondary=SpellCaster, back_populates='spells')
    tags = db.relationship('Tag', secondary=SpellTag, back_populates='spells')
    users = db.relationship('UserSpells', back_populates='spell')

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

class Caster (db.Model): #Caster, the first table with a many-many relationship with Spell
    __tablename__ = "Caster"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)
    
    spells = db.relationship('Spell', secondary=SpellCaster, back_populates='casters')

class Tag (db.Model): #Tag, like Caster but second
    __tablename__ = "Tag"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.Text)

    spells = db.relationship('Spell', secondary=SpellTag, back_populates='tags')

class User (db.Model): #This table will contain data for all the users that make accounts to access the site. I am still finalising details on this table.
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    password = db.Column(db.String())
    validation = db.Column(db.Integer)
    spellbook1 = db.Column(db.String(80))
    spellbook2 = db.Column(db.String(80))
    spellbook3 = db.Column(db.String(80))
    spellbook4 = db.Column(db.String(80))
    spellbook5 = db.Column(db.String(80))

    spells = db.relationship('UserSpells', back_populates='user')

"""
def __repr__(self):
    return self.name, self.id etc

this function is tacked onto the end of a model and defines what is returned when the table is queried.
"""
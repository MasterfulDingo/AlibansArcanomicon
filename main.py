from flask import Flask, render_template, redirect, request





from models import app, Spell, Range, Duration, Castingtime, School


@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/spells")
def all_spells():
    spells = Spell.query.all()

    return render_template("all_spells.html", spells = spells)

@app.route("/spell/<int:id>")
def spell(id):
    spell = Spell.query.filter_by(id=id).first_or_404()
        # .join(Range, Spell.range==Range.id)\
        # .join(Duration, Spell.duration==Duration.id)\
        # .join(School, Spell.school==School.id)\
        # .add_columns(Spell.id, Spell.name, Spell.description, Spell.level, Spell.components, Spell.concentration, Spell.ritual, Spell.damage, Range.name, Duration.name, School.name)\
        
    print(spell)
    return render_template("spell.html", spell=spell)

@app.route("/casters")
def all_casters():
    return render_template("all_casters.html")

@app.route("/caster/<id>")
def caster(id):
    return render_template("caster.html", id=id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404







if __name__ == "__main__":
    app.run(debug=True)
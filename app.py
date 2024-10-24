from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import (
    SQLAlchemy,
)  # this is a tool to interact with the database instance
from models import db, Pet, Species
from forms import PetForm

app = Flask(
    __name__
)  # create instance of flask class, __name__tells where to look for resources.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///pets.db"  # specifying the database file pets.db
)
app.config["SECRET_KEY"] = (
    "your_secret_key"  # configuration of secret key for session management
)
db.init_app(app)  # connects the database instance to the flask application


@app.route("/")  # Route for the home page, renders home.html
def home():
    return render_template("home.html")


@app.route("/pets", methods=["GET", "POST"])  # route for adding pets
def add_pet():
    form = PetForm()
    if form.validate_on_submit():  # checks if the form is submitted and valid
        # I am checking if the species already exists
        species_name = form.species.data
        species = Species.query.filter_by(
            name=species_name
        ).first()  # checking if the species already exists in the database

        if (
            not species
        ):  # writing this to create new species if the specie doesn't exist
            species = Species(name=species_name)
            db.session.add(species)
            db.session.commit()

        new_pet = Pet(name=form.name.data, species_id=species.id)
        db.session.add(new_pet)  # add new pet to database session
        db.session.commit()  # commit the database and saves new pet to the database
        return redirect(url_for("pet_list"))  # redirects to pet_list route

    return render_template(
        "add_pet.html", form=form
    )  # If the form is not submitted/invalid, it renders the add_pet.html template, passing the object for rendering.


# I have seperated the pet table and species table this time, with species table having species id and name,
# where species id is foreign key in the pets table
@app.route("/pet_list", methods=["GET"])
def pet_list():
    species_id = request.args.get("species_id")
    if species_id:
        pets = Pet.query.filter_by(species_id=species_id).all()
    else:
        pets = Pet.query.all()  # Queries the database for all the pets

    species = Species.query.all()
    return render_template(
        "pet_list.html", pets=pets, species=species
    )  # renders the pet_list by passing the pets


# This module is for the feature editting the already existing pet
@app.route("/pets/edit/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        # Check if the entered species exists
        species_name = form.species.data
        species = Species.query.filter_by(name=species_name).first()

        if not species:  # If species doesn't exist, create a new one
            species = Species(name=species_name)
            db.session.add(species)
            db.session.commit()

        pet.name = form.name.data
        pet.species_id = species.id
        db.session.commit()
        return redirect(url_for("pet_list"))

    return render_template("edit_pet.html", form=form, pet=pet)


# This module is for the feture delete the pet from the list
@app.route("/pets/delete/<int:pet_id>", methods=["POST"])
def delete_pet(pet_id):
    # retrieving the pet from the database by using the pet_id and if not found, it returns 404 error
    pet = Pet.query.get_or_404(pet_id)
    species_id = pet.species_id
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for("pet_list"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

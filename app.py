from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # this is a tool to interact with the database instance
from models import db, Pet
from forms import PetForm

app = Flask(__name__)  #create instance of flask class, __name__tells where to look for resources.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db' #specifying the database file pets.db
app.config['SECRET_KEY'] = 'your_secret_key' #configuration of secret key for session management
db.init_app(app) # connects the database instance to the flask application

@app.route('/')  # Route for the home page, renders home.html
def home():
    return render_template('home.html')

@app.route('/pets', methods=['GET', 'POST']) # route for adding pets
def add_pet():
    form = PetForm()
    if form.validate_on_submit(): # checks if the form is submitted and valid
        new_pet = Pet(name=form.name.data, species=form.species.data)
        db.session.add(new_pet) # add new pet to database session
        db.session.commit() #commit the database and saves new pet to the database
        return redirect(url_for('pet_list')) # redirects to pet_list route
    return render_template('add_pet.html', form=form) # If the form is not submitted/invalid, it renders the add_pet.html template, passing the object for rendering.

@app.route('/pet_list')
def pet_list():
    pets = Pet.query.all()  # Queries the database for all the pets
    return render_template('pet_list.html', pets=pets) # renders the pet_list by passing the pets

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

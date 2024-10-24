from flask_sqlalchemy import SQLAlchemy

# create a sqlalchemy object
db = SQLAlchemy()


class Species(db.Model):
    # this class Species represents a table in db that has species id and name of the specie
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"{self.name}"


class Pet(db.Model):
    # defines class pet that is inherited from db.Model, this represents a table in db
    # define three columns 'id', 'name', 'species' with datatypes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # defining species id from Species table as foreign key
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"), nullable=False)
    # creating a relationship to the species model, and create a reverse reation allowing access to all pets of species
    species = db.relationship("Species", backref="pets")

    def __repr__(self):
        return f"<Pet {self.name}, Species: {self.species.name}>"

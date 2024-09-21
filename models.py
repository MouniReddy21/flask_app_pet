from flask_sqlalchemy import SQLAlchemy

#create a sqlalchemy object
db = SQLAlchemy()

class Pet(db.Model):  # defines class pet that is inherited from db.Model, this represents a table in db
    #define three columns 'id', 'name', 'species' with datatypes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False) #cannot have null values

    def __repr__(self):
        return f"<Pet {self.name}, Species: {self.species}>"

from flask_wtf import FlaskForm  #it provides protection
from wtforms import StringField, SubmitField # field type for accpeting string inputs and field for submit button
from wtforms.validators import DataRequired #validates that the field is not left empty

# Defines forms used to collect user input for adding new pets from the applicaton
class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    submit = SubmitField('Add Pet')

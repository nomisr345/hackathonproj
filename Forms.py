from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, TextAreaField,IntegerField, validators,FileField,RadioField, EmailField
from wtforms.validators import DataRequired, NumberRange, AnyOf
from wtforms.validators import ValidationError
class SearchForm(FlaskForm):
    maxcalories = IntegerField('Maximum Calories', validators=[DataRequired(), NumberRange(min=50, max=800)])
    minprotein = IntegerField('Minimum Protein', validators=[DataRequired(), NumberRange(min=10, max=100)])
    maxfat = IntegerField('Maximum Fat', validators=[DataRequired(), NumberRange(min=1, max=100)])
    allergies = StringField('Allergies')
    preferredDiet = StringField('Allergies')

class CreateUserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    email = StringField('email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('password', [validators.Length(min=1, max=150), validators.DataRequired()])

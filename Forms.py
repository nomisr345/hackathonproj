from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange, AnyOf

class SearchForm(FlaskForm):
    maxcalories = IntegerField('Maximum Calories', validators=[DataRequired(), NumberRange(min=50, max=800)])
    minprotein = IntegerField('Minimum Protein', validators=[DataRequired(), NumberRange(min=10, max=100)])
    maxfat = IntegerField('Maximum Fat', validators=[DataRequired(), NumberRange(min=1, max=100)])
    allergies = StringField('Allergies')
    preferredDiet = StringField('Allergies')

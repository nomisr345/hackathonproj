# from wtforms import Form, StringField, SelectField, TextAreaField,IntegerField, validators,FileField
# from wtforms import DateField
# from wtforms import FileField
# from wtforms.validators import NumberRange
# from flask_wtf import FlaskForm
# from werkzeug.utils import secure_filename

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, NumberRange, AnyOf


# class CreateRecipeForm(Form):
#     reward_name = StringField('Reward Name:', [validators.Length(min=1, max=20), validators.DataRequired()])
#     points_required = IntegerField('Points Required:', [validators.DataRequired(), validators.NumberRange(min=1, max=1000)])
#     points_expiry = DateField('Points expiry date:')
#     reward_type = SelectField('Reward type', [validators.DataRequired()], choices=[('', 'Select'), ('V', 'Voucher'), ('D', 'Discount')], default='')
#     description = TextAreaField('Description', [validators.Optional()])
#     reward_pic = FileField('Image', [validators.Optional()])
#

# class preferenceform(Form):
#     range = {"calories":[50,800], "protein":[10,100], "fat":[1,100]}  #Dictionary for their respective ranges (For Example: Minimum 50kcal and Max 800Kcal allowed)
#     allergy = ["dairy","egg","gluten", "grain", "peanut", "seafood", "sesame", "shellfish", "soy", "sulfite", "tree nut", "wheat"]
#     diet = ["Gluten Free","Ketogenic","Vegetarian","Lacto-vegetarian","Ovo-vegetarian","Vegan","Pescetarian","Paleo", "None"]
#
#     calories = IntegerField([validators.DataRequired(),validators.NumberRange(min=50, max=800)], name="maxcalories")
#     proteins = IntegerField([validators.DataRequired(),validators.NumberRange(min=10, max=100)], name="minprotein")
#     fats = IntegerField([validators.DataRequired(),validators.NumberRange(min=1, max=100)], name="maxfat")
#     allergy = SelectField([validators.DataRequired()], choices = allergy, default='None',name="class")
#     diet = SelectField([validators.DataRequired()], choices = diet, default='None',name="class")
#

class SearchForm(FlaskForm):
    maxcalories = IntegerField('Maximum Calories', validators=[DataRequired(), NumberRange(min=50, max=800)])
    minprotein = IntegerField('Minimum Protein', validators=[DataRequired(), NumberRange(min=10, max=100)])
    maxfat = IntegerField('Maximum Fat', validators=[DataRequired(), NumberRange(min=1, max=100)])
    allergies = SelectMultipleField('Allergies', choices=[('Dairy', 'Dairy'), ('Egg', 'Egg'), ('Gluten', 'Gluten'),
                                                          ('Grain', 'Grain'), ('Peanut', 'Peanut'), ('Seafood', 'Seafood'),
                                                          ('Sesame', 'Sesame'), ('Shellfish', 'Shellfish'), ('Soy', 'Soy'),
                                                          ('Sulfite', 'Sulfite'), ('Tree Nut', 'Tree Nut'), ('Wheat', 'Wheat'),
                                                          ('None', 'None')],
                                    validators=[AnyOf(['Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut', 'Seafood',
                                                       'Sesame', 'Shellfish', 'Soy', 'Sulfite', 'Tree Nut', 'Wheat', 'None'])])
    preferredDiet = SelectField('Preferred Diet', choices=[('Gluten Free', 'Gluten Free'), ('Ketogenic', 'Ketogenic'),
                                                           ('Vegetarian', 'Vegetarian'), ('Lacto-vegetarian', 'Lacto-vegetarian'),
                                                           ('Ovo-vegetarian', 'Ovo-vegetarian'), ('Vegan', 'Vegan'),
                                                           ('Pescetarian', 'Pescetarian'), ('Paleo', 'Paleo'), ('None', 'None')],
                                validators=[AnyOf(['Gluten Free', 'Ketogenic', 'Vegetarian', 'Lacto-vegetarian', 'Ovo-vegetarian',
                                                   'Vegan', 'Pescetarian', 'Paleo', 'None'])])




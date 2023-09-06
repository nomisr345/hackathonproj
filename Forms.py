from wtforms import Form, StringField, SelectField, TextAreaField,IntegerField, validators,FileField
from wtforms import DateField
from wtforms import FileField
from wtforms.validators import NumberRange
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename


class CreateRecipeForm(Form):
    reward_name = StringField('Reward Name:', [validators.Length(min=1, max=20), validators.DataRequired()])
    points_required = IntegerField('Points Required:', [validators.DataRequired(), validators.NumberRange(min=1, max=1000)])
    points_expiry = DateField('Points expiry date:')
    reward_type = SelectField('Reward type', [validators.DataRequired()], choices=[('', 'Select'), ('V', 'Voucher'), ('D', 'Discount')], default='')
    description = TextAreaField('Description', [validators.Optional()])
    reward_pic = FileField('Image', [validators.Optional()])


class preferenceform(Form):
    range = {"calories":[50,800], "protein":[10,100], "fat":[1,100]}  #Dictionary for their respective ranges (For Example: Minimum 50kcal and Max 800Kcal allowed)
    allergy = ["dairy","egg","gluten", "grain", "peanut", "seafood", "sesame", "shellfish", "soy", "sulfite", "tree nut", "wheat"]
    diet = ["Gluten Free","Ketogenic","Vegetarian","Lacto-vegetarian","Ovo-vegetarian","Vegan","Pescetarian","Paleo", "None"]

    calories = IntegerField([validators.DataRequired(),validators.NumberRange(min=50, max=800)], name="maxcalories")
    proteins = IntegerField([validators.DataRequired(),validators.NumberRange(min=10, max=100)], name="minprotein")
    fats = IntegerField([validators.DataRequired(),validators.NumberRange(min=1, max=100)], name="maxfat")
    allergy = SelectField([validators.DataRequired()], choices = allergy, default='None',name="class")
    diet = SelectField([validators.DataRequired()], choices = diet, default='None',name="class")





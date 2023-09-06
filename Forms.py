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

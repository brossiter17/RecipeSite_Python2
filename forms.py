from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField, DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length

class BeneficiaryForm(FlaskForm):
    recipe_name = StringField('Recipe Name:', validators=[DataRequired()])
    recipe_ingredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    recipe_directions = TextAreaField('Directions:', validators=[DataRequired()])
    recipe_try = StringField('Try With:', validators=[DataRequired()])
    recipe_picture = FileField('Recipe Picture:', validators=[FileRequired()])


from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields import StringField, TextAreaField, DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length

class RecipeForm(FlaskForm):
    recipe_name = StringField('Name: ', validators=[DataRequired()])
    recipe_ingredients = TextAreaField('Ingredients: ', validators=[DataRequired()])
    recipe_directions = TextAreaField('Directions: ', validators=[DataRequired()])
    recipe_servings = StringField('Serves: ', validators=[DataRequired()])
    recipe_picture = FileField('Picture: ', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Add a valid picture and click Submit')])
import os
from flask import Flask, redirect, url_for, request, render_template, flash
from forms import RecipeForm
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '0(&*_)*(=0N *F)_8-)F*(D_)ZF*Nb-0s89dfPJF{()SD*_098sd[0f'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir','')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir','')

@app.route('/')
def hello_world():
    """
    Function to show example instance
    :return:
    """
    return render_template('index.html')

def is_recipe_name_taken(recipe_name):
    recipe_csv_file = os.path.join(app.config['SUBMITTED_DATA'], recipe_name.lower().replace(" ", "_") + '.csv')
    return os.path.exists(recipe_csv_file)

@app.route('/add_beneficiary_auto', methods = ['POST', 'GET'])
def add_beneficiary_auto():
    """
    Function to us inbuilt methods to add a recipe, with file handling
    :return:
    """
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        if is_recipe_name_taken(recipe_name):
            flash("Name is in use. Enter a new recipe name and click Submit", "error")
            form.recipe_name.data = recipe_name
            form.recipe_ingredients.data = request.form.get('recipe_ingredients', 'recipe_ingredients')
            form.recipe_directions.data = request.form.get('recipe_directions', 'recipe_directions')
            form.recipe_servings.data = request.form.get('recipe_servings', 'recipe_servings')
            return render_template('add_beneficiary_auto.html', form=form)
        recipe_ingredients = form.recipe_ingredients.data
        recipe_directions = form.recipe_directions.data
        recipe_servings = form.recipe_servings.data
        pic_filename = recipe_name.lower().replace(" ", "_") + '.' + secure_filename(form.recipe_picture.data.filename).split('.')[-1]
        form.recipe_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ingredients': recipe_ingredients, 'directions': recipe_directions, 'servings':recipe_servings, 'pic': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return render_template('recipe_added.html', recipe_name=recipe_name)
    else:
        return render_template('add_beneficiary_auto.html', form=form)

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    """
    Function to search for a recipe
    :return:
    """
    form = RecipeForm()
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        return redirect(url_for('display_search_results', recipe_name=recipe_name))
    return render_template('search_recipe.html', form=form)  # Pass the form to the template

@app.route('/display_search_results', methods=['GET'])
def display_search_results():
    """
    Function to display a recipe
    :return:
    """
    recipe_name = request.args.get('recipe_name', '')
    recipe_csv_file = os.path.join(app.config['SUBMITTED_DATA'], recipe_name.lower().replace(" ", "_") + '.csv')
    if os.path.exists(recipe_csv_file):
        df = pd.read_csv(recipe_csv_file)
        return render_template('view_recipe.html', recipe=df.iloc[0], recipe_name=recipe_name)
    else:
        return render_template('recipe_not_found.html', recipe_name=recipe_name)

@app.route('/search_delete', methods=['GET', 'POST'])
def search_delete():
    """
    Function to search for a recipe to delete
    :return:
    """
    form = RecipeForm()
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        return redirect(url_for('display_delete_results', recipe_name=recipe_name))
    return render_template('search_delete.html', form=form)

@app.route('/display_delete_results', methods=['GET'])
def display_delete_results():
    """
    Function to display the recipe to delete
    :return:
    """
    recipe_name = request.args.get('recipe_name', '')
    recipe_csv_file = os.path.join(app.config['SUBMITTED_DATA'], recipe_name.lower().replace(" ", "_") + '.csv')
    if os.path.exists(recipe_csv_file):
        df = pd.read_csv(recipe_csv_file)
        return render_template('view_delete.html', recipe=df.iloc[0], recipe_name=recipe_name)
    else:
        return render_template('delete_not_found.html', recipe_name=recipe_name)

@app.route('/delete_recipe/<recipe_name>', methods=['GET'])
def delete_recipe(recipe_name):
    """
    Function to delete a recipe
    :return:
    """
    recipe_csv_file = os.path.join(app.config['SUBMITTED_DATA'], recipe_name.lower().replace(" ", "_") + '.csv')

    if os.path.exists(recipe_csv_file):
        os.remove(recipe_csv_file)
        return render_template('delete_finished.html', recipe_name=recipe_name)
    else:
        return "Recipe not found"

@app.route('/display_data/<name>')
def render_information(name):
    """
    Function to return the required information
    :param name: Name of the beneficiary
    :return:
    """
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'), index_col=False)
    return render_template('view_recipe.html', recipe=df.iloc[0], recipe_name=df.iloc[0]['name'])

@app.errorhandler(404)
def page_not_found(e):
    """
    Standard error handling mechanism
    :param e: Error details
    :return:
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
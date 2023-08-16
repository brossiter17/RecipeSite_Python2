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

@app.route('/add_beneficiary', methods = ['POST', 'GET'])
def add_beneficiary():
    """
    Function add a beneficiary using a manual form
    :return:
    """
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        print(fname, lname)
        return "Beneficiary added successfully"
    else:
        return render_template('add_beneficiary_manual.html')




@app.route('/add_beneficiary_auto', methods = ['POST', 'GET'])
def add_beneficiary_auto():
    """
    Function to us inbuilt methods to add a beneficiary, with file handling
    :return:
    """
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        recipe_ingredients = form.recipe_ingredients.data
        recipe_directions = form.recipe_directions
        recipe_servings = form.recipe_servings
        pic_filename = recipe_name.lower().replace(" ", "_") + '.' + secure_filename(form.recipe_picture.data.filename).split('.')[-1]
        form.recipe_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ingredients': recipe_ingredients, 'directons': recipe_directions, 'servings':recipe_servings, 'pic': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return redirect(url_for('hello_world'))
    else:
        return render_template('add_beneficiary_auto.html', form=form)

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    form = RecipeForm()  # Create an instance of the form
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        return redirect(url_for('display_search_results', recipe_name=recipe_name))
    return render_template('search_recipe.html', form=form)  # Pass the form to the template

@app.route('/display_search_results', methods=['GET'])
def display_search_results():
    recipe_name = request.args.get('recipe_name', '')
    if recipe_name:
        df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return render_template('view_recipe.html', recipe=df.iloc[0])
    else:
        return "No recipe found"

@app.route('/display_data/<name>')
def render_information(name):
    """
    Function to return the required information
    :param name: Name of the beneficiary
    :return:
    """
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'), index_col=False)
    print (df.iloc[0]['name'])
    return render_template('view_recipe.html', recipe=df.iloc[0])

@app.route('/variabletest/<name>')
def print_variable(name):
    """
    Example function for dynamic content
    :param name: variable name
    :return:
    """
    return 'Hello %s!' % name

@app.route('/integertest/<int:intID>')
def print_integer(intID):
    """
    Example function for dynamic integer content
    :param intID: integer variable
    :return:
    """
    return 'Number %d!' % intID

@app.route('/floattest/<float:floatID>')
def print_float(floatID):
    """
    Example function for dynamic float variable content
    :param floatID: float variable
    :return:
    """
    return 'Floating Number %f!' % floatID

@app.route('/admin')
def hello_admin():
    """
    Example for a sample page
    :return: string
    """
    # return "Hello Admin"
    # return render_template('search_recipe.html')
    return render_template('search_recipe.html')

@app.route('/guest/<guest>')
def hello_guest(guest):
    """
    Example for a sample page with variable
    :param guest: variable
    :return: String
    """
    return "Hello % as Guest" % guest

@app.route('/user/<user>')
def hello_user(user):
    """
    Function that demonstrates the usage of url for function
    :param user:
    :return:
    """
    if user=='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=user))

@app.route('/input', methods = ['POST', 'GET'])
def information():
    """
    Function that demonstrates an example of gathering form info
    :return:
    """
    if request.method == 'POST':
        info = request.form['info']
        return redirect(url_for('hello_guest', guest=info))
    else:
        return redirect(url_for('hello_world'))

@app.route('/texample')
def table_example():
    """
    Function to show example of templating
    :return:
    """
    username = 'Michael'
    avg_score = 70
    marks_dict = {'phy': 50, 'che': 70, 'math': 90}
    return render_template('texample.html', name = username, marks = avg_score, results = marks_dict)

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
from flask import Flask
from flask import request
from db.dbop import dbop
import json

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/', methods=['GET'])
def home():
    return "<h1> This is Recipe-Optimizer! </h1>"

@application.route('/get-recipes', methods=['GET'])
def getRecipes():
    db = dbop()
    return(json.dumps(db.get_all_recipes()))

@application.route('/add-recipe', methods=['GET'])
def addRecipe():

    name = request.args.get('name')
    ingredients = request.args.get('ingredients')
    notes = request.args.get('notes')

    if(name == None or ingredients == None or notes == None):
        return "<div> check your parameters! </div>"

    db = dbop()
    rc = db.add_recipe(name, ingredients, notes)

    if(rc < 0):
        return "<div> something bad happened. might be with ingredient's formatting </div>"

    return(str(rc))

@application.route('/delete-recipe', methods=['GET'])
def deleteRecipe():
    db = dbop()
    return(json.dumps(db.get_all_recipes()))



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
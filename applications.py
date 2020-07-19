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
    id = int(request.args.get('id'))

    if(id == None):
        return "<div> check your parameters! </div>"
    db = dbop()
    return(json.dumps(db.get_all_recipes()))



@application.route('/get-schedule', methods=['GET'])
def getSchedule():
    db = dbop()
    return(json.dumps(db.get_all_schedule()))

@application.route('/add-schedule', methods=['GET'])
def addSchedule():
    recipe_id = int(request.args.get('recipe_id'))
    notes = request.args.get('notes')

    if(recipe_id == None or notes == None):
        return "<div> check your parameters! </div>"

    db = dbop()
    rc = db.add_schedule(recipe_id, notes)

    if(rc < 0):
        return "<div> something bad happened. might be with ingredient's formatting </div>"

    return(str(rc))

@application.route('/delete-schedule', methods=['GET'])
def deleteSchedule():
    id = int(request.args.get('id'))

    if(id == None):
        return "<div> check your parameters! </div>"

    db = dbop()
    return(db.delete_schedule(id)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
from flask import Flask
from flask import request
from flask_mail import Mail, Message
from flask_cors import CORS
from flaskext.mysql import MySQL
from db.dbop import dbop
import json

# EB looks for an 'app' callable by default.
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypass'
app.config['MYSQL_DATABASE_DB'] = 'recipe_optimizer' 
app.config['MYSQL_DATABASE_HOST'] = '34.94.57.213'
mysql.init_app(app)

conn = mysql.connect()

app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "recipeoptimizer@gmail.com",
    MAIL_PASSWORD = 'a3b2c1a3b2c1' #just temp password
)

CORS(app)

mail = Mail(app)

@app.route('/', methods=['GET'])
def home():
    return "<h1> This is Recipe-Optimizer! </h1>"

@app.route('/get-recipes', methods=['GET'])
def getRecipes():
    db = dbop(conn)
    return(json.dumps(db.get_all_recipes()))

@app.route('/add-recipe', methods=['GET'])
def addRecipe():
    name = request.args.get('name')
    ingredients = request.args.get('ingredients')
    notes = request.args.get('notes')

    if(name == None or ingredients == None or notes == None):
        return "<div> check your parameters! </div>"

    db = dbop(conn)
    rc = db.add_recipe(name, ingredients, notes)

    if(rc < 0):
        return "<div> something bad happened. might be with ingredient's formatting </div>"

    return(str(rc))

@app.route('/delete-recipe', methods=['GET'])
def deleteRecipe():
    id = int(request.args.get('id'))

    if(id == None):
        return "<div> check your parameters! </div>"
    db = dbop(conn)
    ((db.delete_recipe(id)))
    return "<div> done! </div>"

@app.route('/get-schedule', methods=['GET'])
def getSchedule():
    db = dbop(conn)
    return(json.dumps(db.get_all_schedule()))

@app.route('/add-schedule', methods=['GET'])
def addSchedule():
    recipe_id = int(request.args.get('recipe_id'))
    notes = request.args.get('notes')

    if(recipe_id == None or notes == None):
        return "<div> check your parameters! </div>"

    db = dbop(conn)
    rc = db.add_schedule(recipe_id, notes)

    if(rc < 0):
        return "<div> something bad happened. might be with ingredient's formatting </div>"

    return(str(rc))

@app.route('/delete-schedule', methods=['GET'])
def deleteSchedule():
    id = int(request.args.get('id'))

    if(id == None):
        return "<div> check your parameters! </div>"

    db = dbop(conn)
    (db.delete_schedule(id))
    return "<div> Done! </div>"

@app.route('/recipe-schedule', methods=['GET'])
def recipeSchedule(jsonObj = True):
    db = dbop(conn)
    schedule = db.get_all_schedule()

    return_obj = []
    for s in schedule:
        recipe = db.recipe_by_id(s.get('recipe_id'))
        return_obj.append({
            "schedule_id" : s.get('id'),
            "recipe_id" : s.get('recipe_id'),
            "notes" : s.get('notes'),
            "recipe_name" : recipe.get('name'),
            "ingredients" : recipe.get('ingredients')
        })
            
    if(jsonObj):
        return(json.dumps(return_obj))
    else:
        return return_obj

@app.route('/ingredients-needed', methods=['GET'])
def ingredientsNeeded(jsonObj = True):
    schedule = recipeSchedule(jsonObj = False)
    allIngredients = []
    for s in schedule:
        allIngredients.extend(s.get('ingredients').split(','))

    allIngredients = set(allIngredients)

    return_obj = []
    for s in allIngredients:
        return_obj.append({
            "name" : s
        })

    if(jsonObj):
        return(json.dumps(return_obj))
    else:
        return(return_obj)

@app.route('/send-needed-ingredients/')
def sendNeededIngredients():

    neededIngredients = ingredientsNeeded(jsonObj = False)

    msg = Message("Ingredients Needed",
        sender="recipeoptimizer@gmail.com",
        recipients=["mzwang25@gmail.com"])

    msg.body = "Hi! You need these ingredients to make it work:\n"
    for i in neededIngredients:
        msg.body = msg.body + "- " + i.get("name") + "\n"
    mail.send(msg)
    return 'Mail sent!'

# run the app.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run(host="localhost", port=5000, debug=True)

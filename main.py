from flask import Flask
from flask import request
from flask_mail import Mail, Message
from flask_cors import CORS
from flaskext.mysql import MySQL
from db.dbop import dbop
from ingredient_parser import Ingredients_Parser
from sensitive import pwds
import re
import json

# EB looks for an 'app' callable by default.
app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = pwds.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = pwds.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = pwds.MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = pwds.MYSQL_DATABASE_HOST

mysql = MySQL()


app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = pwds.MAIL_USERNAME,
    MAIL_PASSWORD = pwds.MAIL_PASSWORD #just temp password
)

CORS(app)

mail = Mail(app)

mysql.init_app(app)

conn = mysql

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

    ip = Ingredients_Parser(ingredients)

    if(not ip.isValid):
        return "<div> something bad happened. might be with ingredient's formatting </div>"

    db = dbop(conn)
    rc = db.add_recipe(name, ip.clean_ingredients, notes)

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

    # We now every ingredient the user inputted
    # Now combine and add like measurements
    # This is a pretty bad algo I think but it works

    # coalesce like units into ingredientNames and ingredientAmounts
    ingredientNames = []
    ingredientAmounts = []
    for i in allIngredients:
        name = i.split('(')[0]
        val = i.split('(')[1][:-1]

        if(not i.split('(')[0] in ingredientNames):
            ingredientNames.append(name)
            insert = val.split(':')
            insert[0] = float(insert[0])
            ingredientAmounts.append(insert)
        else: #Another of the same name already found
            number = float(val.split(':')[0])
            unit = val.split(':')[1]

            foundOne = False
            for j in range(len(ingredientNames)):
                if(ingredientNames[j] == name and ingredientAmounts[j][1] == unit):
                    ingredientAmounts[j][0] += number
                    foundOne = True
                    break

            if(not foundOne):
                ingredientNames.append(name)
                insert = val.split(':')
                insert[0] = float(insert[0])
                ingredientAmounts.append(insert)

    #at this point: ingredientNames is list of names to be printed and amounts are coalesced units
    #like units have been grouped together

    return_obj = []
    ip = Ingredients_Parser("")
    for i in range(len(ingredientNames)):
        name = ingredientNames[i]
        num = float(ingredientAmounts[i][0])
        unit = ingredientAmounts[i][1]
        
        if(unit == "CM3"):
            return_obj.append({
                "name" : ingredientNames[i],
                "tbsp" : num / ip.conversionFactor['tbsp'][0],
                "tsp" : num / ip.conversionFactor['tsp'][0],
                "cups" : num / ip.conversionFactor['cups'][0],
                "li" : num / ip.conversionFactor['li'][0],
                "ml" : num / ip.conversionFactor['ml'][0],
                "gal" : num / ip.conversionFactor['gal'][0],
                "g" : 0,
                "oz" : 0,
                "p" : 0

            })
        elif (unit == "G"):
            return_obj.append({
                "name" : ingredientNames[i],
                "tbsp" : 0,
                "tsp" : 0,
                "cups" : 0,
                "li" : 0,
                "ml" : 0,
                "gal" : 0,
                "g" : num / ip.conversionFactor['g'][0],
                "oz" : num / ip.conversionFactor['oz'][0],
                "p" : 0
            })

        else:
            return_obj.append({
                "name" : ingredientNames[i],
                "tbsp" : 0,
                "tsp" : 0,
                "cups" : 0,
                "li" : 0,
                "ml" : 0,
                "gal" : 0,
                "g" : 0,
                "oz" : 0,
                "p" : num
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
    
@app.route('/prank')
def prank():
    for i in range (0,100):
        msg = Message("Ingredients Needed {}".format(i),
            sender="recipeoptimizer@gmail.com",
            recipients=["meganwang8392@gmail.com"])

        msg.body = "Try out https://front-recipe-optimizer-git-master.mzwang25.vercel.app/ #{}".format(i)
        mail.send(msg)

    return 'done!'

# run the app.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run(host="localhost", port=5000, debug=True)

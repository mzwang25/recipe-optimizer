import sqlite3

class dbop:
    def __init__(self):
        self.conn = sqlite3.connect('storage.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # Gets all the recipes in the db with an array of dictionaries
    def get_all_recipes(self):
        self.cursor.execute("SELECT * from recipes")
        rows = self.cursor.fetchall()
        dicts = []
        for r in rows:
            dicts.append({
                "id" : r[0],
                "name" : r[1],
                "ingredients" : r[2],
                "notes" : r[3]
            })

        return(dicts)

    # adds a recipe. If formatted correctly will return id. Returns -1 otherwise
    def add_recipe(self, name, ingredients, notes):
        name = name.upper()
        ingredients = ingredients.upper().split(',')

        for i in ingredients:
            if(' ' in i):
                return -1

        ingredients = str(ingredients)[1:-1].replace(' ', '').replace("'", '')

        query = "INSERT INTO recipes(name, ingredients, notes) VALUES('{}','{}','{}')"

        print(query.format(name, ingredients, notes))
        self.cursor.execute(query.format(name, ingredients, notes))
        self.conn.commit()
        return(self.cursor.lastrowid)

    #deletes recipe by id
    def delete_recipe(self, id):
        query = "DELETE FROM recipes where id = {}"
        self.cursor.execute(query.format(id))
        self.conn.commit()


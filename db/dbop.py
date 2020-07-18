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

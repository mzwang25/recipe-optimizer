from dbop import dbop

x = dbop()
x.get_all_recipes()

'''
import sqlite3

conn = sqlite3.connect('storage.db')

c = conn.cursor()
#c.execute( "INSERT INTO recipes(name, ingredients, notes) VALUES('Ice Cream', 'stuff', 'good')")
#c.execute( "DELETE FROM recipes WHERE id = 1")
#c.execute("SELECT * from recipes")

rows = c.fetchall()
print(rows)

conn.commit()

conn.close()
'''
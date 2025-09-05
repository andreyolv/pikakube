import sqlite3

connection = sqlite3.connect("pikakube.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")

cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
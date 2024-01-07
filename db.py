import sqlite3

con = sqlite3.connect('database.db')


con.execute("CREATE TABLE IF NOT EXISTS ideas (id INTEGER PRIMARY KEY, userid TEXT, ideatext TEXT)")
con.execute("CREATE TABLE IF NOT EXISTS resources (id INTEGER PRIMARY KEY, ideaid TEXT, resourceName TEXT, value TEXT)")


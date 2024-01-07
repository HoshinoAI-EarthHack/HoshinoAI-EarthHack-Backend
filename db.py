import sqlite3

con = sqlite3.connect('database.db', check_same_thread=False)


con.execute("CREATE TABLE IF NOT EXISTS ideas (id INTEGER PRIMARY KEY, userid INTEGER, ideatext TEXT, resourcesJSON TEXT)")
con.execute("CREATE TABLE IF NOT EXISTS resources (id INTEGER PRIMARY KEY, ideaid TEXT, resourceName TEXT, value TEXT)")


import sqlite3

con = sqlite3.connect('data.db')
c = con.cursor()
try:
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'content'")
    if not c.fetchone():
        with open('migration/init.sql') as sql:
            for statement in sql.read().split(';'):
                con.execute(statement)
                con.commit()
except Exception as ex:
    print(ex)
finally:
    c.close()
    con.close()

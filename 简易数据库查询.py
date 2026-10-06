import sqlite3
conn=sqlite3.connect("demo.db")
c=conn.cursor ()

c.execute("""CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,score REAL)""")

c.execute("INSERT INTO scores (name, score) VALUES ('山茶',88.5)")
c.execute("INSERT INTO scores (name, score) VALUES ('小明', 95)")
c.execute("INSERT INTO scores (name, score) VALUES ('阿花', 76)")
conn.commit()

c.execute("SELECT * FROM scores WHERE score > 80")
for row in c.fetchall():
    print(row)
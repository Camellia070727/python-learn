import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="123456",
    charset="utf8",
    db="douban"
)


c = conn.cursor()

#c.execute("TRUNCATE TABLE movies")
#conn.commit()

c.execute("SELECT * FROM movies LIMIT 10")
for row in c.fetchall():
    print(row)

conn.close
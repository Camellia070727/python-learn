import pymysql
conn = pymysql.connect(host="localhost", user="root", passwd="123456", charset="utf8", db="douban")
c = conn.cursor()

import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36"}

movies = []

for start in range(0,226,25):
    url = f"https://movie.douban.com/top250?start={start}"
    resp = requests.get(url,headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    for item in soup.find_all("div", class_="item"):
        title = item.find("span",class_="title").text
        rating = item.find("span", class_="rating_num").text
        c.execute("INSERT INTO movies (title, rating) VALUES (%s, %s)", (title, rating))

    time.sleep(1)

print(f"共爬到{len(movies)}部")

wb = Workbook()
ws = wb.active
ws.append(["电影名", "评分"])
for row in movies:
    ws.append(row)
wb.save("豆瓣Top250.xlsx")
print("已保存：豆瓣Top250.xlsx")

conn.commit()
c.execute("SELECT COUNT(*) FROM movies")
print("数据库里现在有：", c.fetchone(), "条")
conn.close()
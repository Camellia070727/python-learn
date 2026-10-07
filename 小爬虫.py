import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (windows NT 10.0; Win64; x64)Applewebk/537.36"}

all_quotes = []

import time

for page in range(1,11):
    url = f"https://quotes.toscrape.com/page/{page}/"
    resp = requests.get(url, headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    time.sleep(1)

    for q in soup.find_all("div",class_="quote"):
        text = q.find("span",class_="text").text
        author = q.find("small",class_="author").text
        all_quotes.append([text, author])

print(f"共获取{len(all_quotes)}条")

from openpyxl import Workbook

wb =Workbook()
ws = wb.active
ws.append(["名言", "作者"])
for row in all_quotes:
    ws.append(row)
wb.save("名言.xlsx")
print("已保存:名言.xlsx")
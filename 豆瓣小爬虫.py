import requests
import re
from bs4 import BeautifulSoup
import time

from openpyxl import Workbook
wb = Workbook()
count = 0
ws = wb.active
ws.append(["书名", "评分", "作者", "出版社", "出版年", "价格"])

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win 64; x64)AppleWebkit/537.36"}

for start in range(0, 250, 25):
    url = f"https://book.douban.com/top250?start={start}"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    print(f"--- 正在爬第{start // 25+1}页 ---")

    for box in soup. find_all("tr", class_="item"):
        title = box.find("div", class_="pl2").find("a")["title"]
        rating = box.find("span", class_="rating_nums").text
        info = box.find("p", class_="pl").text

        parts = [p.strip() for p in info.split("/")]
        import re
        last = re
        last = parts[-1]
        if re.search(r'\d+\.\d+', last):
            price = last
            body = parts[:-1]
        else:
            price = "无"
            body = parts

        author = body[0].strip()

        if len(body) >= 3:
            publisher = body[-2].strip()
        else:
            publisher = "未知"
        pub_year = body[-1].strip()

        ws.append([title, rating, author, publisher, pub_year, price])
        count += 1
        print(f" {title} {rating}")
    time.sleep(1)

wb.save("豆瓣图书Top250.xlsx")
print(f"\n完成！共抓取 {count} 条数据")
input("数据已保存至文件夹，按回车键退出...")
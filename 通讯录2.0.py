import sqlite3

conn = sqlite3.connect("contacts.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    name TEXT,
    phone TEXT
)
""")

while True:
    print("\n-----通讯录-----")
    print("1.添加")
    print("2.查询")
    print("3.删除")
    print("4.退出")
    choice = input("请选择(1/2/3/4)")
    if choice == "1":
        name = input("姓名：")
        phone = input("电话：")
        c.execute("INSERT INTO contacts (name,phone)VALUES (?, ?)",(name, phone))
        conn.commit()
    elif choice == "2":
        name = input("查谁：")
        c.execute("SELECT phone FROM contacts WHERE name = ?",(name,))
        row = c.fetchone()
        if row is None:
            print("通讯录里没有这个人")
        else:
            print(f"{name}的电话是{row[0]}")
    elif choice == "3":
        name = input("删谁：")
        c.execute("DELETE FROM contacts WHERE name = ?", (name,))
        conn.commit()
        print("已删除")
    elif choice == "4":
        print("再见")
        break
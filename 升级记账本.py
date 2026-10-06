import sqlite3

conn = sqlite3.connect("money.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    note TEXT
)
""")

while True:
    print("\n===== 记账本（数据库版）=====")
    print("1. 记一笔")
    print("2. 看余额")
    print("3. 退出")
    choice = input("请选择(1/2/3)：")

    if choice == "1":
        kind = input("收还是支（收/支）：")
        amount = float(input("金额："))
        note = input("备注：")
        c.execute("INSERT INTO records (type, amount, note) VALUES (?, ?, ?)", (kind, amount, note))
        conn.commit()
        print("已记下")

    elif choice == "2":
        balance = 0.0
        c.execute("SELECT type, amount FROM records")
        for kind, amount in c.fetchall():
            if kind == "收":
                balance = balance + amount
            else:
                balance = balance - amount
        print(f"当前余额：{balance}")

    elif choice == "3":
        print("再见！")
        break
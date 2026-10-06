# 我的记账本
while True:
    print("\n===== 记账本 =====")
    print("1. 记一笔")
    print("2. 查看流水和余额")
    print("3. 退出")
    choice = input("请选择(1/2/3)")

    if choice == "1":
        kind = input("收入还是支出？(收/支)：")
        amount = float(input("金额："))
        note = input("备注：")
        with open("money.txt", "a", encoding="utf-8") as f:
            f.write(f"{kind},{amount},{note}\n")
        print("已记下")
    elif choice == "2":
        balance = 0.0
        with open("money.txt", "r", encoding="utf-8") as f:
            for line in f:
                kind, amount, note = line.strip().split(",")
                amount = float(amount)
                if kind == "收":
                    balance = balance + amount
                    print(f"收入 +{amount} {note}")
                else:
                    balance = balance - amount
                    print(f"支出 -{amount} {note}")
            print(f"------ 当前余额：{balance}元------")
    elif choice == "3":
        print("再见！")
        break
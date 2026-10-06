contacts = {}

while True:
    print("n=====通讯录=====")
    print("1. 添加联系人")
    print("2. 查询联系人")
    print("3. 退出")
    choice = input("请选择(1/2/3)：")

    if choice == "1":
        name = input("姓名：")
        phone = input("电话：")
        contacts[name] = phone
    elif choice == "2":
        name = input("要查谁：")
        if name in contacts:
            print(f"{name}的电话是{contacts[name]}")
        else:
            print("通讯录里没有这个人")
    elif choice == "3":
        print("再见！")
        break
    else:
        print("输入无效，请重新输入")
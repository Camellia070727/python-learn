while True:
    print("\n=====待办清单=====")
    print("1. 查看清单")
    print("2. 添加事项")
    print("3. 退出")
    choice = input("请选择(1/2/3)")

    if choice == "1":
        with open("todos.txt", "r", encoding="utf-8") as f:
            for line in f:
                print(line.strip())
    elif choice == "2":
        item = input("要做什么：")
        with open("todos.txt", "a", encoding="utf-8") as f:
            f.write(item + "\n")
        print("已保存")
    elif choice == "3":
        print("再见！")
        break
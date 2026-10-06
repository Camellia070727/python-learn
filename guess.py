import random

answer = random.randint(1,100)
count = 0

print("我想好了一个1-100之间的数字，来猜猜看！")

while True:
    guess = int(input("你猜是几："))
    count = count + 1

    if guess == answer:
        print(f"恭喜你猜对了！答案就是{answer}")
        print(f"你一共猜了{count}次")
        break
    elif guess > answer:
        print("大了，往小了猜")
    else:
        print("小了，往大了猜")
    if count >= 7:
        print(f"你已经猜了7次了，次数用尽了，很遗憾你失败了，答案是{answer}")
        break
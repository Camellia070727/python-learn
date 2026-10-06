weight = float(input("请输入体重（公斤)："))
height_cm = float(input("请输入你的身高（厘米）："))
height = height_cm / 100

bmi = weight / (height * height)
print(f"你的BMI指数是：{bmi:.1f}")

if bmi < 18.5:
    print("偏瘦，多吃点，别熬夜")
elif bmi < 24:
    print("正常，继续保持")
elif bmi < 28:
    print("超重了，改动一动")
else:
    print("肥胖，开始认真锻炼吧")
scores = []

for i in range(30):
    s = float(input(f"请输入第{i+1}个成绩"))
    scores.append(s)

total = sum(scores)
avg = total / len(scores)
top = max(scores)

print(f"总分：{total}")
print(f"平均分：{avg:.1f}")
print(f"最高分：{top}")

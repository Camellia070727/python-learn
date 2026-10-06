import os

folder = input("把要处理的文件夹拖进去，然后回车：")

for name in os.listdir(folder):
    old_path = os.path.join(folder, name)
    new_path = os.path.join(folder, "作业" + name)
    os.rename(old_path, new_path)
    print(f"已重命名：{name} → 作业_{name}")
    
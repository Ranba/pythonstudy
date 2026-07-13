import os
import re

num_map = {
    "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9
}

def cn_to_int(s):
    if s.isdigit():
        return int(s)
    if s == "十":
        return 10
    if "十" in s:
        left, right = s.split("十", 1)
        tens = 1 if left == "" else num_map[left]
        ones = 0 if right == "" else num_map[right]
        return tens * 10 + ones
    return num_map[s]

folder = r"D:\你的文件夹"

for name in os.listdir(folder):
    m = re.search(r"第([一二三四五六七八九十零\d]+)集", name)
    if not m:
        continue

    old_num = m.group(1)
    n = cn_to_int(old_num)
    new_part = f"第{n:02d}集"
    new_name = name[:m.start()] + new_part + name[m.end():]

    old_path = os.path.join(folder, name)
    new_path = os.path.join(folder, new_name)

    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f"{name} -> {new_name}")
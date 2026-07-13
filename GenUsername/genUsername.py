import random
from itertools import cycle

def generate_readable_username(length):
    """生成符合发音规则的用户名"""
    # 常用元音和辅音定义（加权处理）
    vowels = {'a': 8, 'e': 9, 'i': 6, 'o': 7, 'u': 5, 'y': 2}
    consonants = {
        'b':7, 'c':6, 'd':8, 'f':5, 'g':5, 'h':5, 
        'j':4, 'k':4, 'l':7, 'm':7, 'n':8, 'p':6,
        'r':8, 's':9, 't':9, 'v':4, 'w':3, 'z':3
    }

    # 常见双字母组合
    common_pairs = [
        'th', 'tr', 'br', 'st', 'sh', 'ch', 'ph', 
        'gh', 'ng', 'nt', 'nd', 'pr', 'pl', 'cl'
    ]

    # 随机选择生成模式：交替模式(60%)或随机组合(40%)
    pattern = random.choices(
        ['alternating', 'random'], 
        weights=[60, 40]
    )[0]

    username = []
    position = 0
    
    while len(username) < length:
        # 每3-4个字符尝试插入常见组合
        if len(username) >= 2 and position > 2:
            if random.random() < 0.3:  # 30%概率插入组合
                pair = random.choice(common_pairs)
                if len(username) + len(pair) <= length:
                    username.extend(list(pair))
                    position = 0
                    continue

        if pattern == 'alternating':
            # 元音/辅音交替模式
            pool = vowels if (position % 2 == 1) else consonants
        else:
            # 随机混合模式
            pool = {**vowels, **consonants} if random.random() < 0.4 else (
                vowels if random.random() < 0.5 else consonants
            )

        # 加权随机选择
        letters, weights = zip(*pool.items())
        char = random.choices(letters, weights=weights, k=1)[0]
        
        username.append(char)
        position += 1

        # 防止重复字符超过2次
        if len(username) >= 2 and username[-1] == username[-2]:
            if len(username) >=3 and username[-3] == username[-2]:
                username.pop()
                position -= 1

    # 确保首字母是辅音（更符合常见发音）
    if username[0] in vowels:
        username[0] = random.choices(list(consonants.keys()), 
                                   weights=list(consonants.values()))[0]

    return ''.join(username[:length])

def main():
    while True:
        try:
            length = int(input("请输入用户名长度（6-12位）："))
            if 6 <= length <= 12:
                break
            else:
                print("长度必须在6-12位之间。")
        except ValueError:
            print("请输入整数。")
    
    while True:
        try:
            num_usernames = int(input("请输入生成的用户名数量："))
            if num_usernames > 0:
                break
            else:
                print("数量必须大于0。")
        except ValueError:
            print("请输入整数。")
    
    usernames = [generate_readable_username(length) for _ in range(num_usernames)]
    
    print("\n生成的用户名如下：")
    for i, username in enumerate(usernames, start=1):
        print(f"{i}. {username}")

if __name__ == "__main__":
    main()

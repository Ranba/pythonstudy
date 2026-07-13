import secrets
import string
import argparse
import sys


def generate_secure_random_token(length=32):
    """
    生成安全的随机字符串，用于Token、Auth Key等敏感用途。
    
    使用secrets模块生成密码学安全的随机字符串，包含：
    - 大写字母 (A-Z)
    - 小写字母 (a-z)
    - 数字 (0-9)
    - 安全的特殊字符 (!@#$%^&*+-=)
    
    注意：
    - 字符串不会以符号开头，确保系统兼容性
    - 移除了可能导致问题的符号：空格、引号、括号、花括号、方括号、竖线、分号、冒号、逗号、句号、问号、反斜杠、斜杠、波浪号等
    
    参数:
        length (int): 生成的字符串长度，默认为32位
        
    返回:
        str: 安全的随机字符串
    """
    # 定义字符集：大小写字母、数字和安全的特殊字符
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    # 只使用安全的特殊字符，移除可能导致兼容性问题的符号
    safe_special_characters = '!@#$%^&*+-='
    
    # 所有字符集
    all_characters = uppercase_letters + lowercase_letters + digits + safe_special_characters
    
    # 字母数字字符集（用于开头）
    alphanumeric_characters = uppercase_letters + lowercase_letters + digits
    
    # 确保第一个字符不是符号
    first_char = secrets.choice(alphanumeric_characters)
    
    # 生成剩余字符
    remaining_chars = ''.join(secrets.choice(all_characters) for _ in range(length - 1))
    
    return first_char + remaining_chars


def generate_secure_token_with_guaranteed_types(length=32):
    """
    生成安全的随机字符串，保证包含所有类型的字符。
    
    这个版本确保生成的字符串至少包含：
    - 1个大写字母
    - 1个小写字母
    - 1个数字
    - 1个特殊字符
    剩余字符从所有字符集中随机选择。
    
    注意：
    - 字符串不会以符号开头，确保系统兼容性
    - 移除了可能导致问题的符号
    
    参数:
        length (int): 生成的字符串长度，默认为32位
        
    返回:
        str: 安全的随机字符串，保证包含所有字符类型
    """
    if length < 4:
        raise ValueError("长度必须至少为4位，以确保包含所有字符类型")
    
    # 定义字符集
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    safe_special_characters = '!@#$%^&*+-='
    
    all_characters = uppercase_letters + lowercase_letters + digits + safe_special_characters
    alphanumeric_characters = uppercase_letters + lowercase_letters + digits
    
    # 确保每种类型至少有一个字符
    characters = [
        secrets.choice(uppercase_letters),
        secrets.choice(lowercase_letters),
        secrets.choice(digits),
        secrets.choice(safe_special_characters)
    ]
    
    # 填充剩余字符
    for _ in range(length - 4):
        characters.append(secrets.choice(all_characters))
    
    # 使用secrets模块进行密码学安全的洗牌
    secrets.SystemRandom().shuffle(characters)
    
    # 确保第一个字符不是符号
    if characters[0] in safe_special_characters:
        # 找到第一个非符号字符
        for i in range(1, len(characters)):
            if characters[i] not in safe_special_characters:
                characters[0], characters[i] = characters[i], characters[0]
                break
        else:
            # 如果所有其他字符都是符号（不太可能），替换第一个字符为字母数字
            characters[0] = secrets.choice(alphanumeric_characters)
    
    return ''.join(characters)


def generate_hex_token(length=32):
    """
    生成十六进制的安全随机字符串。
    
    适用于需要十六进制格式的Token或Key。
    十六进制字符串只包含0-9和a-f，天然不包含特殊字符。
    
    参数:
        length (int): 生成的字符串长度（字符数），默认为32位
        
    返回:
        str: 十六进制的安全随机字符串
    """
    # 计算需要的字节数（每个十六进制字符代表4位，2个字符=1字节）
    byte_length = (length + 1) // 2
    random_bytes = secrets.token_bytes(byte_length)
    hex_string = random_bytes.hex()
    
    # 截取到指定长度
    return hex_string[:length]


def generate_base64_token(length=32):
    """
    生成Base64编码的安全随机字符串。
    
    适用于需要Base64格式的Token或Key。
    URL安全的Base64只包含字母、数字、-和_，天然兼容性好。
    
    参数:
        length (int): 生成的基础随机字节数，默认为32字节
        
    返回:
        str: Base64编码的安全随机字符串
    """
    random_bytes = secrets.token_bytes(length)
    import base64
    # 使用urlsafe_b64encode生成URL安全的Base64字符串
    # 只包含字母、数字、-和_
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(
        description='生成安全的随机字符串，用于Token、Auth Key等敏感用途',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s                    # 生成32位默认随机字符串
  %(prog)s -l 64              # 生成64位随机字符串
  %(prog)s -t guaranteed      # 生成保证包含所有字符类型的字符串
  %(prog)s -t hex             # 生成十六进制字符串
  %(prog)s -t base64          # 生成Base64字符串
  %(prog)s -c 5               # 生成5个随机字符串

注意:
  - 所有生成的字符串都不会以特殊符号开头
  - 特殊字符只使用安全的符号：!@#$%^&*+-=
  - hex和base64模式天然兼容性好，推荐使用
        '''
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        default=32,
        help='生成的字符串长度（默认：32）'
    )
    
    parser.add_argument(
        '-t', '--type',
        choices=['default', 'guaranteed', 'hex', 'base64'],
        default='default',
        help='生成的字符串类型：default（默认）、guaranteed（保证包含所有字符类型）、hex（十六进制）、base64（Base64编码）'
    )
    
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=1,
        help='生成的字符串数量（默认：1）'
    )
    
    parser.add_argument(
        '-n', '--no-newline',
        action='store_true',
        help='输出时不添加换行符'
    )
    
    args = parser.parse_args()
    
    # 根据类型选择生成函数
    generators = {
        'default': generate_secure_random_token,
        'guaranteed': generate_secure_token_with_guaranteed_types,
        'hex': generate_hex_token,
        'base64': generate_base64_token
    }
    
    generator = generators[args.type]
    
    # 生成指定数量的随机字符串
    results = []
    for _ in range(args.count):
        try:
            token = generator(args.length)
            results.append(token)
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    # 输出结果
    if args.no_newline:
        print(results[0], end='')
    else:
        for i, result in enumerate(results):
            if args.count > 1:
                print(f"{i + 1}. {result}")
            else:
                print(result)


if __name__ == '__main__':
    main()
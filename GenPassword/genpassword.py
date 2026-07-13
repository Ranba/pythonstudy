# -*- coding:utf-8 -*-

import string
import random

print("模式1：大小写、数字组合；")
print("模式2：大小写、数字、特殊符号组合；")
print("请选择模式：")
m = int(input())

print("请输入生成密码长度，最少8位：")
length = int(input())

def GenPassm1(length):
    if length < 2:  # 确保长度足够
        raise ValueError("密码长度必须至少为2")
    first_char = random.choice(string.ascii_letters)  # 确保以字母开头
    remaining_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
    return first_char + remaining_chars

def GenPassm2(length):
    if length < 2:  # 确保长度足够
        raise ValueError("密码长度必须至少为2")
    first_char = random.choice(string.ascii_letters)  # 确保以字母开头
    remaining_chars = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length - 1))
    return first_char + remaining_chars

if __name__ == "__main__":
    if length < 8:
        length = 8  # 确保密码长度至少为8

    if m == 1:
        for _ in range(5):  # 生成5个密码
            print(GenPassm1(length))

    elif m == 2:
        for _ in range(5):  # 生成5个密码
            print(GenPassm2(length))

    else:
        print("无效的模式选择！")
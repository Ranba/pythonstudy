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
    return ''.join(random.sample(string.ascii_letters,length))

def GenPassm2(length):
    return ''.join(random.sample(string.ascii_letters+string.punctuation,length))

if __name__ == "__main__":
    if length < 8:
        len = 8
    else:
        len = length

    if m == 1:
        print(GenPassm1(len))

    if m == 2:
        print(GenPassm2(len))
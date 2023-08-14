# -*- coding: utf-8 -*-

m = int(input("总分期金额："))
n = int(input("期数："))
a = float(input("每期利率%："))
s = m*a*n/100
print(s)
m1 = m/n
print(m1)
nn = (1+n)*n/2
print(nn)
x = 12*((s/m1)/nn)
print(x)

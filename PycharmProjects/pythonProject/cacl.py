import re

def checkInput(regExp,str):
    res = re.search(regExp,str)
    if res:
        return True
    else:
        return False


ctype = input('请输入类型编码： ')
while checkInput('^[1,2][3,4,5,6]$',ctype) == False:
    print(ctype,'输入错误')
    ctype = input('请输入2位数类型编码：')
    if checkInput('^[1,2][3,4,5,6]$',ctype) == True:
        continue
print('输入正确')

cnumber = input('请输入后四位数字： ')
while checkInput('^\d{4}$',cnumber) == False:
    print(cnumber,'输入错误')
    cnumber = input('请输入后四位数字：')
    if checkInput('^\d{4}$',cnumber) == True:
        continue
print('输入正确')

bspec = input('请输入2位特殊码： ')
while checkInput('^\d{2}$',bspec) == False:
    print(bspec,'输入错误')
    bspec = input('请输入2位特殊码：：')
    if checkInput('^\d{2}$',bspec) == True:
        continue
print('输入正确')
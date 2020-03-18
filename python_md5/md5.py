#-*-coding:UTF-8–*-
import hashlib

# 待加密信息
def md5(str):
	import hashlib
# 创建md5对象
	m = hashlib.md5()
	b = str.encode(encoding='utf-8')
	m.update(b)
	return m.hexdigest()
h=','
pwfile = open('./mobile.csv')
pw = pwfile.read().splitlines()
print(pw)
md5file = open('./mobilemd5.csv','a+')
for d in pw:
    print(md5(d))
    md5file.write((d)+(h)+md5(d))
    md5file.write('\n')
pwfile.close()
md5file.close()
import hashlib


#MD5加密
def md5_key(arg):
    hash = hashlib.md5()
    hash.update(arg.encode(encoding='UTF-8'))
    return hash.hexdigest()

file_name = "pythonforshortenurl\m.txt"
with open(file_name) as file_object:
    for line in file_object:
        line1 = line.rstrip()
        md5_string = md5_key(line1)
        print(md5_string)
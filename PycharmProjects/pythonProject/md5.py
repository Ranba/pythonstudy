import hashlib

ln = input("input: ")
hl =hashlib.md5()
hl.update(ln.encode("utf-8"))
mstr = hl.hexdigest()
print(mstr)
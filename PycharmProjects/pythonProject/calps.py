import sqlite3
import hashlib

conn = sqlite3.connect('./cinfo.db')
cur =conn.cursor()

lastnum = input("lastNumber: ")

def md5ln(ln):
    hl = hashlib.md5()
    hl.update(ln.encode("utf-8"))
    mstr = hl.hexdigest()
    return mstr
    print(mstr)

mln = md5ln(lastnum)

sqls = "select * from CardInfo where LastNumber='{}'".format(mln)
cur.execute(sqls)
data = list(cur.fetchone())
cur.close()
conn.close()

ct = data[0]
sn = data[2]

key = 165461+(ct*10000)+(sn+95500)
print(key)
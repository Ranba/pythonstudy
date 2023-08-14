import sqlite3
import hashlib

conn = sqlite3.connect('./cinfo.db')
cur =conn.cursor()

# 新建数据库文件和表
# sqltexttablemenu = '''CREATE TABLE cardinfo
#                         (CardType NUMBER,
#                         LastNumber TXET,
#                         SpecNumber NUMBER);'''
# cur.execute(sqltexttablemenu)
# conn.commit()





# 插入数据
def saveCardInfo(ct,ln,sn):
    # print(ct)
    # print(ln)
    # print(sn)
    cardinfodata = (ct,ln,sn)
    cur.execute("INSERT INTO cardinfo(CardType, LastNumber, SpecNumber) VALUES(?,?,?)", cardinfodata)
    conn.commit()

def md5ln(ln):
    hl = hashlib.md5()
    hl.update(ln.encode("utf-8"))
    mstr = hl.hexdigest()
    return mstr
    print(mstr)

cardtype = int(input("Type: "))
lastnumber = input("LastNumber: ")
mln = md5ln(lastnumber)
specnumber = int(input("SpecNumber: "))
saveCardInfo(cardtype,mln,specnumber)

cur.execute("select * from cardinfo")
print(cur.fetchall())
conn.close()



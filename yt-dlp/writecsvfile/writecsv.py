import csv

phone = input("输入号码：" )

with open('number.csv', 'a') as file:
    writer = csv.writer(file)
    writer.writerow(phone)
    i = 1
    while i < 10:
        phone = int(phone)
        phone = phone + i
        writer.writerow(str(phone))
        i += 1
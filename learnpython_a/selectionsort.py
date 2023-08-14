a = [5,4,3,2,1]
min_index  = 0
for i in range(1,len(a)):
    if a[min_index] > a[i]:
        min_index = i
    print(min_index)
a[0],a[min_index] = a[min_index],a[0]
print(a)
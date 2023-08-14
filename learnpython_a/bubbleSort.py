def bubbleSort(list):
    for i in range(len(list)):
        for j in range(len(list)-i-1):
            if list[j] > list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]
    return list

nums=[1,345,65,7,988,1024]
bubbleSort(nums)
print(nums)
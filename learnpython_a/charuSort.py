def charuSort(list):
    for i in range(len(list)):
        for j in range(1,len(list)):
            if list[j-1] > list[j]:
                list[j-1],list[j] = list[j],list[j-1]
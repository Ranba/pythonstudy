import random
lis = []
for i in range(3):
	n = random.randint(1,999)
	lis.append(n)
print("Random Numbers:",lis)

for i in range(len(lis)):
	for j in range(len(lis)):
		if lis[i] < lis[j]:
			lis[i],lis[j] = lis[j],lis[i]
print("Sort Numbers:",lis)
import random

def bubble_sort(nums):
	for i in range(len(nums) - 1):
		for j in range(len(nums) - i -1):
			if nums[j] > nums[j + 1]:
				nums[j],nums[j + 1] = nums[j + 1],nums[j]
	return nums

lis = []
x = input("Input Number of Numbers:")
for i in range(int(x)):
	n = random.randint(1,999)
	lis.append(n)
print("Random Numbers:",lis)

bubble_sort(lis)
print("Sort Numbers:",lis)

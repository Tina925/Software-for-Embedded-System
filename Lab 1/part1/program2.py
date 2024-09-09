import random

numbers = []

for x in range(10):
    number = random.randrange(1, 100)
    numbers.append(number)
    numbers = sorted(numbers)
print (numbers)

newNum = input("Enter number: ")
newList=[]
for x in numbers:
    if (x) < int(newNum):
        newList.append(x)
        newList = sorted(newList)
print (newList)
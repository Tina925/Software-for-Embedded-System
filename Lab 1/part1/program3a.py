number = input("How many Fibonacci numbers would you like to generate? ")
List = []
firstNum = 0
secNum = 1
i = 0
if int(number)>1:
    List.append(1)
while i < int(number)-1:
    i+=1
    thirdNum = firstNum + secNum
    firstNum = secNum
    secNum = thirdNum
    List.append(thirdNum)
print(List)
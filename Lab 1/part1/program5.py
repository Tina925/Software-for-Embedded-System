class Find:
    def __init__(self, List):
        self.List = List
    def findIndex(self, target):
        pair = []
        index = {}
        for x, num in enumerate(self.List):
            #print(f"{x}, {num}")
            secondNum = target - num
            if secondNum in index:
                pair.append((index[secondNum], x))
            index[num] = x
        return pair
    
List = [10, 20, 10, 40, 50, 60, 70]

target = int(input("What is your target number? "))

find = Find(List)

result = find.findIndex(target)
#print(result)
for index1, index2 in result:
    print(f"index1={index1}, index2={index2}")
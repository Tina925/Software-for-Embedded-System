dict = {
  "Alex": "07/23/2002",
  "Christina": "10/17/2002",
  "Tina": "09/25/2001",
  "Edmund":"02/10/2002",
  "Freya": "02/09/2001"
}

print("Welcome to the birthday dictionary. We know the birthdays of: ")
for name in dict.keys():
    print(name)
name = input("Whose birthday do you want to look up?\n")
if name in dict:
    birth = dict[name]
    print(name + "'s birthday is "+birth)

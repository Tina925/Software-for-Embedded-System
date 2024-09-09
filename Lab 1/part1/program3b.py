import random

number = random.randrange(0, 10)
print(number)
guess1 = input("Enter your guess: ")
if int(guess1) == number:
    print("You Win!")
else:
    guess2 = input("Enter your guess: ")
    if int(guess2) == number:
        print("You Win!")
    else:
        guess3 = input("Enter your guess: ")
        if int(guess3) == number:
            print("You Win!")
        else:
            print("You Lose!")
import random
def hangman():
    word = random.choice(["pugger", "littlepugger", "bigpugger", "tiger", "superman", "thor", "kane", "ashu", "sumit", "aman", "umesh"])
    validletters = 'abcdefghijklmnopqrstuvwxyz'
    turn = 10
    guessmade = ''
    while len(word) > 0:
        main = ""
        missed = 0
        for letter in word:
            if letter in guessmade:
                main = main+letter 
            else:
                main = main + "_" + " "
        if main == word:
            print(main)
            print("You win")
            break
        print("guess the word:", main)
        guess = input()

        if guess in validletters:
            guessmade = guessmade + guess
        else:
            print("enter a valid character")
            guess = input()
        if guess not in word:
            turns = turns - 1
            if turns == 9:
                print("9 turns left")
                print(" ----- ")
            if turns == 8:
                print("8 turns left")
                print(" ----- ")
                print("   0   ")
            if turns == 7:
                print("7 turns left")
                print(" ----- ")
                print("   0   ")
                print("   1   ")

name = input("Enter your name")
print("welcome" , name )
print("---------")
print("try to guess the word in less than 10 try")
hangman()
print()

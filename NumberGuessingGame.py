#NumberGuessingGame.py
#Created by Sky Floyd
#Final Project - CIT1100
import random
from datetime import datetime
import sqlite3
from contextlib import closing
conn = sqlite3.connect("GuessingGameDB.sqlite")
conn.row_factory = sqlite3.Row

def displayMenu():
    menu = """
__________________________________________


                    Random Number Guessing Game
                    
__________________________________________

How to play:

A random number from 1 to 100 will be generated.
Guess and you’ll be told if you are high or low.
Try guess in as little guesses as possible.
Good luck!

Choose menu option:

0. Quit
1. Play
2. Leaderboard
"""
    print(menu)

def playGame():
    myScoreList = []
    again = "y"
    while again.lower() == "y":         # As long as the play wants to keep going the game will continue
        ranNum = random.randint(1,100)
        score = 1
        strike = 0
        while True:         # Run the actual game
            print("\nGuess a number from 1 to 100\n")
            guess = input("Guess: ")
            if guess.isnumeric():       # Makes sure that entry is a number
                if int(guess) > 100 or int(guess) < 1:      # If outside the bounds of the game then penalize
                    print("Please enter a valid number.")
                    strike += 1
                    if strike < 3:      # This is just a warning
                        print("If this keeps happening you will be penalized.")
                    elif strike >= 3:       # 3 strikes your out
                        print("I warned you. You will now get an extra point added to your score")
                        score += 1
                elif int(guess) < (ranNum - 10):        #Actual guess
                    print("Too low!")
                    score += 1
                elif int(guess) < ranNum and int(guess) >= (ranNum - 10):       #Actual guess
                    print("Too low, but very close.")
                    score += 1
                elif int(guess) > (ranNum + 10):        #Actual guess
                    print("Too high!")
                    score += 1
                elif int(guess) > ranNum and int(guess) <= (ranNum + 10):       #Actual guess
                    print("Too high, but very close.")
                    score += 1
                elif int(guess) == ranNum:      #Guess is correct
                    print("\nYour final score is " + str(score) + "!\n")
                    myScoreList.append(score)
                    print("Here are all of your scores for this session")
                    print(myScoreList)
                    break
            else:       # If not a number go here and penalize
                print("Please enter a number.")
                strike += 1
                if strike < 3:      # This is just a warning
                    print("If this keeps happening you will be penalized.")
                elif strike >= 3:        # 3 strikes your out
                    print("I warned you. You will now get an extra point added to your score")
                    score += 1
        print()         # This is when the game has completed and the user is prompeted to play again
        again = input("Would you like to play again? (y/n) ")
    print()         # This is when the player does NOT want to continue playing
    print("Thank you for playing!\n")
    entryLB(myScoreList)

def entryLB(scoreList):
    username = input("Please enter a username for the Leaderboard (3-10 characters) ")
    while len(username) > 10 or len(username) < 3:       # For as long as the user doesn't input a valid name they will keep being prompted to do it again
        print("\nUsername length isn't valid.\n")
        username = input("Please enter a username for the Leaderboard (3-10 characters) ")
    scoreList.sort()
    print("\nHere are " + username + "'s scores for the session, from best to worst.")
    print("The best score will be entered into the Leaderboard\n")
    print(scoreList)
    today = str(datetime.today().strftime(' %Y-%m-%d %H:%M '))
    with closing(conn.cursor()) as c:
        sql = "INSERT INTO Leaderboard (username, highScore, date) VALUES (?,?,?)"
        c.execute(sql, (username, scoreList[0], today))
        conn.commit()
    
    

def displayLB():
    try:
        limit = input("How many entries do you want to see (ex. 10)? ")
        print("\nPlease note there may not be that many entries.")
        with closing(conn.cursor()) as c:
            query = "SELECT * FROM Leaderboard ORDER BY highScore LIMIT ?"
            c.execute(query, (limit,))
            leaderboard = c.fetchall()
    except sqlite3.OperationalError as e:
        print("Error reading database -", e)
        leaderboard = None

    if leaderboard != None:
        counter = 1
        print("\n\nPlace | Username | HighScore | Date\n")
        for entry in leaderboard:
            print(counter, "  |  ", entry[1], "     |     ", entry[2], "     |     ", entry[3])
            counter += 1
        print()
        input("Press ENTER to continue")
        
    
def main():
    displayMenu()
    while True:
        choice = input("Enter Choice: ")
        if choice == "1":
            playGame()
        elif choice == "2":
            displayLB()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Not a valid command. Please try again. \n")
        displayMenu()

if __name__ == "__main__":
    main()
        

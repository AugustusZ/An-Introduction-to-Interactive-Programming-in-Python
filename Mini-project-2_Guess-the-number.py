## http://www.codeskulptor.org/#user38_QVmNcrNChD_10.py

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# default assignment
range_upper_limit = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global remaining_guesses
    secret_number = random.randrange(0,range_upper_limit)
    remaining_guesses = int(math.ceil(math.log(range_upper_limit + 1, 2)))
    # print range_upper_limit
    print
    print ">>>>>>>>>>>>> NEW GAME <<<<<<<<<<<<<"
    print "===================================="
    print "The Range of Secret number: [0," + str(range_upper_limit) + ")"
    print "The number of allowed guesses:  " + str(remaining_guesses)
    print "------------------------------------"
    pass

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range_upper_limit
    range_upper_limit = 100 
   
    # reset the secret number in the desired range
    new_game()
    pass

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range_upper_limit
    range_upper_limit = 1000
    
    # reset the secret number in the desired range
    new_game()
    pass
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_guesses
    
    # first of all, check whether input is a non-negative int
    if not guess.isdigit():
        print "Input a non-negative integer please!"
        print
        return None
    
    guess_number = int(guess)
    print "Guess was " + str(guess_number) + "."
    
    if secret_number > guess_number:
        remaining_guesses -= 1
        print "Higher!"
        if remaining_guesses > 1:
            print "You still have", remaining_guesses, "guesses left."
            print
        elif remaining_guesses == 1:
            print "And your last guess goes to..."
            print
        else:
            print
            print "GAME OVER! The secret number is " + str(secret_number) + "."
            print "Don't be sad! Just have another try!"
            print "===================================="
            print 
            new_game()
    
    elif secret_number < guess_number:
        remaining_guesses -= 1
        print "Lower!"
        if remaining_guesses > 1:
            print "You still have", remaining_guesses, "guesses left."
            print
        elif remaining_guesses == 1:
            print "And your last guess goes to..."
            print
        else:
            print
            print "GAME OVER! The secret number is " + str(secret_number) + "."
            print "Don't be sad! Just have another try!"
            print "===================================="
            print       
            new_game()
            
    else:
        print "Correct!"
        print "************* YOU WIN! *************"
        print "===================================="
        print
        new_game()
    pass
 
# create frame
frame = simplegui.create_frame("Guess the Number",300,300)


# register event handlers for control elements and start frame
frame.add_input("Input your guess here:",input_guess,100)
frame.add_button("NEW GAME",new_game)

# additional buttons
frame.add_button("Range: 0 - 100",range100)
frame.add_button("Range: 0 - 1000",range1000)


frame.start()
# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

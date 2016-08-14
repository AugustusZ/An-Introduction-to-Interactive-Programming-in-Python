## http://www.codeskulptor.org/#user38_6OLLFj9Cpu_0.py

import random

# name to number
def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return -1
    
# number to name
def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return number


def rpsls(player_choice):
    # 1
    print 'Player chooses ' + player_choice
    player_number = name_to_number(player_choice)

    # 2
    comp_number = random.randrange(0,5,1)
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses ' + comp_choice

    # 3
    diff = (comp_number - player_number) % 5
    if diff <= 2 and diff > 0:
        print 'Computer wins!'
    elif diff == 0:
        print 'Player and computer tie!'
    else:
        print 'Player wins!'
    print
        
rpsls('rock')
rpsls('Spock')
rpsls('paper')
rpsls('lizard')
rpsls('scissors')
    

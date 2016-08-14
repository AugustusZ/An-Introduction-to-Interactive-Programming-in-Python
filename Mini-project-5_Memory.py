## http://www.codeskulptor.org/#user38_LHggECXCiK_15.py

# implementation of card game - Memory

import simplegui
import random

# init
deck = []
turns = 0
FACE_DOWN = False
FACE_UP = True
exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
state = 0
exposed_idx_stack = [None,None]

# style
TEXT_COLOR = 'Yellow'
TEXT_OFFSET = 10
TEXT_PT = 50

# helper function to initialize globals
def new_game():
    global deck
    global turns
    global state
    global exposed
    idx_exposed = []
    turns = 0
    state = 0
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

    label.set_text("Turns = " + str(turns))
    
    half_deck = range(0,8)
    
    random.shuffle(half_deck)
    half_deck_1 = list(half_deck)
    random.shuffle(half_deck)
    half_deck_2 = list(half_deck)
    
    deck = half_deck_1 + half_deck_2
    random.shuffle(deck)
    print deck

def expose(new_idx):
    exposed_idx_stack.pop(0)
    exposed_idx_stack.append(new_idx)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    idx = pos[0] // 50
    print idx
    
    global state
    global turns
    
    # State 0 corresponds to the start of the game
    if state == 0:
        exposed[idx] = True
        expose(idx)
        state = 1
    
    # State 1 corresponds to a single exposed unpaired card
    elif state == 1:
        if not exposed[idx]:
            exposed[idx] = True
            expose(idx)            
            state = 2
            turns += 1
        
    # State 2 corresponds to the end of a turn    
    else:
        if not exposed[idx]:
                        
            if deck[exposed_idx_stack[0]] != deck[exposed_idx_stack[1]]:
                exposed[exposed_idx_stack[0]] = False
                exposed[exposed_idx_stack[1]] = False  
            else:
                exposed[exposed_idx_stack[0]] = True
                exposed[exposed_idx_stack[1]] = True
                
            expose(idx)
            exposed[idx] = True
            state = 1
            
    
    if not (False in exposed):
        label.set_text("Turns = " + str(turns) + " and you win!")
    else:
        label.set_text("Turns = " + str(turns))
    
                               
# cards are logically 50x100 pixels in size    
def draw(canvas):   
    for idx,digit in enumerate(deck):
        if exposed[idx]:
            text_pos = TEXT_OFFSET + idx * 50
            canvas.draw_text(str(digit), (text_pos,65),TEXT_PT,TEXT_COLOR,'monospace')
        else:
            L = idx * 50
            R = idx * 50 + 50
            U = 0
            D = 100
            rect_pos = [[L,U],[L,D],[R,D],[R,U]]
            canvas.draw_polygon(rect_pos, 1, 'White', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
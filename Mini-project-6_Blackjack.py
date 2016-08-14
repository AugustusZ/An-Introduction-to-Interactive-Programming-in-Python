## http://www.codeskulptor.org/#user38_LFWimF1jw8_28.py

# Mini-project #6 - Blackjack
# Features:
# 0 Overlaid cards with shadow
# 1 Shadow of texts
# 2 Text alignment
# 3 Shortcuts (try 'D','H','S')

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

INTERVAL_X = -30
INTERVAL_Y = 120
MARGIN_X = 50
MARGIN_Y = 220
SHADOW_OFFSET = 1
TEXT_PT = 40
BIG_TEXT_PT = 100
BIG_TEXT_OFFSET = 20
SMALL_TEXT_PT = 20


# initialize some useful global variables
in_play = False
outcome = ""
score = 0
during_the_middle_of_a_round = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        L = pos[0] #- SHADOW_OFFSET
        U = pos[1] + 1
        D = U + CARD_SIZE[1] - 2
        canvas.draw_line((L, U), (L, D), 2, 'grey')
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []
        
    def __str__(self):        
        card_str = "Hand contains:"
        for card in range(len(self.card_list)):
            card_str += ' ' + self.card_list[card].suit + self.card_list[card].rank
        return card_str + '.'
        
    def add_card(self, card):
        self.card_list.append(card)
        
    def get_value(self):
        hand_value = 0
        num_of_A = 0
       
        for card in range(len(self.card_list)):
            hand_value += VALUES[self.card_list[card].rank]
            if self.card_list[card].rank == 'A':
                num_of_A += 1
            
        if num_of_A == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
    
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):

        canvas.draw_image(card_images, card_loc, CARD_SIZE, pos, CARD_SIZE)
        
       
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.card_list.append(Card(suit, rank))        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)
        
    def deal_card(self):
        return self.card_list.pop()
            
    def __str__(self):
        card_str = "Deck contains:"
        for card in range(len(self.card_list)):
            card_str += ' ' + self.card_list[card].suit + self.card_list[card].rank
        return card_str + '.'


#define event handlers for buttons
def deal():
    global dealer_msg, player_msg, outcome, in_play, new_deck, dealer, player, score, during_the_middle_of_a_round

    new_deck = Deck()
    new_deck.shuffle()
    
    dealer = Hand()
    dealer.add_card(new_deck.deal_card())    
    dealer.add_card(new_deck.deal_card())

    player = Hand()
    player.add_card(new_deck.deal_card())
    player.add_card(new_deck.deal_card())
    print "Dealer's " + dealer.__str__()
    print "Player's " + player.__str__()
        
    if during_the_middle_of_a_round:
        outcome = 'Lose.  Hit/stand?'
        score -= 1
        during_the_middle_of_a_round = False
    else:
        outcome = "Hit or stand?"
        dealer_msg = ''
        player_msg = ''
    # your code goes here
    
    in_play = True
    during_the_middle_of_a_round = True

def hit():
    global in_play, outcome, dealer_msg, player_msg, score, during_the_middle_of_a_round
    if during_the_middle_of_a_round:
        # if the hand is in play, hit the player
        if in_play:
            hit_card = new_deck.deal_card()
    #        print "HIT CARD:"
    #        print hit_card
    #        print       
            player.add_card(hit_card)
    #        print "PLAYER'S VALUE:"
    #        print player.get_value()
    #        print 
            if player.get_value() > 21:
                player_msg = "BSTD"
                dealer_msg = "WIN"
                score -= 1
                during_the_middle_of_a_round = False
                outcome = "New deal?"
                
        else:
            in_play = False
            player_msg = "BSTD"
            delaer_msg = "WIN"
            # if busted, assign a message to outcome, update in_play and score
            score -= 1
            during_the_middle_of_a_round = False
            outcome = "New deal?"
        
        
def stand():
    global in_play, outcome, dealer_msg, player_msg, score, during_the_middle_of_a_round
    
    in_play = False
    if during_the_middle_of_a_round:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            hit_card = new_deck.deal_card()
    #        print "HIT CARD:"
    #        print hit_card
    #        print   
            dealer.add_card(hit_card)
    #    print "DEALER'S VALUE:"
    #    print dealer.get_value()
    #    print 
        if dealer.get_value() > 21:
            dealer_msg = "BSTD"
            player_msg = "WIN"
            score += 1
            during_the_middle_of_a_round = False
        else:
            if dealer.get_value() >= player.get_value():
                dealer_msg = "WIN"
                player_msg = "LOSE"
                score -= 1
                during_the_middle_of_a_round = False
            else:
                player_msg = "WIN"
                dealer_msg = "LOSE"
                score += 1
                during_the_middle_of_a_round = False
        outcome = "New deal?"
         
    # assign a message to outcome, update in_play and score

def darw_text_with_shadow(canvas, text, pos, pt, color):
    canvas.draw_text(text, (pos[0] - 3, pos[1]), pt, 'Black', 'monospace')
    canvas.draw_text(text, (pos[0] - 2, pos[1]), pt, 'Grey', 'monospace')
    canvas.draw_text(text, pos, pt, color, 'monospace')

def keydown(key):
    if key == simplegui.KEY_MAP['D']:
        deal()
    if key == simplegui.KEY_MAP['H']:
        hit()
    if key == simplegui.KEY_MAP['S']:
        stand()
        
        
# draw handler    
def draw(canvas):
    # draw title
    darw_text_with_shadow(canvas, 'Blackjack', (80, 90), 80, 'Black')
    
    # draw player names
    darw_text_with_shadow(canvas, 'Dealer', (MARGIN_X, MARGIN_Y - TEXT_PT), TEXT_PT, 'White')
    darw_text_with_shadow(canvas, 'You', (MARGIN_X, MARGIN_Y + INTERVAL_Y + CARD_SIZE[1] - TEXT_PT), TEXT_PT, 'White')
    
    # draw score
    score_text = "YOUR SCORE: " + str(score)
    score_text_x = 550 - frame.get_canvas_textwidth(score_text, SMALL_TEXT_PT, 'monospace')
    darw_text_with_shadow(canvas, score_text, (score_text_x, 120), SMALL_TEXT_PT, 'White')
    
    # draw outcome (instruction)
    outcome_msg_x = 550 - frame.get_canvas_textwidth(outcome, TEXT_PT, 'monospace')
    darw_text_with_shadow(canvas, outcome, (outcome_msg_x, MARGIN_Y + INTERVAL_Y + CARD_SIZE[1] - TEXT_PT), TEXT_PT, 'White')
    
    # draw cards
    for card in range(len(dealer.card_list)):
        pos = (MARGIN_X + card * (INTERVAL_X + CARD_SIZE[0]), MARGIN_Y)
        if in_play:
            if card == 0:
                canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            else:
                dealer.card_list[card].draw(canvas, pos)
        else:
            dealer.card_list[card].draw(canvas, pos)
    for card in range(len(player.card_list)):
        pos = (MARGIN_X + card * (INTERVAL_X + CARD_SIZE[0]), MARGIN_Y + INTERVAL_Y + CARD_SIZE[1])
        player.card_list[card].draw(canvas, pos)
    
    # draw win and lose
    dealer_msg_x = 550 - frame.get_canvas_textwidth(dealer_msg, BIG_TEXT_PT, 'monospace')
    player_msg_x = 550 - frame.get_canvas_textwidth(player_msg, BIG_TEXT_PT, 'monospace')
    darw_text_with_shadow(canvas, dealer_msg, (dealer_msg_x, MARGIN_Y + CARD_SIZE[1] - BIG_TEXT_OFFSET ), BIG_TEXT_PT, 'White')
    darw_text_with_shadow(canvas, player_msg, (player_msg_x, MARGIN_Y + INTERVAL_Y + 2 * CARD_SIZE[1] - BIG_TEXT_OFFSET), BIG_TEXT_PT, 'White')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal [D]", deal, 200)
frame.add_button("Hit [H]",  hit, 200)
frame.add_button("Stand [S]", stand, 200)
frame.set_keydown_handler(keydown)

frame.add_label('')
frame.add_label("Shortcuts:")
frame.add_label('')

frame.add_label("Letters in brackets on buttons.")
frame.add_label('')
frame.add_label('')
frame.add_label('')

frame.add_label('Help:')
frame.add_label('')

frame.add_label("1. BSTD = Busted")
frame.add_label('')
frame.add_label("2. Clicking 'Stand' button to check the hole when you go BSTD.")
frame.add_label('')
frame.add_label("3. Clicking 'Deal' button during the middle of a round makes you lose.")
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
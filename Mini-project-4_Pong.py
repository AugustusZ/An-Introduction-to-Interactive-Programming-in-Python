## http://www.codeskulptor.org/#user38_DIJmI6VRkw_17.py
## http://www.codeskulptor.org/#user38_upXUdmIHcI_0.py

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# init
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
ACC = 1.1
player_scores = [0,0]
direction = LEFT
PADDLE_ACC = 3

# style para
SCORE_TXT_PT = 60
TEXT_COLOR = 'White'
LINE_COLOR = 'White'
BG_COLOR = 'Green'
LINE_WIDTH = 2
CIRCLE_RADIUS = 40
HALF_PENALTY_AREA_WIDTH = 35
HALF_PENALTY_AREA_HEIGHT = 90
HALF_GOAL_AREA_WIDTH = 12
CIRCLE_LOC = 48
ball_vel = [2.0,3.0] # pixels per update (1/60 seconds)

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):# direction as arg
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    ball_vel[1] = -random.randrange(60, 180) / 60.0 
    # randomization of vertical velocity
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60.0
    else: # left
        ball_vel[0] = -random.randrange(120, 240) / 60.0

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    player_scores[0] = 0
    player_scores[1] = 0 # these are ints
    spawn_ball(direction)
    
        
def paddle_extent(paddle_pos):
    L = paddle_pos[0] - HALF_PAD_WIDTH
    R = paddle_pos[0] + HALF_PAD_WIDTH   
    U = paddle_pos[1] - HALF_PAD_HEIGHT
    D = paddle_pos[1] + HALF_PAD_HEIGHT
    return [[L, U], [L, D], [R, D], [R, U]]

        
def penalty_area_extent(pos):
    L = pos[0] - HALF_PENALTY_AREA_WIDTH
    R = pos[0] + HALF_PENALTY_AREA_WIDTH  
    U = pos[1] - HALF_PENALTY_AREA_HEIGHT
    D = pos[1] + HALF_PENALTY_AREA_HEIGHT
    return [[L, U], [L, D], [R, D], [R, U]]

        
def goal_area_extent(pos):
    L = pos[0] - HALF_GOAL_AREA_WIDTH
    R = pos[0] + HALF_GOAL_AREA_WIDTH  
    U = pos[1] - HALF_PAD_HEIGHT
    D = pos[1] + HALF_PAD_HEIGHT
    return [[L, U], [L, D], [R, D], [R, U]]


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], LINE_WIDTH, LINE_COLOR)
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], LINE_WIDTH, LINE_COLOR)
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], LINE_WIDTH, LINE_COLOR)
    
    # center circle
    canvas.draw_circle((WIDTH / 2, HEIGHT /2), CIRCLE_RADIUS, LINE_WIDTH, LINE_COLOR)   
    canvas.draw_circle([CIRCLE_LOC + PAD_WIDTH, HEIGHT / 2], CIRCLE_RADIUS, LINE_WIDTH, LINE_COLOR)
    canvas.draw_circle([WIDTH - CIRCLE_LOC - PAD_WIDTH, HEIGHT / 2], CIRCLE_RADIUS, LINE_WIDTH, LINE_COLOR)
        
    # penalty area
    L_penalty_area = [HALF_PENALTY_AREA_WIDTH + PAD_WIDTH, HEIGHT / 2]
    R_penalty_area = [WIDTH - HALF_PENALTY_AREA_WIDTH - PAD_WIDTH, HEIGHT / 2]
    canvas.draw_polygon(penalty_area_extent(L_penalty_area), LINE_WIDTH, LINE_COLOR,BG_COLOR)  
    canvas.draw_polygon(penalty_area_extent(R_penalty_area), LINE_WIDTH, LINE_COLOR,BG_COLOR)  
    
    # goal area    
    L_goal_area = [HALF_GOAL_AREA_WIDTH + PAD_WIDTH, HEIGHT / 2]
    R_goal_area = [WIDTH - HALF_GOAL_AREA_WIDTH - PAD_WIDTH, HEIGHT / 2]
    canvas.draw_polygon(goal_area_extent(L_goal_area), LINE_WIDTH, LINE_COLOR, BG_COLOR)   
    canvas.draw_polygon(goal_area_extent(R_goal_area), LINE_WIDTH, LINE_COLOR, BG_COLOR)    
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ball collides with and bounces off of the top and bottom walls
    if (ball_pos[1] - BALL_RADIUS <= 0) or (ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
        print ball_vel
        
    # interaction w/ gutter and paddle
    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH):# left gutter
        if paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT - 1:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= ACC
            ball_vel[0] *= ACC
        else:
            spawn_ball(RIGHT)
            player_scores[0] += 1
    if (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH - 1):
        if paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT - 1:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= ACC
            ball_vel[0] *= ACC
        else:
            spawn_ball(LEFT) 
            player_scores[1] += 1          
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    if HALF_PAD_HEIGHT <= paddle1_pos[1] + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT - 1 :
        paddle1_pos[1] += paddle1_vel
    if HALF_PAD_HEIGHT <= paddle2_pos[1] + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT - 1 :
        paddle2_pos[1] += paddle2_vel

    
    # draw paddles
    canvas.draw_polygon(paddle_extent(paddle1_pos), LINE_WIDTH, LINE_COLOR, 'Orange')
    canvas.draw_polygon(paddle_extent(paddle2_pos), LINE_WIDTH, LINE_COLOR, 'Blue')
    
    # draw scores
    score1_hpos = WIDTH / 4 - 0.6 * SCORE_TXT_PT * len(str(player_scores[0])) / 2.0
    socre2_hpos = 3 * WIDTH / 4 - 0.6 * SCORE_TXT_PT * len(str(player_scores[1])) / 2.0
    
    canvas.draw_text(str(player_scores[1]), (score1_hpos + 2, HEIGHT / 4 + 2), SCORE_TXT_PT, 'Black', 'monospace')
    canvas.draw_text(str(player_scores[0]), (socre2_hpos + 2, HEIGHT / 4 + 2), SCORE_TXT_PT, 'Black', 'monospace')
    
    canvas.draw_text(str(player_scores[1]), (score1_hpos, HEIGHT / 4), SCORE_TXT_PT, TEXT_COLOR, 'monospace')
    canvas.draw_text(str(player_scores[0]), (socre2_hpos, HEIGHT / 4), SCORE_TXT_PT, TEXT_COLOR, 'monospace')

    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += PADDLE_ACC
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= PADDLE_ACC
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += PADDLE_ACC
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PADDLE_ACC
    if key == simplegui.KEY_MAP['r']:
        new_game()
          
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= PADDLE_ACC
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += PADDLE_ACC
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= PADDLE_ACC
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += PADDLE_ACC

def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Rstart (R)", restart)
frame.set_canvas_background(BG_COLOR)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)



# start frame
new_game()
frame.start()

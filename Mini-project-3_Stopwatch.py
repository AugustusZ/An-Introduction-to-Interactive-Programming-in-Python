## http://www.codeskulptor.org/#user38_JCllWstV5X_13.py

# template for "Stopwatch: The Game"
import simplegui

# define global variables
t = 0
stop_times = 0
successful_stop_times = 0
success_rate = '0.0%'
modename = 'Standard Mode'
hint = 'Just try to zero this ^'

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # X:xx.x
    minute = str(int(t / 600))
   
    # x:Xx.x
    num_of_tenths_of_sec = t % 600
    num_of_tens_of_sec = int(num_of_tenths_of_sec / 100)
    tens_of_sec = str(num_of_tens_of_sec)
    
    # x:xX.x
    num_of_sec = int(num_of_tenths_of_sec / 10) - num_of_tens_of_sec * 10
    sec = str(num_of_sec)
    
    # x:xx.X
    tenths_of_sec = str(num_of_tenths_of_sec % 10)
    
    # return X:XX.X 
    return minute + ':' + tens_of_sec + sec + '.' + tenths_of_sec
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    if modename == 'Standard Mode':
        timer.start()
    else:
        timer_in_hell.start()

    
def stop():
    global stop_times
    global successful_stop_times
    
    if timer.is_running():
        timer.stop()
        stop_times +=1
        if t % 10 == 0:
            successful_stop_times += 1
            
    if timer_in_hell.is_running():
        timer_in_hell.stop()
        stop_times +=1
        if t % 10 == 0:
            successful_stop_times += 1

 
def reset():
    global t
    global stop_times
    global successful_stop_times
    if modename == 'Standard Mode':
        timer.stop()
    else:
        timer_in_hell.stop()
    t = 0
    stop_times = 0
    successful_stop_times = 0    
    
    
# define mode parameter
def standardize():
    global interval
    global modename
    global hint
    reset()
    modename = 'Standard Mode'
    hint = 'Just try to zero this ^'    
    
def hellize():    
    global interval
    global modename
    global hint
    reset()
    modename = 'Hell Mode'
    hint = "More like a Random Mode :)"

    
# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t += 1

    
# define draw handler
def draw(canvas):
    # assume players always reset at least once in 10 min
    canvas.draw_text(format(t), [70, 115], 50, "Red", 'monospace') 
    score = str(successful_stop_times) + '/' + str(stop_times)
    canvas.draw_text(hint, [46, 130], 14, "green", 'monospace') 
    
    # no success no rate :) only times output
    if successful_stop_times == 0:
        # assume players always successfully stop at least once for the first 999 stops
        if stop_times >= 100:
            canvas.draw_text(score, [216, 20], 20, "Red", 'monospace')       
        elif stop_times >= 10:
            canvas.draw_text(score, [228, 20], 20, "Red", 'monospace')
        else:
            canvas.draw_text(score, [240, 20], 20, "Red", 'monospace')
    else:
        # success rate ouput formatting
        success_rate = str(int(100 * successful_stop_times / stop_times)) + '%'
        if success_rate == '100%' or success_rate == '10%':
            canvas.draw_text(score + '=' + success_rate, [180, 20], 20, "Red", 'monospace')
        else:
            canvas.draw_text(score + '=' + success_rate, [195, 20], 20, "Red", 'monospace')
     
    # mode
    canvas.draw_text(modename, [20, 190], 20, "Red", 'monospace') 
    
    
# create frame
frame = simplegui.create_frame("Home", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
timer_in_hell = simplegui.create_timer(1, tick)
frame.set_draw_handler(draw)
frame.add_button("Start!", start, 65)
frame.add_button("Stop!", stop, 65)
frame.add_button("Reset!", reset, 65)
frame.add_label('')
frame.add_label('Mode:')
frame.add_button("Standard", standardize, 65)
frame.add_button("Hell*", hellize, 65)
frame.add_label('* ARE YOU SERIOUS???')


# start frame
frame.start()


# Please remember to review the grading rubric
# checked √
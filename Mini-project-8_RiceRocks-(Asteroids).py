## http://www.codeskulptor.org/#user38_4tyyNdzdFH_38.py

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
level = 1
time = 0.5
CANNON_LEN = 43
TEXT_COL = 'White'
SHADOW_COL = "rgb(120,43,237)"
HIGHLIGHT_COL = "rgb(255,112,251)"
TEXT_PT = 30
TEXT_MARGIN_X = 20
TEXT_MARGIN_Y = 50
SHIP_COLLISION_TOLERANCE = 10
ROCK_SPAWN_TOLERANCE = 100
started = False
# globals for playing 
ON = True
OFF = False


class Const:
    def __init__(self, start_value, max_value):
        self.val = start_value
        self.change_val = 0.005 * max_value
        self.change_vel = 0
        self.max_val = max_value
        
    def incre(self, switch):
        if switch == OFF:
            self.change_vel = 0
        else:
            self.change_vel = self.change_val
        
    def decre(self, switch):
        if switch == OFF:
            self.change_vel = 0
        else:
            self.change_vel = -1 * self.change_val              
        
    def update(self):
        if self.val + self.change_vel < 0:
            self.val = 0.001 * self.max_val
        elif self.val + self.change_vel > self.max_val:
            self.val = self.max_val
        else:
            self.val += self.change_vel
           
    def __str__(self):        
        return str(self.val)
    
    
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_brown.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(0.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
#missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.image_center2 = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        self.sound = sound
        self.explose = False
        
    def draw(self,canvas):       
        if self.thrust:
            canvas.draw_image(self.image, self.image_center2, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def turn_clockwise(self): self.angle_vel = - ANG_CONST.val
    def turn_counterclockwise(self): self.angle_vel = ANG_CONST.val
    def stop_turning(self): self.angle_vel = 0
    
    def turn_on_thruster(self, switch): 
        self.thrust = switch
        if switch == ON:
            self.sound.play()
        else:
            self.sound.rewind()
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= 1 - FRC_CONST.val        
        self.vel[1] *= 1 - FRC_CONST.val
        
        self.angle += self.angle_vel
        
        self.forward = angle_to_vector(self.angle)
        
        if self.thrust == ON:
            self.vel[0] += ACC_CONST.val * self.forward[0]            
            self.vel[1] += ACC_CONST.val * self.forward[1]

        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
    def shoot(self):
        missile_pos = (self.pos[0] + CANNON_LEN * self.forward[0], self.pos[1] + CANNON_LEN * self.forward[1])
        missile_vel = [self.vel[0] + MSS_CONST.val * self.forward[0], self.vel[1] + MSS_CONST.val * self.forward[1]]
        missile_ang = self.angle
        a_missile = Sprite(missile_pos, missile_vel, missile_ang, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_radius(self):
        return self.radius - SHIP_COLLISION_TOLERANCE
    
    def get_position(self):
        return self.pos
    
    def set_explose(self, status):
        self.explose = status
        
    def get_explose(self):
        return self.explose
    
def keydown(key):
    global FRC_CONST, ACC_CONST
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_clockwise()
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn_counterclockwise()  
    if key == simplegui.KEY_MAP["up"]:
        my_ship.turn_on_thruster(ON)
    
    if key == simplegui.KEY_MAP["z"]:
        FRC_CONST.decre(ON)   
    if key == simplegui.KEY_MAP["x"]:
        FRC_CONST.incre(ON)        
    if key == simplegui.KEY_MAP["a"]:
        ACC_CONST.decre(ON)        
    if key == simplegui.KEY_MAP["s"]:
        ACC_CONST.incre(ON)
    if key == simplegui.KEY_MAP["q"]:
        MSS_CONST.decre(ON)        
    if key == simplegui.KEY_MAP["w"]:
        MSS_CONST.incre(ON)
    if key == simplegui.KEY_MAP["1"]:
        ANG_CONST.decre(ON)        
    if key == simplegui.KEY_MAP["2"]:
        ANG_CONST.incre(ON)
        
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        

def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.stop_turning()
    if key == simplegui.KEY_MAP["right"]:
        my_ship.stop_turning()
    if key == simplegui.KEY_MAP["up"]:
        my_ship.turn_on_thruster(OFF)
        
    if key == simplegui.KEY_MAP["z"]:
        FRC_CONST.decre(OFF)   
    if key == simplegui.KEY_MAP["x"]:
        FRC_CONST.incre(OFF)        
    if key == simplegui.KEY_MAP["a"]:
        ACC_CONST.decre(OFF)        
    if key == simplegui.KEY_MAP["s"]:
        ACC_CONST.incre(OFF)
    if key == simplegui.KEY_MAP["q"]:
        MSS_CONST.decre(OFF)        
    if key == simplegui.KEY_MAP["w"]:
        MSS_CONST.incre(OFF)
    if key == simplegui.KEY_MAP["1"]:
        ANG_CONST.decre(OFF)        
    if key == simplegui.KEY_MAP["2"]:
        ANG_CONST.incre(OFF)
  
        
def mouse_handler(position):
    global started,lives,score
    if started == False:
        started = True
        lives = 3
        score = 0
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            current_frame_index = self.age
            current_frame_center = [self.image_center[0] + current_frame_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_frame_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
           
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        self.forward = angle_to_vector(self.angle)

        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        self.age += 1
        
        if self.age < self.lifespan:
            return False
        else:
            return True
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def collide(self, other_object):
        d = dist(self.pos, other_object.get_position())
        if d < self.radius + other_object.get_radius():
            return True
        else:
            return False

def process_sprite_group(canvas, group):
    if len(group) > 0:
        for item in set(group):
            if item.update():
                group.remove(item)
                continue
            item.draw(canvas)
                        
def group_collide(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            group.remove(item)
            an_explosion = Sprite(item.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            return True
    return False

def group_group_collide(group1, group2):
    num_of_collisions_in_g1 = 0
    for item1 in set(group1):
        if group_collide(group2, item1):
            num_of_collisions_in_g1 += 1
            group1.discard(item1)
    return num_of_collisions_in_g1
        
    
    
def draw_text_with_shadow(canvas, text, pos, pt):
    canvas.draw_text(text, (pos[0] - 3, pos[1]), pt, SHADOW_COL, 'monospace')
    canvas.draw_text(text, (pos[0] - 2, pos[1]), pt, HIGHLIGHT_COL, 'monospace')
    canvas.draw_text(text, pos, pt, TEXT_COL, 'monospace')
    
def draw(canvas):
    global time, time_for_ship, lives, level, score, started, rock_group, missile_group, ship_explosing
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
          
    # lives, level and score 
    level = score // 10 + 1
    score_text_width = frame.get_canvas_textwidth('Score: ' + str(score), TEXT_PT, 'monospace')    
    level_text_width = frame.get_canvas_textwidth('Level ' + str(level), TEXT_PT, 'monospace')
    score_pos = [WIDTH - score_text_width - TEXT_MARGIN_X, TEXT_MARGIN_Y]
    level_pos = [WIDTH / 2 - level_text_width / 2, TEXT_MARGIN_Y]
    lives_pos = [TEXT_MARGIN_X, TEXT_MARGIN_Y]
    draw_text_with_shadow(canvas, 'Score: ' + str(score), score_pos, TEXT_PT)  
    draw_text_with_shadow(canvas, 'Level ' + str(level), level_pos, TEXT_PT)    
    draw_text_with_shadow(canvas, 'Lives: ' + str(lives), lives_pos, TEXT_PT)    
    
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    score += group_group_collide(missile_group, rock_group)
    
    # update ship and sprites
    my_ship.update()
    
    #update constants
    ACC_CONST.update()
    L_acc.set_text("ship acceleration: " + str(ACC_CONST))
    FRC_CONST.update()
    L_frc.set_text("ship-space friction: " + str(FRC_CONST))    
    MSS_CONST.update()
    L_mss.set_text("missile speed: " + str(MSS_CONST))    
    ANG_CONST.update()
    L_ang.set_text("ship rotation speed: " + str(ANG_CONST))  
    
    # lives
    if group_collide(rock_group, my_ship):
        lives -= 1
        my_ship.set_explose(True)
        time_for_ship = 0
    
    if my_ship.get_explose() == True:
        current_frame_index = time_for_ship // 1
        current_frame_center = [explosion_info.get_center()[0] + current_frame_index * explosion_info.get_size()[0], explosion_info.get_center()[1]]
        canvas.draw_image(ship_explosion_image, current_frame_center, explosion_info.get_size(), my_ship.pos, explosion_info.get_size(), my_ship.angle)
        #explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
        time_for_ship += 1
        if time_for_ship > 24:
            my_ship.set_explose(False)
    
    if lives == 0:
        started = False
        rock_group = set()

    # splash image    
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
    
    # BGM
    if started:
        soundtrack.play()
    else:
        soundtrack.rewind()
        
   
# timer handler that spawns a rock    
def rock_spawner():
    if started:
        if len(rock_group) <= 12: 
            rand_pos = [WIDTH * random.random(), HEIGHT * random.random()]
            
            while dist(rand_pos, my_ship.get_position()) < ROCK_SPAWN_TOLERANCE:
                rand_pos = [WIDTH * random.random(), HEIGHT * random.random()]
            #lvl = score // 10 + 1
            rand_vel = [(random.random() - 0.5) * level,  (random.random() - 0.5) * level]
            rand_ang = random.random() * 2 * math.pi
            rand_ang_vel = random.random() * 0.1 - 0.05
            a_rock = Sprite(rand_pos, rand_vel, rand_ang, rand_ang_vel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)
            
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, two sprites and constants
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
rock_group = set()
missile_group = set()
explosion_group = set()


FRC_CONST = Const(0.1,1)
ACC_CONST = Const(1,10)
MSS_CONST = Const(10,20)
ANG_CONST = Const(0.1,0.3)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# labels
frame.add_label("SETTINGS:")
frame.add_label("")
frame.add_label("Press [1] and [2] to adjust")
L_ang = frame.add_label("ship rotation speed: " + str(ANG_CONST))
frame.add_label("")
frame.add_label("Press [Q] and [W] to adjust")
L_mss = frame.add_label("missile speed: " + str(MSS_CONST))
frame.add_label("")
frame.add_label("Press [A] and [S] to adjust")
L_acc = frame.add_label("ship acceleration: " + str(ACC_CONST))
frame.add_label("")
frame.add_label("Press [Z] and [X] to adjust")
L_frc = frame.add_label("ship-space friction: " + str(FRC_CONST))

frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

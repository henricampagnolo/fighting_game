PIXEL = (320, 180)
PIXEL_SCALE = 6
RENDER_RES = (1920, 1080)
INITIAL_SCREENSIZE = (1280, 720)
FPS = 60

#Player
PLAYER_SIZE = (96, 144)

#JAVI
RUNNING_ANIM_START = 1 #min speed before animation
RUNNING_ANIM_SPEED = 30 #higher is slower
JUMPING_ANIM_SPEED = 4 #higher is slower
LANDING_ANIM_SPEED = 2 #higher is slower
VELOCITY_FOR_LANDING = 20 # falling faster than this causes a landing animation
LANDING_COMPENSATE = 1.7 # higher make the last frames of the landing last longer

NUMBER_OF_ATTACKS  = 4

KNOCK_BACK_SCALE = 100 # higher is weaker
LAUNCHED = 20 # min velocity to be launched
LAUNCHED_BOUNCINESS = 0.7
LAUNCHED_SPEED_LOSS_AIR = 0.985
LAUNCHED_SPEED_LOSS_GROUND = 0.98
INVICIBILITY_FRAMES = 40
LAUNCHED_ANIM_SPEED = 10

#Damage counter
DC_SCALE = 1
DC_BORDER = 30
DC_BAR_VAL = 60
DC_BARS = 5

#Movement 
N_JUMPS = 3
JUMP_COOLDOWN = 25
TURNSPEED = 0.5 #higher is faster (<1)
BOUNCINESS = 0 #higher is more (<1)
GRAVITY = 2 # higher is stronger
TERMINAL_VELOCITY = 30
JUMP_ACCELERATION = 25 #higher is stronger
JUMP_CONTROL = 1
ACCELERATION = 0.4 #higher is faster
DESACCELERATION = 0.90 #lower is stronger
MAXSPEED = 10 
MINSPEED = 0.1

#Camera
MIN_CAM_SIZE = (960, 540)
CAM_TOP_BORDER = 100
CAM_LEFT_BORDER = 100
CAM_RIGHT_BORDER = 100
CAM_BOTTOM_BORDER = 100

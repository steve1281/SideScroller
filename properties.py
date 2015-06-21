window_width  = 640
window_height = 480
frames_per_second = 60
level_file_list = ['data/level00.dat','data/level01.dat',
                   'data/level02.dat','data/level03.dat',
                   'data/level04.dat','data/level05.dat',
                   'data/level06.dat']
MAXLEVEL = len(level_file_list)

image_list = [ { 'filename': 'sprites/cat.gif',  'name': 'cat', 'x':60, 'y':50 },
               { 'filename': 'sprites/dead.gif', 'name': 'dead', 'x':30, 'y':50 },
               { 'filename': 'sprites/down.gif', 'name': 'down', 'x':30, 'y':50 },
               { 'filename': 'sprites/exit.gif', 'name': 'exit', 'x':30, 'y':50 },
               { 'filename': 'sprites/key.gif', 'name': 'key', 'x':30, 'y':50 },
               { 'filename': 'sprites/run_left.gif', 'name': 'left', 'x':30, 'y':50 },
               { 'filename': 'sprites/run_right.gif', 'name': 'right', 'x':30, 'y':50 },
               { 'filename': 'sprites/standing.gif', 'name': 'standing', 'x':30, 'y':50 },
               { 'filename': 'sprites/up.gif', 'name': 'up', 'x':30, 'y':50 },
             ]
help_image = 'help.BMP'
game_over_image = 'gameover.gif'
sound_list = [
              { 'filename': 'sounds/blop.wav', 'name': 'blop'},
              { 'filename': 'sounds/cat_meow_2.wav', 'name': 'meow'},
              { 'filename': 'sounds/coin_drop.wav', 'name': 'coin'},
              { 'filename': 'sounds/glass_ping.wav', 'name': 'glass_ding'},
              { 'filename': 'sounds/ping_drop.wav', 'name': 'ping_drop'},
              { 'filename': 'sounds/woosh.wav', 'name': 'woosh'},
             ]



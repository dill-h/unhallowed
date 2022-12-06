from player import *

# initialize pygame
pygame.init()

# start the clock and set fps to 60
clock = pygame.time.Clock()
fps = 60

# set up window
pygame.display.set_caption('nhallowed')
icon = pygame.image.load('ico.png')
pygame.display.set_icon(icon)

# sound
pygame.mixer.init()
#jump_sound = pygame.mixer.Sound('sound/jump.ogg')        
        
# game variables
main_menu = True
room_number = 0
        
# initialize player
player = Player(starting_pos[0][0], starting_pos[0][1])
# initialize background
background_image = pygame.image.load('tile/bg_cave.png')
background_image = pygame.transform.scale(background_image, (window_width, window_height)).convert() # resize image and convert to non-transparent to prevent lag

#initialize room
room = World(update_room(room_number))
 
 
# Game loop --------------------------------------------------+
run = True
while run:
    # runs game at given fps
    clock.tick(fps)
    
    # background image
    window.blit(background_image, (0, 0))
    
    room.draw()
    
    # Player -------------------------------------------------+
    
    player.update(room)
    '''
    if player.get_pos()[0] > window_width:
        room_number += 1
        room = World(current_room_data)
        player.set_pos(0,0)
    '''
    player.debug() # draw_hitboxes, draw_grid
    
    if player.ground_attacking:
        player.attack()
    if player.air_attacking:
        player.attack()
        
    if player.offscreen:
        room_number += 1
        player.offscreen = False
        room_data = []
        room = World(update_room(room_number))
        player.reset_pos(room_number)
        
    
    # Display ------------------------------------------------+
    pygame.display.update()
    
    # Check for exit -----------------------------------------+
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False
    if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_w]:
        run = False
    
# ------------------------------------------------------------+
pygame.quit()
from player import *
# from level import *

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
jump_sound = pygame.mixer.Sound('sound/jump.ogg')        
        
        
        
# initialize player
player = Player(100.0, window_height - 5 * tile_size)
# initialize background
background_image = pygame.image.load('tile/bg_cave.png')
background_image = pygame.transform.scale(background_image, (window_width, window_height)).convert() # resize image and convert to non-transparent to prevent lag
 
 
 
# Game loop --------------------------------------------------+
run = True
while run:
    # runs game at given fps
    clock.tick(fps)
    
    # background image
    window.blit(background_image, (0, 0))
    
    room.draw()
    
    # Player -------------------------------------------------+
    
    player.update()
    
    if player.get_pos()[0] > window_width:
        room_number += 1
        room = World(current_room_data)
        player.set_pos(0,0)
    
    player.debug() # draw_hitboxes, draw_grid
    
    if player.ground_attacking:
        player.attack()
    if player.air_attacking:
        player.attack()
    
    # Display ------------------------------------------------+
    pygame.display.update()
    
    # Check if game needs to be closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False
# ------------------------------------------------------------+
pygame.quit()
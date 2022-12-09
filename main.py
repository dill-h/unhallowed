from player import *

def main():
    # initialize pygame
    pygame.init()

    # start the clock and set fps to 60
    clock = pygame.time.Clock()
    fps = 60

    # set up window
    pygame.display.set_caption('nhallowed')
    icon = pygame.image.load('ico.png')
    pygame.display.set_icon(icon)

    # Sound ------------------------------------------------------+
    music_volume = 0.0 #0.5
    pygame.mixer.music.load('sound/title.ogg')
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()
            
    # game variables
    main_menu = not True #True
    info_menu = False #False
    room_number = 0 #0
    falls = 1
    hearts = 3
            
    # initialize player
    player = Player(0, window_height - (4*32+5), 0)
    # initialize background
    background_image = pygame.image.load('tile/bg_cave.png')
    background_image = pygame.transform.scale(background_image, (window_width, window_height)).convert() # resize image and convert to non-transparent to prevent lag
    main_menu_bg = pygame.image.load('titlescreen/bg_titlescreen.png')
    main_menu_bg = pygame.transform.scale(main_menu_bg, (window_width, window_height)).convert()
    info_menu_bg = pygame.image.load('titlescreen/bg_infoscreen.png')
    info_menu_bg = pygame.transform.scale(info_menu_bg, (window_width, window_height)).convert()

    def fade_out_menu(time):
        pygame.mixer.music.fadeout(time)
        pygame.time.wait(time)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    # initialize room
    room = World(update_room(room_number))
    
    #initialize enemies

    run = True
    while run:
        # runs game at given fps
        clock.tick(fps)
        pygame.event.pump()
        
    # Title screen -----------------------------------------------+
        if main_menu:
            #window.blit(main_menu_bg, (0, 0))
            # menu buttons
                
            if info_menu:
                window.blit(info_menu_bg, (0, 0))
                
                if back_button.draw():
                    pygame.time.wait(100)
                    info_menu = False
            else:
                window.blit(main_menu_bg, (0, 0))
                
                if play_button.draw():
                    fade_out_menu(1000)
                    pygame.mixer.music.load('sound/step_three.ogg')
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(fade_ms=500)
                    main_menu = False
                
                if info_button.draw():
                    pygame.time.wait(100)
                    info_menu = True
                    
                if quit_button.draw():
                    fade_out_menu(200)
                    pygame.quit()
                    break

    # Main game loop ---------------------------------------------+
        else:
            # Room -----------------------------------------------+
            window.blit(background_image, (0, 0))
            
            room.draw()
            
            # Player ---------------------------------------------+
            
            player.update(room)

            player.debug() # draw_hitboxes, draw_grid
            
            if player.ground_attacking:
                player.attack()
            if player.air_attacking:
                player.attack()
                
            if player.offscreen:
                room_number += 1
                player.offscreen = False
                room = World(update_room(room_number))
                player.reset_pos(room_number)
                
            if player.die(room_number, falls):
                print("Oops")
                falls += 1
                
        # Enemies ------------------------------------------------+
        
        enemy_group.update(player)
        enemy_group.draw(window)
            
        
        # Display ------------------------------------------------+
        pygame.display.update()
        
        # Check for exit -----------------------------------------+
            # I would put a more conventional exit method here
            # but if I use a loop to look for the pygame.QUIT event
            # double jumps stop working.
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
        if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_w]:
            run = False
        
    # ------------------------------------------------------------+
    pygame.quit()
    
if __name__ == '__main__':
    main()

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
    font = pygame.font.Font(path.join('font', 'perfectdos.ttf'), 24)

    # Sound ------------------------------------------------------+
    music_volume = 0.5 #0.5
    pygame.mixer.music.load('sound/title.ogg')
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()
            
    # game variables
    main_menu = True #True
    info_menu = False #False
    room_number = 0 #0
    falls = 1
            
    # initialize player
    player = Player(0, window_height - (4*32+5), 0)
    
    # initialize backgrounds
    bg_cave = pygame.image.load('tile/bg_cave.png')
    bg_cave = pygame.transform.scale(bg_cave, (window_width, window_height)).convert() # resize image and convert to non-transparent to prevent lag
    cave_levels = True
    bg_snow = pygame.image.load('tile/bg_snow.png')
    snow_levels = False
    bg_snow = pygame.transform.scale(bg_snow, (window_width, window_height)).convert()
    
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
                
        elif room_number >= 4 and snow_levels == False:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load('sound/ice.wav')
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(fade_ms=1500)
            snow_levels = True

    # Main game loop ---------------------------------------------+
        else:
            # Room -----------------------------------------------+
            if room_number < 4:
                window.blit(bg_cave, (0, 0))
            elif 4 <= room_number:
                window.blit(bg_snow, (0, 0))
                motd(font)
            
            room.draw()
            draw_text(f'HP:{"[]" * player.hp}', font, (237,237,237), 16, 16)
            # Player ---------------------------------------------+
            
            player.update(room, enemy_group)

            player.debug(enemy_group) # draw_hitboxes, draw_grid
            
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

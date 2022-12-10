import pygame
from pygame.locals import *
import random
import time
import pickle
from os import path

if __name__ == '__main__':
    print("\nDon't run me, I'm shy!")
    quit()


tile_size = 32
window_width = 32 * tile_size
window_height = 18 * tile_size

window = pygame.display.set_mode((window_width, window_height))

# SOUNDS
pygame.mixer.init()
sfx_volume = 0.5
slime_die = pygame.mixer.Sound('sound/slime_die.wav')
# CAVE TILESET
'''
8 1 2
7 0 3
6 5 4  
'''
room_number = 0


#load images
# CAVE - MAIN SURFACES
c_O = pygame.image.load('tile/c_O.png')
c_N = pygame.image.load('tile/c_N.png')
c_NE = pygame.image.load('tile/c_NE.png')
c_E = pygame.image.load('tile/c_E.png')
c_SE = pygame.image.load('tile/c_SE.png')
c_S = pygame.image.load('tile/c_S.png')
c_SW = pygame.image.load('tile/c_SW.png')
c_W = pygame.image.load('tile/c_W.png')
c_NW = pygame.image.load('tile/c_NW.png')

# CAVE - INNER CORNERS
c_NEic = pygame.image.load('tile/c_NEic.png')
c_SEic = pygame.image.load('tile/c_SEic.png')
c_SWic = pygame.image.load('tile/c_SWic.png')
c_NWic = pygame.image.load('tile/c_NWic.png')

# CAVE - FLOATING BLOCK
c_FBs = pygame.image.load('tile/c_FBs.png')
c_FBl = pygame.image.load('tile/c_FBl.png')
c_FBc = pygame.image.load('tile/c_FBc.png')
c_FBr = pygame.image.load('tile/c_FBr.png')

# CAVE - ENEMIES
c_slime = pygame.image.load('enemy/slime/idle/idle0.png')

# SNOW - MAIN SURFACES
s_O = pygame.image.load('tile/s_O.png')
s_N = pygame.image.load('tile/s_N.png')
s_NE = pygame.image.load('tile/s_NE.png')
s_E = pygame.image.load('tile/s_E.png')
s_SE = pygame.image.load('tile/s_SE.png')
s_S = pygame.image.load('tile/s_S.png')
s_SW = pygame.image.load('tile/s_SW.png')
s_W = pygame.image.load('tile/s_W.png')
s_NW = pygame.image.load('tile/s_NW.png')

# SNOW - INNER CORNERS
s_NEic = pygame.image.load('tile/s_NEic.png')
s_SEic = pygame.image.load('tile/s_SEic.png')
s_SWic = pygame.image.load('tile/s_SWic.png')
s_NWic = pygame.image.load('tile/s_NWic.png')

barrier = pygame.image.load('tile/barrier.png')



tileset =  {1: c_SW,
            2: c_S,
            3: c_SE,
            4: c_W,
            5: c_O,
            6: c_E,
            7: c_NW,
            8: c_N,
            9: c_NE,
            10: c_NEic,
            11: c_SEic,
            12: c_SWic,
            13: c_NWic,
            14: c_FBs,
            15: c_FBl,
            16: c_FBc,
            17: c_FBr,
            18: c_slime,
            19: s_SW,
            20: s_S,
            21: s_SE,
            22: s_W,
            23: s_O,
            24: s_E,
            25: s_NW,
            26: s_N,
            27: s_NE,
            28: s_NEic,
            29: s_SEic,
            30: s_SWic,
            31: s_NWic,
            32: barrier
            }
enemy_group = pygame.sprite.Group()

    
class World:
    def __init__(self, data):
        self.tile_list = []
        
        def tileify(image_file):
            image = pygame.transform.scale(image_file, (tile_size, tile_size))
            image_rect = image.get_rect()
            image_rect.x = col_count * tile_size
            image_rect.y = row_count * tile_size
            tile = (image, image_rect)
            self.tile_list.append(tile)
            
        def enemyify(image_file):
            foo = 'bar'
            
        row_count = 0    
        for row in data:
            col_count = 0
            for tile in row:
                if tile != 0 and tile != 18:
                    tileify(tileset[tile])
                    
                elif tile == 18:
                    slime = Slime(col_count * tile_size + 16, row_count * tile_size - 14)
                    enemy_group.add(slime)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])
            
            

class Slime(pygame.sprite.Sprite):
    def __init__(self, x0, y0, right = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy/slime/chassis.png')
        self.image = pygame.transform.scale(self.image, (64, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        # vars
        self.dead = False
        self.die_sound = True
        self.right = right
        self.move_counter = 0
        self.wait_counter = 0
        self.stopped = False
        self.direction = 'L'
        
        # animation vars
        self.idleframe = 0
        self.moveframe = 0
        self.dieframe = 0
        self.gamefeel_counter = 0
        
        
        # initialize animations
        
        # IDLE
        self.idle_frame_start = time.time()
        self.idle_anim_left = []
        self.idle_anim_right = []
        for f in range(0,4):
            frame_left = pygame.image.load(f'enemy/slime/idle/idle{f}.png')
            frame_left = pygame.transform.scale(frame_left, (64, 50))
            frame_right = pygame.transform.flip(frame_left, True, False)
            self.idle_anim_left.append(frame_left)
            self.idle_anim_right.append(frame_right)
        
        # MOVE
        self.move_frame_start = time.time()
        self.move_anim_left = []
        self.move_anim_right = []
        for f in range(0,4):
            frame_left = pygame.image.load(f'enemy/slime/move/move{f}.png')
            frame_left = pygame.transform.scale(frame_left, (64, 50))
            frame_right = pygame.transform.flip(frame_left, True, False)
            self.move_anim_left.append(frame_left)
            self.move_anim_right.append(frame_right)
            
        # DIE
        self.die_frame_start = time.time()
        self.die_anim_left = []
        self.die_anim_right = []
        for f in range(0,4):
            frame_left = pygame.image.load(f'enemy/slime/death/die{f}.png')
            frame_left = pygame.transform.scale(frame_left, (64, 50))
            frame_right = pygame.transform.flip(frame_left, True, False)
            self.die_anim_left.append(frame_left)
            self.die_anim_right.append(frame_right)
        
        
        
        
    def die(self):
        if self.die_sound:
            pygame.mixer.Sound.play(slime_die).set_volume(sfx_volume)
        self.die_sound = False
        self.dead = True
        
    def update(self, hero, tiles = 2):
        self.hitbox = Rect(self.rect.x + 4, self.rect.y + 20, 56, 28)
        
        if self.right and not self.stopped:
            self.rect.x += 1
            self.move_counter += 1
        elif not self.right and not self.stopped:
            self.rect.x -= 1
            self.move_counter += 1
        if abs(self.move_counter) > 32 * tiles:
            if self.right:
                self.direction = 'R'
            else:
                self.direction = 'L'
            self.stopped = True
            self.wait_counter += 1
            if self.wait_counter > random.randint(30,120):
                self.right = not self.right
                self.move_counter = 0
                self.wait_counter = 0
                self.stopped = False
            
        if hero.ground_attacking:
            if self.rect.colliderect(hero.hitbox_gattackL) and hero.direction == 'L' and 2 <= hero.gattackframe >= 3:
                self.die()
            if self.rect.colliderect(hero.hitbox_gattackR) and hero.direction == 'R' and 2 <= hero.gattackframe >= 3:
                self.die()
        if hero.air_attacking:
            if self.rect.colliderect(hero.hitbox_aattack) and 2 <= hero.aattackframe <= 3:
                self.die()
                
        # Animation handling ---------------------------------+
        if self.idleframe >= 4:
            self.idleframe = 0
            
        if self.moveframe >= 4:
            self.moveframe = 0
            
        if self.dieframe >= 4:
            for enemy in enemy_group:
                if enemy.dead:
                    enemy_group.remove(enemy)
            self.dieframe = -1
                    
        
        
        if self.dead:
            if self.right:
                window.blit(self.die_anim_right[self.dieframe], (self.rect.x, self.rect.y))
                if time.time() - self.die_frame_start > 0.1:
                    self.dieframe += 1        
                    self.die_frame_start = time.time()
            elif not self.right:
                window.blit(self.die_anim_left[self.dieframe], (self.rect.x, self.rect.y))
                if time.time() - self.die_frame_start > 0.1:
                    self.dieframe += 1        
                    self.die_frame_start = time.time()

        else:
            if self.stopped and self.direction == 'L':
                window.blit(self.idle_anim_left[self.idleframe], (self.rect.x, self.rect.y))
                if time.time() - self.idle_frame_start > 0.15:
                    self.idleframe += 1        
                    self.idle_frame_start = time.time()
                    
            elif self.stopped and self.direction == 'R':
                window.blit(self.idle_anim_right[self.idleframe], (self.rect.x, self.rect.y))
                if time.time() - self.idle_frame_start > 0.15:
                    self.idleframe += 1        
                    self.idle_frame_start = time.time()
            else:
                if self.right:
                    window.blit(self.move_anim_right[self.moveframe], (self.rect.x, self.rect.y))
                    if time.time() - self.move_frame_start > 0.15:
                        self.moveframe += 1        
                        self.move_frame_start = time.time()
                else:
                    window.blit(self.move_anim_left[self.moveframe], (self.rect.x, self.rect.y))
                    if time.time() - self.move_frame_start > 0.15:
                        self.moveframe += 1        
                        self.move_frame_start = time.time()

            
        
            


class Pickup:
    def __init__(self, pickup_type):
        foo = 'bar'
# -------------------------------------------------------------+
# Putting this here so I don't have to add yet another module to the import chain
class Button:
    def __init__(self, x, y, name):
        self.image_inactive = pygame.image.load(f'titlescreen/btn_{name}0.png')
        self.image_active = pygame.image.load(f'titlescreen/btn_{name}1.png')
        self.rect = self.image_inactive.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            window.blit(self.image_active, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            window.blit(self.image_inactive, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        return action

play_button = Button(window_width // 2 - 64, window_height // 2, 'play')
info_button = Button(window_width // 2 - 64, window_height // 2 + 64, 'info')
back_button = Button(window_width // 2 - 64, window_height // 2 + 64, 'back')
quit_button = Button(window_width // 2 - 64, window_height // 2 + 128, 'quit')

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    window.blit(img, (x, y))
# ------------------------------------------------------------------------------+
def update_room(rn, caption = False):
    enemy_group.empty()
    if path.exists(f'level/room{rn}_data'):
        with open(path.join('level', f'room{rn}_data'), 'rb') as pickle_in:
            room_data = pickle.load(pickle_in)
            
    if caption:
        pygame.display.set_caption(f'nhallowed [{rn}]')
    return room_data

def motd(fnt):
    draw_text('Thank you for playing Unhallowed!', fnt, (32,32,32), 92, 32)
    draw_text('More good stuff to come in the future.', fnt, (32,32,32), 92, 56)
    draw_text('In the meantime, please press either ESC or CTRL+W to exit.', fnt, (32,32,32), 92, 80)

import pygame, time
from pygame.locals import *
from world import *

if __name__ == '__main__':
    print("\nDon't run me, I'm shy!")
    quit()

tile_size = 32
window_width = 32 * tile_size
window_height = 18 * tile_size
room_number = 0
window = pygame.display.set_mode((window_width, window_height))

class Player:
    def __init__(self, x0, y0):
        self.image = pygame.image.load('player/idle/idle0.png')
        self.image = pygame.transform.scale(self.image, (100, 74))
        self.rect = self.image.get_rect()
        
        # ---- ANIMATIONS ----
        
        # IDLE
        self.idle_frame_start = time.time()
        self.idle_anim_right = []
        self.idle_anim_left = []
        for f in range(0,4):
            frame_right = pygame.image.load(f'player/idle/idle{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.idle_anim_right.append(frame_right)
            self.idle_anim_left.append(frame_left)
            
        # CROUCH
        self.crouch_anim_right = []
        self.crouch_anim_left = []
        for f in range(0,4):
            frame_right = pygame.image.load(f'player/crouch/crouch{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.crouch_anim_right.append(frame_right)
            self.crouch_anim_left.append(frame_left)
        
        # RUN
        self.run_frame_start = time.time()
        self.run_anim_right = []
        self.run_anim_left = []
        for f in range(0,6):
            frame_right = pygame.image.load(f'player/run/run{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.run_anim_right.append(frame_right)
            self.run_anim_left.append(frame_left)
            
        # GROUND ATTACK
        self.gattack_frame_start = time.time()
        self.gattack_anim_right = []
        self.gattack_anim_left = []
        for f in range(0,5):
            frame_right = pygame.image.load(f'player/attack/ground{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.gattack_anim_right.append(frame_right)
            self.gattack_anim_left.append(frame_left)
        
        # JUMP
        self.jump_frame_start = time.time()
        self.jump_anim_right = []
        self.jump_anim_left = []
        for f in range(2,9):
            frame_right = pygame.image.load(f'player/jump/jump{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.jump_anim_right.append(frame_right)
            self.jump_anim_left.append(frame_left)
            
        # DOUBLE JUMP EFFECT
        self.djeffect_frame_start = time.time()
        self.djeffect_anim_right = []
        self.djeffect_anim_left = []
        for f in range(0,5):
            frame_right = pygame.image.load(f'player/effect/effect{f}.png')
            #dframe_right = pygame.transform.scale(frame_right, (128, 128))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.djeffect_anim_right.append(frame_right)
            self.djeffect_anim_left.append(frame_left)
            
        # AIR ATTACK
        self.aattack_frame_start = time.time()
        self.aattack_anim_right = []
        self.aattack_anim_left = []
        for f in range(0,5):
            frame_right = pygame.image.load(f'player/attack/air{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.aattack_anim_right.append(frame_right)
            self.aattack_anim_left.append(frame_left)
            
        # FALL LOOP
        self.fall_frame_start = time.time()
        self.fall_anim_right = []
        self.fall_anim_left = []
        for f in range(0,2):
            frame_right = pygame.image.load(f'player/jump/fall{f}.png')
            frame_right = pygame.transform.scale(frame_right, (100, 74))
            frame_left = pygame.transform.flip(frame_right, True, False)
            self.fall_anim_right.append(frame_right)
            self.fall_anim_left.append(frame_left)
        
        # movement flags
        self.runframe = 0
        self.idleframe = 0
        self.jumpframe = 0
        self.djeffectframe = 0
        self.fallframe = 0
        self.airborne = True
        self.fallanim = False
        self.left = False
        self.right = False
        self.direction = 'R'
        self.jumping = False
        self.doublejumped = False
        
        # combat flags
        self.gattackframe = 0
        self.ground_attacking = False
        self.aattackframe = 0
        self.air_attacking = False
        
        # pos creds
        self.rect.x = x0
        self.rect.y = y0
        self.width = 50 * 2
        self.height = 37 * 2
        self.hitbox_width = self.width // 2
        self.hitbox_height = self.height - 10
        self.vel_x = 5
        #self.dx = 5
        #self.dy = 0
        self.vel_y = 0
        
    def get_pos(self):
        return [self.rect.x, self.rect.y]
    
    def set_pos(self, x0, y0):
        self.rect.x = x0
        self.rect.y = y0
        
    def update(self):
        # HITBOXES
        # COLLISION/HURTBOX
        self.hitbox = Rect(self.rect.x + 25, self.rect.y + 10, self.hitbox_width, self.hitbox_height)
        # GROUND ATTACKS
        self.hitbox_gattackL = Rect(self.hitbox.x - 30, self.hitbox.y, self.hitbox_width + 30, self.hitbox_height)
        self.hitbox_gattackR = Rect(self.hitbox.x, self.hitbox.y, self.hitbox_width + 30, self.hitbox_height)
        self.hitbox_aattack = Rect(self.hitbox.x - 30, self.hitbox.y, self.hitbox_width + 60, self.hitbox_height - 20)
        self.dx = 0
        self.dy = 0
        # input
        key = pygame.key.get_pressed()
        
        if key[pygame.K_o] and not self.jumping and not self.ground_attacking:
            self.vel_y = -15
            self.jumpframe = 0
            self.jumping = True
            self.airborne = True
        # if key[pygame.K_o] and self.jumping and self.fall and not self.doublejumped:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o and self.jumping and not self.doublejumped:
                    self.vel_x *= 1.5
                    self.vel_y = -15
                    self.jumpframe = 0
                    self.djeffectframe = 0
                    self.doublejumped = True
                    self.fallanim = False
            
            #pygame.mixer.Sound.play(jump_sound)
            
        '''
        if not key[pygame.K_o]:
            self.jumping = False
        ''' # if enabled this turns on infinite midair jumps
        
        if key[pygame.K_a] and not self.ground_attacking:
            self.dx -= self.vel_x
            self.left = True
            self.right = False
            self.direction = 'L'
        elif key[pygame.K_d] and not self.ground_attacking:
            self.dx += self.vel_x
            self.left = False
            self.right = True
            self.direction = 'R'
        else:
            self.left = False
            self.right = False
            self.runframe = 0
        
        if key[pygame.K_k]:
            self.attack()
        
        
        # GRAVITYYYYYY
        self.vel_y += 1.5
        if self.vel_y > 20:
            self.vel_y = 20
        self.dy += self.vel_y
        
        if self.vel_y > 0:
            self.fall = True
        
        #check for collision
        self.airborne = True
        #self.jumpframe = 7
        for tile in room.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.hitbox.x + self.dx, self.hitbox.y, self.hitbox_width, self.hitbox_height):
                self.dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.hitbox.x, self.hitbox.y + self.dy, self.hitbox_width, self.hitbox_height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    self.dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    self.jumpframe = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.hitbox.bottom
                    if self.vel_x != 5:
                        self.vel_x = 5
                    self.vel_y = 0
                    self.jumping = False
                    self.doublejumped = False
                    self.fallanim = False
                    self.fall = False
                    self.airborne = False
                    self.air_attacking = False
                    self.aattackframe = 0
                    self.jumpframe = 0
        
        #update player coordinates
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
            self.dy = 0
    
        # Animation Handling -------------------------------------------------------------------------------------------------+
        
        # GROUND ANIMATIONS
        if self.runframe >= 6:
            self.runframe = 0
            
        if self.idleframe >= 4:
            self.idleframe = 0
            
        if self.djeffectframe >= 5:
            self.djeffectframe = 4
            
        if self.left and not self.airborne and not self.ground_attacking:
            window.blit(self.run_anim_left[self.runframe], (self.rect.x, self.rect.y))
            if time.time() - self.run_frame_start > 0.1:
                self.runframe += 1        
                self.run_frame_start = time.time()
            
        elif self.right and not self.airborne and not self.ground_attacking:
            window.blit(self.run_anim_right[self.runframe], (self.rect.x, self.rect.y))
            if time.time() - self.run_frame_start > 0.1:
                self.runframe += 1        
                self.run_frame_start = time.time()
                
        elif not self.ground_attacking and not self.airborne:
            if self.direction == 'L':
                if not key[pygame.K_s]:
                    window.blit(self.idle_anim_left[self.idleframe], (self.rect.x, self.rect.y))
                else:
                    window.blit(self.crouch_anim_left[self.idleframe], (self.rect.x, self.rect.y))
                if time.time() - self.idle_frame_start > 0.15:
                    self.idleframe += 1        
                    self.idle_frame_start = time.time()
            elif self.direction == 'R':
                if not key[pygame.K_s]:
                    window.blit(self.idle_anim_right[self.idleframe], (self.rect.x, self.rect.y))
                else:
                    window.blit(self.crouch_anim_right[self.idleframe], (self.rect.x, self.rect.y))
                if time.time() - self.idle_frame_start > 0.15:
                    self.idleframe += 1        
                    self.idle_frame_start = time.time()
                    
        # AIR ANIMATIONS
        if self.jumpframe >= 7:
            self.fallanim = True
            
            if self.fallframe >= 2:
                self.fallframe = 0
            if self.direction == 'L' and not self.air_attacking and self.fallanim:
                window.blit(self.fall_anim_left[self.fallframe], (self.rect.x, self.rect.y))
                if time.time() - self.fall_frame_start > 0.1:
                    self.fallframe += 1        
                    self.fall_frame_start = time.time()
            elif self.direction == 'R' and not self.air_attacking and self.fallanim:
                window.blit(self.fall_anim_right[self.fallframe], (self.rect.x, self.rect.y))
                if time.time() - self.fall_frame_start > 0.1:
                    self.fallframe += 1        
                    self.fall_frame_start = time.time()
            
        if self.airborne and not self.fallanim and not self.air_attacking:
            if self.direction == 'L':
                window.blit(self.jump_anim_left[self.jumpframe], (self.rect.x, self.rect.y))
                if time.time() - self.jump_frame_start > 0.05:
                    self.jumpframe += 1        
                    self.jump_frame_start = time.time()
            else:
                window.blit(self.jump_anim_right[self.jumpframe], (self.rect.x, self.rect.y))
                if time.time() - self.jump_frame_start > 0.05:
                    self.jumpframe += 1        
                    self.jump_frame_start = time.time()
        
        if self.doublejumped:
            if self.left:
                window.blit(self.djeffect_anim_left[self.djeffectframe], (self.hitbox.right - 32, self.hitbox.bottom - 32))
            elif self.right:
                window.blit(self.djeffect_anim_right[self.djeffectframe], (self.hitbox.left - 32, self.hitbox.bottom - 32))
                
            if time.time() - self.djeffect_frame_start > 0.05:
                self.djeffectframe += 1
                self.djeffect_frame_start = time.time()
            
                    
    def attack(self):
        if not self.airborne:
            self.ground_attacking = True
            if self.direction == 'L':
                window.blit(self.gattack_anim_left[self.gattackframe], (self.rect.x, self.rect.y))
                if time.time() - self.gattack_frame_start > 0.075:
                    self.gattackframe += 1        
                    self.gattack_frame_start = time.time()
            elif self.direction == 'R':
                window.blit(self.gattack_anim_right[self.gattackframe], (self.rect.x, self.rect.y))
                if time.time() - self.gattack_frame_start > 0.075:
                    self.gattackframe += 1        
                    self.gattack_frame_start = time.time()
            if self.gattackframe >= 5:
                self.gattackframe = 0
                self.ground_attacking = False
        else:
            self.air_attacking = True
            if self.direction == 'L':
                window.blit(self.aattack_anim_left[self.aattackframe], (self.rect.x, self.rect.y))
                if time.time() - self.aattack_frame_start > 0.075:
                    self.aattackframe += 1        
                    self.aattack_frame_start = time.time()
            elif self.direction == 'R':
                window.blit(self.aattack_anim_right[self.aattackframe], (self.rect.x, self.rect.y))
                if time.time() - self.aattack_frame_start > 0.075:
                    self.aattackframe += 1        
                    self.aattack_frame_start = time.time()
            if self.aattackframe >= 5:
                self.aattackframe = 0
                self.air_attacking = False
        
    def debug(self, draw_hitboxes = False, draw_grid = False):
        self.draw_hitboxes = draw_hitboxes
        self.draw_grid = draw_grid
        
        if pygame.key.get_pressed()[pygame.K_BACKQUOTE]:
            self.draw_hitboxes = not self.draw_hitboxes
            self.draw_grid = not self.draw_grid
        
        if self.draw_hitboxes:
            pygame.draw.rect(window, (0,0,255), self.hitbox,2) # player hitbox display
            pygame.draw.rect(window, (255,0,0), self.hitbox_gattackR,1) # ground attacks
            pygame.draw.rect(window, (255,0,0), self.hitbox_gattackL, 1)
            pygame.draw.rect(window, (255,255,0), self.hitbox_aattack, 1) # air attack
        
        if self.draw_grid:
            for line in range(0, 32):
                pygame.draw.line(window, (255, 255, 255), (0, line * tile_size), (window_width, line * tile_size))
                pygame.draw.line(window, (255, 255, 255), (line * tile_size, 0), (line * tile_size, window_height))

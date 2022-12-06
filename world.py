import pygame
from levels import *

tile_size = 32
window_width = 32 * tile_size
window_height = 18 * tile_size

window = pygame.display.set_mode((window_width, window_height))

# CAVE TILESET
'''
8 1 2
7 0 3
6 5 4  
'''

room_index = [room0_data, room1_data]
room_number = 0

class World:
    def __init__(self, data):
        self.tile_list = []

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
        self.tileset = {1: c_SW,
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
                        17: c_FBr
                        }
        
        def tileify(image_file):
            image = pygame.transform.scale(image_file, (tile_size, tile_size))
            image_rect = image.get_rect()
            image_rect.x = col_count * tile_size
            image_rect.y = row_count * tile_size
            tile = (image, image_rect)
            self.tile_list.append(tile)
            
        row_count = 0    
        for row in data:
            col_count = 0
            for tile in row:
                if tile != 0:
                    tileify(self.tileset[tile])
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])

current_room_data = room_index[room_number]
room = World(current_room_data)
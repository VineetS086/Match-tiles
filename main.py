import pygame
from pygame import display, event, image, transform
import random
import os
import time
Difficulty = int(input('''
0 - Noob(2*2)
1 - Easy(4*4)
2 - Normal(6*6)
'''))

if not Difficulty:
    D_side = 2
    D_size = 160
elif Difficulty == 1:
    D_side = 4
    D_size = 128
elif Difficulty == 2:
    D_side = 6
    D_size = 100
    
# Declaring Sizes and NO

NUM_TILES_SIDE = D_side
NUM_TILES_TOTAL = NUM_TILES_SIDE*NUM_TILES_SIDE

IMAGE_SIZE = D_size
SCREEN_SIZE = IMAGE_SIZE*NUM_TILES_SIDE
MARGIN = 5
NUM_TILES_SIDE
    
# ADDIND ASSETS
Asset_Dir_IMAGE = 'photos'

Asset_Dir_IMAGE_ANIMAL = Asset_Dir_IMAGE+'/animals'
ASSET_ANIMALS = [x for x in os.listdir(Asset_Dir_IMAGE_ANIMAL)  ]

matched = image.load(Asset_Dir_IMAGE+'/others/matched.png')
matched = transform.scale( matched, (SCREEN_SIZE , SCREEN_SIZE))

start = image.load(Asset_Dir_IMAGE+'/others/start.png')
start = transform.scale( start, (SCREEN_SIZE , SCREEN_SIZE))

end = image.load(Asset_Dir_IMAGE+'/others/end.png')
end = transform.scale( end, (SCREEN_SIZE , SCREEN_SIZE)) 

#ASSET_ANIMALS SHORTLIST and rearrange

random.shuffle(ASSET_ANIMALS)
ASSET_MAIN = ASSET_ANIMALS[:int(NUM_TILES_TOTAL/2)]*2
random.shuffle(ASSET_MAIN)
ASSET_MAIN

#Class Animal ___THE MAIN OBJ
class Animal:
    def __init__(self,index):
        self.index = index
        self.row = index//NUM_TILES_SIDE
        self.col = index%NUM_TILES_SIDE
        self.name = ASSET_MAIN.pop()
        self.image_path = os.path.join(Asset_Dir_IMAGE_ANIMAL,self.name)
        self.image = transform.scale( image.load(self.image_path), (IMAGE_SIZE - 2 * MARGIN , IMAGE_SIZE - 2 * MARGIN))
        self.box = self.image.copy()
        self.box.fill((200,200,200))
        self.skip = False

def tile_no(x,y):
    row = y//IMAGE_SIZE
    col = x//IMAGE_SIZE
    index = (col + row*NUM_TILES_SIDE)
    return index

pygame.init()

display.set_caption('Match Tiles')
screen = display.set_mode((SCREEN_SIZE , SCREEN_SIZE))


running = True
tiles = [Animal(i) for i in range(0, NUM_TILES_TOTAL)]
current_images = []

screen.blit(start,(0,0))
display.flip()
time.sleep(3)

while running:
    current_events = event.get()
    for e in current_events:
        if e.type == pygame.QUIT:
            running = False
            
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
                
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            index = tile_no(mouse_x, mouse_y)
            if tiles[index] not in current_images:
                current_images.append(index)
            if len(current_images)>2:
                current_images = current_images[1:]
                    
    screen.fill((222,222,222))
    
    total_skipped = 0
    
    for i,tile in enumerate(tiles):
        dis_image = tile.image if i in current_images else tile.box
        
        if not tile.skip:
            screen.blit(dis_image,(tile.col*IMAGE_SIZE + MARGIN, tile.row*IMAGE_SIZE + MARGIN ))
        else:
            total_skipped +=1
            
    display.flip()
        
    if len(current_images)==2:
        if tiles[current_images[0]].name == tiles[current_images[1]].name:
            tiles[current_images[0]].skip = True
            tiles[current_images[1]].skip = True
            time.sleep(0.5)
            screen.blit(matched,(0,0))
            display.flip()
            time.sleep(0.3)
            current_images = []
    
    if total_skipped == len(tiles):
        running = False
        screen.blit(matched,(0,0))
        display.flip()
        screen.blit(end,(0,0))
        display.flip()
        time.sleep(1)
      

pygame.quit()

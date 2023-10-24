import pygame
import sys
import random
import time
from setting import *

# step1 : set screen, fps
# step2 : show dino, jump dino
# step3 : show tree, move tree

class Object(pygame.sprite.Sprite):
    def __init__(self, type, i, x, y):
        pygame.sprite.Sprite.__init__(self)
        if type==0: self.image = ball_images[i]
        elif type==1: self.image = obstacle_images[i]
        self.width = object_width[type][i]
        self.height = object_height[type][i]
        self.type = type

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        # set screen, fps
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
        pygame.display.set_caption('Jumping dino')
        self.fps = pygame.time.Clock()
        self.running = True

    def start(self):
        self.char_height = char_images[0].get_size()[1]
        self.char_bottom = MAX_HEIGHT - self.char_height
        self.char_x = 50
        self.char_y = self.char_bottom
        self.cur_idx = 0

        self.tree_width = tree_img.get_size()[0]
        self.tree_height = tree_img.get_size()[1]
        self.tree_x = MAX_WIDTH
        self.tree_y = MAX_HEIGHT - self.tree_height + 256

        self.objects = pygame.sprite.Group()
        obj = Object(1, 0, 1280 - object_width[1][0], MAX_HEIGHT - object_height[1][0])
        self.objects.add(obj)
        self.st = time.time()

        self.jump_top = 200
        self.is_bottom = True
        self.is_go_up = False
        self.stop = False

        self.run()
    def run(self):
        while True:
            self.fps.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # dino move
        if self.is_go_up:
            self.char_y -= 10.0
            self.stop = True
        elif not self.is_go_up and not self.is_bottom:
            self.char_y += 10.0
            self.stop = False

        # dino top and bottom check
        if self.is_go_up and self.char_y <= self.jump_top:
            self.is_go_up = False

        if not self.is_bottom and self.char_y >= self.char_bottom:
            self.is_bottom = True
            self.char_y = self.char_bottom

        # tree move
        self.tree_x -= 12
        if self.tree_x <= -self.tree_width: self.tree_x = MAX_WIDTH
        
        for obj in self.objects:
            obj.rect.x -= 12
            if obj.rect.x <= -obj.width: obj.kill()
        
        now = time.time()
        while len(self.objects) < 2 and now - self.st >= random.uniform(0.5, 2):
            if not random.randint(0,1): break
            i = random.randint(0,1)
            obj = Object(1, i, 1280 - object_width[1][i], MAX_HEIGHT - object_height[1][i])
            self.objects.add(obj)
            self.st = time.time()

        pygame.display.update()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.is_bottom:
                    self.is_go_up = True
                    self.is_bottom = False
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(tree_img, (self.tree_x, self.tree_y))
        self.objects.draw(self.screen)
        # draw dino
        if self.cur_idx==10: self.cur_idx=0
        self.screen.blit(char_images[self.cur_idx], (self.char_x, self.char_y))
        if not self.stop: self.cur_idx+=1 
    
        pygame.display.flip()
    
g = Game()
while g.running:
    g.start()
 

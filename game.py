import pygame
import sys
import random
import time
from setting import *
from os import path

class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [char_images[i] for i in range(10)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.h = char_images[0].get_size()[1]
        self.bottom = MAX_HEIGHT - self.h
        self.rect.x = 50
        self.rect.y = self.bottom

        self.vel = -20
        self.acc = 2
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

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

        self.mask = pygame.mask.from_surface(self.image)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
        pygame.display.set_caption('Jumping dino')
        self.fps = pygame.time.Clock()
        self.font = pygame.font.SysFont(None,32)
        self.running = True 
        self.load()

    def load(self):
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, HS_PATH), 'r') as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            self.highscore = 0

    def start(self):
        self.all_objects = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

        self.char = Character()
        self.all_objects.add(self.char)

        obj = Object(1, 0, 1280 - object_width[1][0], MAX_HEIGHT - object_height[1][0])
        self.objects.add(obj)

        self.tree_width = tree_img.get_size()[0]
        self.tree_height = tree_img.get_size()[1]
        self.tree_x = MAX_WIDTH
        self.tree_y = MAX_HEIGHT - self.tree_height + 256

        self.jump_top = 200
        self.vel = 12
        self.lv = 0
        self.score = 0

        self.is_bottom = True
        self.is_go_up = False
        self.stop = False

        self.st = time.time()
        self.timer = time.time()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.fps.tick(30)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_objects.update()
        
        hits = pygame.sprite.spritecollide(self.char, self.objects, False, 
                                           pygame.sprite.collide_mask)
        if hits:
            self.playing = False

        if not self.score % 10 and self.score / 10 != self.lv:
            self.lv = self.score / 10
            self.vel += ACC
            print(self.lv)
            print(self.vel)

        if not self.is_bottom:
            self.char.vel += self.char.acc
            self.char.rect.y += self.char.vel + 0.5*self.char.acc
        if self.is_go_up:
            self.stop = True
        elif not self.is_bottom:
            self.stop = False
        if self.is_go_up and self.char.rect.y <= self.jump_top:
            self.is_go_up = False
        if not self.is_bottom and self.char.rect.y >= self.char.bottom:
            self.is_bottom = True
            self.char.rect.y = self.char.bottom

        self.tree_x -= self.vel
        if self.tree_x <= -self.tree_width: self.tree_x = MAX_WIDTH
        
        for obj in self.objects:
            obj.rect.x -= self.vel
            if obj.rect.x <= -obj.width: obj.kill()
        
        now = time.time()
        self.score = int((now - self.timer)*10)

        while len(self.objects) < 2 and now - self.st >= random.uniform(0.8, 2) + self.lv/500:
            i = random.randint(0,1)
            if not random.randint(0,7): 
                obj = Object(0, i, 1280 - object_width[0][i], 
                             MAX_HEIGHT - object_height[0][i] - self.char.h)
                self.st -= 1
            else:
                obj = Object(1, i, 1280 - object_width[1][i], 
                             MAX_HEIGHT - object_height[1][i])
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
                    self.char.vel = -30
 
    def draw(self):
        background = pygame.image.load('images/background.png')
        self.screen.blit(background, (0,0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(tree_img, (self.tree_x, self.tree_y))
        self.objects.draw(self.screen)
        self.all_objects.draw(self.screen)
        self.screen.blit(self.font.render("HI "+str(self.highscore), True, (0, 0, 0)),
                         (MAX_WIDTH-240,30))
        self.screen.blit(self.font.render(str(self.score), True, (0, 0, 0)),
                         (MAX_WIDTH-120,30))
        pygame.display.flip()

    def game_start(self):
        self.screen.fill((255,255,255))
        self.draw_text("INCODE GAME", 128, (0,0,0), MAX_WIDTH/2, MAX_HEIGHT/4)
        self.draw_text("Space to jump!",
                       32, (0,0,0), MAX_WIDTH/2, MAX_HEIGHT/2)
        self.draw_text("Press Any Key to Continue...",
                       32, (0,0,0), MAX_WIDTH/2, MAX_HEIGHT*3/4)
        self.draw_text("High Score : " + str(self.highscore),
                       32, (0,0,0), MAX_WIDTH/2, 15)
        pygame.display.flip()
        self.wait()

    def game_over(self):
        self.draw_text("GAME OVER", 48, (0,0,0), MAX_WIDTH/2, MAX_HEIGHT/4)
        self.draw_text("Press Any Key to Continue...", 32, (0,0,0), MAX_WIDTH/2, MAX_HEIGHT*3/4)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 32, (0,0,0), MAX_WIDTH/2, 30)
            with open(path.join(self.dir, HS_PATH), 'w') as f:
                f.write(str(self.score))
        pygame.display.flip()
        self.wait()

    def wait(self):
        waiting = True
        while waiting:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
  
while g.running:
    g.game_start()
    g.start()
    g.game_over()

import pygame

MAX_WIDTH = 1280
MAX_HEIGHT = 720

char_images = [
    pygame.image.load('images/572px/1.png'),
    pygame.image.load('images/572px/2.png'),
    pygame.image.load('images/572px/3.png'),
    pygame.image.load('images/572px/4.png'),
    pygame.image.load('images/572px/5.png'),
    pygame.image.load('images/572px/6.png'),
    pygame.image.load('images/572px/7.png'),
    pygame.image.load('images/572px/8.png'),
    pygame.image.load('images/572px/9.png'),
    pygame.image.load('images/572px/10.png')
]
ball_images = [
    pygame.image.load('images/ball1.png'),
    pygame.image.load('images/ball2.png')
]
obstacle_images=[
    pygame.image.load('images/obstacle1.png'),
    pygame.image.load('images/obstacle2.png')
]
tree_img = pygame.image.load('images/trees.png')

object_width = [
    [ball_images[0].get_size()[0],
     ball_images[1].get_size()[0]],
    [obstacle_images[0].get_size()[0],
     obstacle_images[1].get_size()[0]]
]
object_height = [
    [ball_images[0].get_size()[1],
     ball_images[1].get_size()[1]],
    [obstacle_images[0].get_size()[1],
     obstacle_images[1].get_size()[1]]
]
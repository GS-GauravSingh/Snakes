import pygame
from pygame import Vector2, math
from pygame.locals import *
import pygame.display
import pygame.event
import pygame.draw
import pygame.time
import pygame.image
import pygame.transform
import pygame.font
import pygame.mixer
import random, sys

from pygame.math import Vector2
pygame.mixer.init()
pygame.init()

# Defining colors with RGB values
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (12, 87, 3)

# Creating Window
Screen_Width = 1280
Screen_Height = 720
Screen = pygame.display.set_mode([Screen_Width, Screen_Height])
pygame.display.set_caption("Snakes")

# Game Variables
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('footlight', 30)
Game_Images = {}

""" Loading Images  """

# Head
Game_Images["head_right"] = pygame.image.load("Graphics/head_right1.png").convert_alpha()
Game_Images["head_left"] = pygame.image.load("Graphics/head_left2.png").convert_alpha()
Game_Images["head_up"] = pygame.image.load("Graphics/head_up.png").convert_alpha()
Game_Images["head_down"] = pygame.image.load("Graphics/head_down.png").convert_alpha()

"""--------------------------------------------------------------------------------------------"""

# Background Image
bgimg = pygame.image.load("Graphics/background.png").convert_alpha()
bgimg = pygame.transform.scale2x(bgimg)

# Food
food_x = random.randint(0, 22)
food_y =  random.randint(0, 22)
food_position = (Vector2(food_x, food_y))
food_rect = pygame.Rect(food_position.x * 22, food_position.y * 22, 20, 20)
add_block = False

# Snake
snake_x = 22
snake_y = 22
snake_list = [Vector2(8, 10), Vector2(7, 10), Vector2(6, 10)]
snake_speed = Vector2(1, 0)

MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 200)


def eat_food():
    global food_position, snake_list, food_rect, food_x, food_y, add_block
    if food_position == snake_list[0]:
        food_x = random.randint(0, 50)
        food_y =  random.randint(0, 30)
        food_position = (Vector2(food_x, food_y))
        food_rect = pygame.Rect(food_position.x * 22, food_position.y * 22, 20, 20)
        add_block = True


while True:
    Screen.blit(bgimg, (0, 0))
    pygame.draw.rect(Screen, red, food_rect)
    eat_food()




    for index, block in enumerate(snake_list):
        if index == 0:
            Screen.blit(Game_Images["head_right"],(block.x * snake_x, block.y * snake_y))

        else:
            pygame.draw.rect(Screen, white, (block.x * snake_x, block.y * snake_y, 20, 20))


    head_direction = snake_list[1] -  snake_list[0]
    if head_direction == Vector2(1,0):
        Game_Images["head_right"] = Game_Images["head_left"]
    if head_direction == Vector2(-1,0):
        Game_Images["head_right"]
            




    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOVE_SNAKE:
            if add_block == True:
                snake_list_copy = snake_list[:]
                snake_list_copy.insert(0, snake_list_copy[0] + snake_speed)
                snake_list = snake_list_copy[:]
                add_block = False
            else:
                snake_list_copy = snake_list[:-1]
                snake_list_copy.insert(0, snake_list_copy[0] + snake_speed)
                snake_list = snake_list_copy[:]
            

        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                if snake_speed.x != 1:
                    snake_speed = Vector2(-1, 0)

            if event.key == K_RIGHT:
                if snake_speed.x != -1:
                    snake_speed = Vector2(1, 0)

            if event.key == K_UP:
                if snake_speed.y != 1:
                    snake_speed = Vector2(0, -1)

            if event.key == K_DOWN:
                if snake_speed.y != -1:
                    snake_speed = Vector2(0, 1)

    pygame.display.update()
    clock.tick(FPS)
        
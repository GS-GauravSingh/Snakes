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
Game_Images["head_right"] = pygame.image.load("Graphics/head_right.png").convert_alpha()
Game_Images["head_left"] = pygame.image.load("Graphics/head_left.png").convert_alpha()
Game_Images["head_up"] = pygame.image.load("Graphics/head_up.png").convert_alpha()
Game_Images["head_down"] = pygame.image.load("Graphics/head_down.png").convert_alpha()

# Tail
Game_Images["tail_right"] = pygame.image.load("Graphics/tail_right.png").convert_alpha()
Game_Images["tail_left"] = pygame.image.load("Graphics/tail_left.png").convert_alpha()
Game_Images["tail_up"] = pygame.image.load("Graphics/tail_up.png").convert_alpha()
Game_Images["tail_down"] = pygame.image.load("Graphics/tail_down.png").convert_alpha()

# Body
Game_Images["h_body"] = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
Game_Images["v_body"] = pygame.image.load("Graphics/body_vertical.png").convert_alpha()

# Body Curves
Game_Images["topleft"] = pygame.image.load("Graphics/body_tl.png").convert_alpha()
Game_Images["topright"] = pygame.image.load("Graphics/body_tr.png").convert_alpha()
Game_Images["bottomleft"] = pygame.image.load("Graphics/body_bl.png").convert_alpha()
Game_Images["bottomright"] = pygame.image.load("Graphics/body_br.png").convert_alpha()
"""--------------------------------------------------------------------------------------------"""

# Background Image
bgimg = pygame.image.load("Graphics/background.png").convert_alpha()
bgimg = pygame.transform.scale2x(bgimg)

# Food
food_x = random.randint(0, 26)
food_y =  random.randint(0, 16)
food_position = (Vector2(food_x, food_y))
food_rect = pygame.Rect(food_position.x * 40, food_position.y * 40, 40, 40)
add_block = False

# Snake
snake_x = 40
snake_y = 40
snake_list = [Vector2(8, 10), Vector2(7, 10), Vector2(6, 10)]
snake_speed = Vector2(1, 0)

MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 200)


def eat_food():
    global food_position, snake_list, food_rect, food_x, food_y, add_block

    food_img = pygame.image.load("Graphics/food.png").convert_alpha()
    Screen.blit(food_img, food_rect)
    
    if food_position == snake_list[0]:
        pygame.mixer.Sound("point.wav").play()
        food_x = random.randint(0, 26)
        food_y =  random.randint(0, 16)
        food_position = (Vector2(food_x, food_y))
        food_rect = pygame.Rect(food_position.x * 40, food_position.y * 40, 40, 40)
        add_block = True

def snake_graphics():
    global snake_list, snake_x, snake_y

    for index, block in enumerate(snake_list):
        if index == 0:
            head_direction = snake_list[0] -  snake_list[1]
            if head_direction == Vector2(-1,0):
                Screen.blit(Game_Images["head_left"],(block.x * snake_x, block.y * snake_y))

            if head_direction == Vector2(1,0):
                Screen.blit(Game_Images["head_right"],(block.x * snake_x, block.y * snake_y))

            if head_direction == Vector2(0,1):
                Screen.blit(Game_Images["head_down"],(block.x * snake_x, block.y * snake_y))

            if head_direction == Vector2(0,-1):
                Screen.blit(Game_Images["head_up"],(block.x * snake_x, block.y * snake_y))


        elif index == len(snake_list) - 1:
            tail_direction = snake_list[-1] -  snake_list[-2]
            if tail_direction == Vector2(-1,0):
                Screen.blit(Game_Images["tail_left"],(block.x * snake_x, block.y * snake_y))

            if tail_direction == Vector2(1,0):
                Screen.blit(Game_Images["tail_right"],(block.x * snake_x, block.y * snake_y))

            if tail_direction == Vector2(0,-1):
                Screen.blit(Game_Images["tail_up"],(block.x * snake_x, block.y * snake_y))

            if tail_direction == Vector2(0,1):
                Screen.blit(Game_Images["tail_down"],(block.x * snake_x, block.y * snake_y))


        else:
            previous_block = snake_list[index + 1] - block
            next_block = snake_list[index - 1] - block
            if previous_block.x == next_block.x:
                Screen.blit(Game_Images["v_body"],(block.x * snake_x, block.y * snake_y))
            elif previous_block.y == next_block.y:
                Screen.blit(Game_Images["h_body"],(block.x * snake_x, block.y * snake_y))
            else:
                if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                    Screen.blit(Game_Images["topleft"],(block.x * snake_x, block.y * snake_y))

                elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                    Screen.blit(Game_Images["bottomleft"],(block.x * snake_x, block.y * snake_y))

                elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                    Screen.blit(Game_Images["topright"],(block.x * snake_x, block.y * snake_y))

                elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                    Screen.blit(Game_Images["bottomright"],(block.x * snake_x, block.y * snake_y))

while True:
    Screen.blit(bgimg, (0, 0))
    eat_food()
    snake_graphics()


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
        
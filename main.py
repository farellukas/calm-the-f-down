from matplotlib.pyplot import plot
import pygame  # docs found here: https://www.pygame.org/docs/
from sys import exit

from brainflow.data_filter import (
    DataFilter,
    FilterTypes,
    AggOperations,
    WindowFunctions,
    DetrendOperations,
)
import numpy as np
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from Board import Board, get_board_id

from eeg_functions import *
from random import randint

# initialize the pygame
pygame.init()

# game parameters
WIDTH = 768
HEIGHT = 640

# create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# customize the pygame window
pygame.display.set_caption('calm the food down')
window_icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(window_icon)

# create Clock object
clock = pygame.time.Clock()

# customers
customer_surf = pygame.Surface((128, 128))
customer_rect = customer_surf.get_rect(topleft=(-128,0))

customers_rect_list = []

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# game functions
def customer_movement(customer_list):
    if customer_list:
        for customer_rect in customer_list:
            customer_rect.x += 5

            screen.blit(customer_surf, customer_rect)
        return customer_list
    else:
        return []

def collisions(customer_list):
    for i in range(len(customer_list)):
        if i == 0:
            if customer_list[i].right >= WIDTH: 
                customer_list[i].right = WIDTH
        else:
            if customer_list[i].right >= customer_list[i-1].left:
                customer_list[i].right = customer_list[i-1].left

# game loop
while True:
    screen.fill('white')  # background

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            pygame.quit()
            exit()
        if event.type == obstacle_timer:
            customers_rect_list.append(customer_surf.get_rect(topleft=(randint(-256, -128), 0)))
            pygame.time.set_timer(obstacle_timer, randint(3000, 10000))  # randomize customer timer
    
    # customer movement
    customer_rect_list = customer_movement(customers_rect_list)
    collisions(customers_rect_list)
        
    # updates display surface
    pygame.display.update()
    clock.tick(60)  # set fps ceiling to 60
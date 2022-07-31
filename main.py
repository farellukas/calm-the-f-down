from matplotlib.pyplot import plot
import pygame  # docs found here: https://www.pygame.org/docs/
from sys import exit
from random import randint, choice

# initialize the pygame
pygame.init()

# game parameters
WIDTH = 768
HEIGHT = 640
ORDERS = ['fries', 'fish']
completed = None

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
customers_order_list = []

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

def customer_collisions(customer_list):
    for i in range(len(customer_list)):
        if i == 0:
            if customer_list[i].right >= WIDTH: 
                customer_list[i].right = WIDTH
        else:
            if customer_list[i].right >= customer_list[i-1].left:
                customer_list[i].right = customer_list[i-1].left

def customer_complete(customer_list, order_list):
    customer_list.pop(0)
    order_list.pop(0)

# game loop
while True:
    # set background
    screen.fill('white') 

    # events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            pygame.quit()
            exit()
        if event.type == obstacle_timer:
            customers_rect_list.append(customer_surf.get_rect(topleft=(randint(-256, -128), 0)))
            customers_order_list.append(choice(ORDERS))
            pygame.time.set_timer(obstacle_timer, randint(3000, 7000))  # randomize customer timer
    
    # customer physics
    customer_rect_list = customer_movement(customers_rect_list)
    customer_collisions(customers_rect_list)
    if customers_order_list and completed == customers_order_list[0]:
        customer_complete(customers_rect_list, customers_order_list)
        
    # updates display surface
    pygame.display.update()
    clock.tick(60)  # set fps ceiling to 60
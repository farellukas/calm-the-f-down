import pygame  # docs found here: https://www.pygame.org/docs/
from sys import exit

# initialize the pygame
pygame.init()

# create the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# customize the pygame window
pygame.display.set_caption('calm the food down')
# window_icon = pygame.image.load('')
# pygame.display.set_icon(window_icon)

# create Clock object
clock = pygame.time.Clock()

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            pygame.quit()
            exit()

    # updates display surface
    pygame.display.update()
    clock.tick(60)  # set fps ceiling to 60
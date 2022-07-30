import pygame

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # args: tuple(width, height)

# customize the pygame window
pygame.display.set_caption('calm the food down')
# window_icon = pygame.image.load('')
# pygame.display.set_icon(window_icon)

# game loop
game_playing = True
while game_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            game_playing = False
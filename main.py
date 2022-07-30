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
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from Board import Board

# initialize the pygame
pygame.init()

# game parameters
WIDTH = 1600
HEIGHT = 900
BOARD_ID = 22  # muse 2 id

# create board object
board = Board(board_id=BOARD_ID)
sampling_rate = board.get_sampling_rate()
BUFFER_LENGTH = 1
NUM_POINTS = sampling_rate * BUFFER_LENGTH

# create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# customize the pygame window
pygame.display.set_caption('calm the food down')
window_icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(window_icon)

# create Clock object
clock = pygame.time.Clock()

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            pygame.quit()
            exit()

    # bci
    data = board.get_data_quantity(NUM_POINTS)
    exg_channels = board.get_exg_channels()
    print(data)
    eeg_data = data[exg_channels,:]

    # updates display surface
    pygame.display.update()
    clock.tick(60)  # set fps ceiling to 60
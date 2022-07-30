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

# initialize the pygame
pygame.init()

# game parameters
WIDTH = 1600
HEIGHT = 900
BOARD_ID = 22  # muse 2 id

# create board object
board = Board(board_id=BOARD_ID)
sampling_rate = board.get_sampling_rate(BOARD_ID)

buffer_length = 1
num_points = sampling_rate * buffer_length

# create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# customize the pygame window
pygame.display.set_caption('calm the food down')
window_icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(window_icon)

# create Clock object
clock = pygame.time.Clock()

# arrays
alpha_levels = []

def average(list):
    return sum(list)/len(list)

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # listen for QUIT event
            pygame.quit()
            exit()

    # bci
    data = board.get_data_quantity(num_points)
    alpha_session = []

    alpha_index = 2
    for i in range(1, 5):
        channel = data[i, :]
        fftData = np.fft.fft(channel)
        freq = np.fft.fftfreq(len(channel))*250

        # Remove unnecessary negative reflection
        fftData = fftData[1:int(len(fftData)/2)]
        freq = freq[1:int(len(freq)/2)]

        # Recall FFT is a complex function
        fftData = np.sqrt(fftData.real**2 + fftData.imag**2)

        # Band binding
        bandTotals = [0,0,0,0,0]
        bandCounts = [0,0,0,0,0]

        for point in range(len(freq)):
            if(freq[point] < 4):
                bandTotals[0] += fftData[point]
                bandCounts[0] += 1
            elif(freq[point] < 8):
                bandTotals[1] += fftData[point]
                bandCounts[1] += 1
            elif(freq[point] < 12):
                bandTotals[2] += fftData[point]
                bandCounts[2] += 1
            elif(freq[point] < 30):
                bandTotals[3] += fftData[point]
                bandCounts[3] += 1
            elif(freq[point] < 100):
                bandTotals[4] += fftData[point]
                bandCounts[4] += 1

        # Save the average of all points 
        bands = list(np.array(bandTotals)/np.array(bandCounts))
        alpha_bands = bands[alpha_index]

        alpha_session.append(alpha_bands)
    alpha_levels.append(average(alpha_session))

    # updates display surface
    pygame.display.update()
    clock.tick(60)  # set fps ceiling to 60
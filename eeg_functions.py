import matplotlib.pyplot as plt
import numpy as np

from Board import Board

from brainflow.data_filter import (
    DataFilter,
    FilterTypes,
    AggOperations,
    WindowFunctions,
    DetrendOperations,
)
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def process_data(data):
    channel = []
    for line in data:
        channel.append(line[0])
    print(channel)
    return channel

def plot_graph(channel): 
    time = np.arange(0, len(channel), 1)
    
    plt.plot(time, channel)
    plt.xlabel("Sample")
    plt.ylabel("μV")
    plt.show()
    plt.clf()

def plotBands(bands):
    binNames = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    plt.ylabel("Amplitude")
    plt.bar(binNames, bands, color="#7967e1")
    plt.show()
    plt.clf()

def average(list):
    return sum(list)/len(list)

BOARD_ID = 22  # muse 2 id
BOARD = Board(board_id=BOARD_ID)
SAMPLING_RATE = BOARD.get_sampling_rate(BOARD_ID)

BUFFER_LENGTH = 1
num_points = SAMPLING_RATE * BUFFER_LENGTH

ALPHA_LEVELS = []
THETABETA_RATIOS = []

def export_theta_beta_ratio(file):
    data = BOARD.get_data_quantity(num_points)
    alpha_session = []
    theta_session = []
    beta_session = []

    alpha_index = 2
    theta_index = 1
    beta_index = 3

    exg_channels = BOARD.get_exg_channels()

    for i in exg_channels:
        channel = data[i, :]
        fftData = np.fft.fft(channel)
        freq = np.fft.fftfreq(len(channel))*250

        # cut freq
        cutFreq = 60
        tolerance = 2

        # Use slicing to set a range of values to 0 amplitude
        fftData[   cutFreq - tolerance   :   cutFreq + tolerance   ] = 0

        # Remove unnecessary negative reflection
        fftData = fftData[1:int(len(fftData)/2)]
        freq = freq[1:int(len(freq)/2)]
        filteredData = abs(np.fft.ifft(fftData))

        # redo processing with filteredData
        fftData = np.fft.fft(filteredData)
        freq = np.fft.fftfreq(len(filteredData))*250

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
        theta_bands = bands[theta_index]
        beta_bands = bands[beta_index]

        alpha_session.append(alpha_bands)
        theta_session.append(theta_bands)
        beta_session.append(beta_bands)
    ALPHA_LEVELS.append(average(alpha_session))
    THETABETA_RATIOS.append(sum(theta_session)/sum(beta_session))
    export(file,sum(theta_session)/sum(beta_session))
    print(sum(theta_session)/sum(beta_session))

def export(file, data):
    file.write(str(data))
    file.write('\n')

if __name__ == '__main__':
    file = open('exported.txt', 'w')
    while True:
        export_theta_beta_ratio(file)
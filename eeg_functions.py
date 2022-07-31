import matplotlib.pyplot as plt
import numpy as np

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
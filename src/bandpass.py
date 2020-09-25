from scipy.signal import filtfilt
from scipy import stats
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy

def plot():
    data = pd.read_csv('./signal.csv')
    sensor_data = data[['# data']]

    sensor_data = np.array(sensor_data)

    time=np.linspace(0,0.5,79872)

    plt.plot(time,sensor_data)
    plt.show()

    filtered_signal = bandPassFilter(sensor_data)

    plt.plot(time, filtered_signal)
    plt.show()

def bandPassFilter(signal):
    fs = 79872.0
    lowcut = 600.0
    highcut= 2000.0

    nyq = 0.5*fs
    low = lowcut/nyq
    high = highcut/nyq

    order = 5

    b,a= scipy.signal.butter(order,[low,high], 'bandpass', analog=False)
    y = scipy.signal.filtfilt(b,a,signal,axis=0)

    return(y)

plot()

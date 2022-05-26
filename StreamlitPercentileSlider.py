import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

maxPercent = st.slider('Maximum Percentile', 0, 100)
minPercent = st.slider('Minimum Percentile', 0, 100)

cooling = pd.read_csv('smallCoolingData.csv')

histBins = np.arange(cooling['LoadHourlyAvg'].min(), cooling['LoadHourlyAvg'].nlargest(50).iloc[-1], 100)
fig, ax = plt.subplots(figsize=(12,6), facecolor='w')
cnts, values, bars = ax.hist(cooling['LoadHourlyAvg'], edgecolor='k', bins = histBins)

plt.xlabel('Cooling Load (Btu/h)', fontsize = 18)
plt.ylabel('Count of Hours', fontsize = 18)
plt.title('Histogram of San Leandro Patient Room Btu/h', fontsize = 24)

fig.show()

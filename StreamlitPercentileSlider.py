import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

minPercent = st.slider(label = 'Minimum Percentile', min_value = 0.0, max_value = 100.0, step = 0.1)
maxPercent = st.slider(label = 'Maximum Percentile', min_value = 0.0, max_value = 100.0, value =  95.0, step = 0.1)

cooling = pd.read_csv('smallCoolingData.csv')

histBins = np.arange(cooling['LoadHourlyAvg'].min(), cooling['LoadHourlyAvg'].nlargest(50).iloc[-1], 100)
fig, ax = plt.subplots(figsize=(12,6), facecolor='w')
cnts, values, bars = ax.hist(cooling['LoadHourlyAvg'], edgecolor='k', bins = histBins)

maxLoad = np.nan
while pd.isna(maxLoad):
    dfMax = cooling[cooling['Percentile'] == maxPercent / 100]
    maxLoad = dfMax['LoadHourlyAvg'].max()
    if pd.isna(maxLoad):
        maxPercent += 0.1
overHour = dfMax.max()['index']

minLoad = np.nan
while pd.isna(minLoad):
    dfMin = cooling[cooling['Percentile'] == minPercent / 100]
    minLoad = dfMin['LoadHourlyAvg'].min()
    if pd.isna(minLoad):
        minPercent += 0.1

for i, (cnt, value, bar) in enumerate(zip(cnts, values, bars)):
    if ((value <= minLoad) & (minPercent != 0)) | (value >= maxLoad) :
        bar.set_facecolor('#7997a1')
    else:
        bar.set_facecolor('#add8e6')

maxStr = (str(maxPercent) + 'th Percentile: ' + str(int(round(maxLoad))) + ' Btu/h')
hourStr = ('Cooling load greater in ' + str(int(overHour)) + ' hours out of ' + str(len(cooling)))

plt.xlabel('Cooling Load (Btu/h)', fontsize = 18)
plt.ylabel('Count of Hours', fontsize = 18)
plt.title('Histogram of San Leandro Patient Room Btu/h', fontsize = 24)
plt.annotate(maxStr, (0, 0), xytext=(0.45, 0.7), textcoords='axes fraction', fontsize = 14)
plt.annotate(hourStr, (0, 0), xytext=(0.45, 0.6), textcoords='axes fraction', fontsize = 14)

st.pyplot(fig)

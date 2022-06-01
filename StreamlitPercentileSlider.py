# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import Dataset (cleaned elsewhere beforehand)
cooling = pd.read_csv('smallCoolingData.csv')
cooling.drop(columns=['index', 'Unnamed: 0'], inplace = True)

# Create containers to organize widgets
container1 = st.container()
container2 = st.container()
col2_1, col2_2 = container2.columns(2)
container3 = st.container()
col3_1, col3_2 = container2.columns(2)
container4 = st.container()


# Set sliders
minPercent = container1.slider(label = 'Minimum Percentile', min_value = 0.0, max_value = 100.0, step = 0.1)
maxPercent = container1.slider(label = 'Maximum Percentile', min_value = 0.0, max_value = 100.0, value =  95.0, step = 0.1)

# Pick colors
inColor = col2_1.color_picker(label = 'Color Within Percentiles', value = '#add8e6')
outColor = col3_1.color_picker(label = 'Color Outside of Percentiles', value = '#7997a1')

# Pick Variable options (month, room name, etc)
monthDict = {
    'Select All':'Select All',
    'January':1,
    'February':2,
    'March':3,
    'April':4,
    'May':5,
    'June':6,
    'July':7,
    'August':8,
    'September':9,
    'October':10,
    'November':11,
    'December':12
}
monthList = list(monthDict.keys())
month = col2_2.selectbox(label = 'Month', options = monthList)
monthNum = monthDict[month]

zoneList = list(cooling['ZoneName'].unique())
zoneList.insert(0, 'Select All')
zoneName = col3_2.selectbox(label = 'Zone Name', options = zoneList)

# Change Dataset based on vars
if (zoneName != 'Select All') & (monthNum != 'Select All'):
    selectedData = cooling[cooling['ZoneName'] == zoneName]
    selectedData = selectedData[selectedData['SignalMonth'] == monthNum]
elif zoneName != 'Select All':
    selectedData = cooling[cooling['ZoneName'] == zoneName]
elif monthNum != 'Select All':
    selectedData = cooling[cooling['SignalMonth'] == monthNum]
else:
    selectedData = cooling

# Reset index and make it a column for ranking by percentile
selectedData.reset_index(drop = True, inplace = True)
selectedData.reset_index(inplace = True)
selectedData.rename(columns = {'level_0': 'index'}, inplace = True)

# Add percentile column
selectedData['Percentile'] = selectedData['index'].rank(ascending = False, method = 'dense', pct = True)
selectedData['Percentile']= round(selectedData['Percentile'], 3)

# Setup bins
if selectedData['LoadHourlyAvg'].max() > 2500:
    histBins = np.arange(selectedData['LoadHourlyAvg'].min(), selectedData['LoadHourlyAvg'].max(), 100)
elif selectedData['LoadHourlyAvg'].max() > 1000:
    histBins = np.arange(selectedData['LoadHourlyAvg'].min(), selectedData['LoadHourlyAvg'].max(), 50)
else:
    histBins = np.arange(selectedData['LoadHourlyAvg'].min(), selectedData['LoadHourlyAvg'].max(), 20)

# Setup Figure object
fig, ax = plt.subplots(figsize=(12,6), facecolor='w')
cnts, values, bars = ax.hist(selectedData['LoadHourlyAvg'], edgecolor='k', bins = histBins)

# Find cooling load value at given max percentile
# Loop ensures a value exists at specified percentile, moves onto next percentile if not
maxLoad = np.nan
while pd.isna(maxLoad):
    dfMax = selectedData[selectedData['Percentile'] == maxPercent / 100]
    maxLoad = dfMax['LoadHourlyAvg'].max()
    if pd.isna(maxLoad):
        maxPercent += 0.1
        maxPercent = round(maxPercent, 1)
# Note the number of hours greater than the max
overHour = dfMax.max()['index']

# Repeat above for min percentile
minLoad = np.nan
while pd.isna(minLoad):
    dfMin = selectedData[selectedData['Percentile'] == minPercent / 100]
    minLoad = dfMin['LoadHourlyAvg'].min()
    if pd.isna(minLoad):
        minPercent += 0.1
        minPercent = round(minPercent, 1)

# Color bars based on if in or outside of percentile ranges
for i, (cnt, value, bar) in enumerate(zip(cnts, values, bars)):
    if ((value <= minLoad) & (minPercent >= 0.5)) | (value >= maxLoad) :
        bar.set_facecolor(outColor)
    else:
        bar.set_facecolor(inColor)

# Create strings to annotate chart
maxStr = (str(maxPercent) + 'th Percentile: ' + str(int(round(maxLoad))) + ' Btu/h')
hourStr = ('Cooling load greater in ' + str(int(overHour)) + ' hours out of ' + str(len(selectedData)))

# Add lables/titles and annotations
plt.xlabel('Cooling Load (Btu/h)', fontsize = 18)
plt.ylabel('Count of Hours', fontsize = 18)
plt.title('Histogram of San Leandro Patient Room Btu/h', fontsize = 24)
plt.annotate(maxStr, (0, 0), xytext=(0.48, 0.9), textcoords='axes fraction', fontsize = 14)
plt.annotate(hourStr, (0, 0), xytext=(0.48, 0.8), textcoords='axes fraction', fontsize = 14)

# Display chart
container4.pyplot(fig)

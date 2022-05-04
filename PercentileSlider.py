import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

full = pd.read_csv('SL_All_Zones_Cooling_no_dups_11_30_21.csv', low_memory = False)
full = full[full['ZoneType'] == 'Patient Room']
full = full[['LoadHourlyAvg']]

cooling = pd.DataFrame()
between = full[full['LoadHourlyAvg'] < 0]
cooling['LoadHourlyAvg'] = abs(between['LoadHourlyAvg'])
cooling.reset_index(inplace = True, drop = True)

cooling.sort_values(by = 'LoadHourlyAvg', ascending = False, inplace = True)
cooling.reset_index(drop = True, inplace = True)
cooling.reset_index(inplace = True)
cooling.rename(columns = {'level_0': 'index'}, inplace = True)
cooling['Percentile'] = cooling['index'].rank(ascending = False, method = 'dense', pct = True)
cooling['Percentile']= round(cooling['Percentile'], 3)

df = cooling
maxPercent = 95
minPercent = 0

if len(df) == len(cooling):
    histBins = np.arange(df['LoadHourlyAvg'].min(), df['LoadHourlyAvg'].nlargest(50).iloc[-1], 100)
else:
    histBins = np.arange(df['LoadHourlyAvg'].nsmallest(50).iloc[-1], df['LoadHourlyAvg'].max(), 200)


dfMax = df[df['Percentile'] == maxPercent / 100]
maxLoad = dfMax['LoadHourlyAvg'].max()
overHour =dfMax.iloc[0]['index']

dfMin = df[df['Percentile'] == minPercent / 100]
minLoad = dfMin['LoadHourlyAvg'].min()

fig, ax = plt.subplots()
cnts, values, bars = ax.hist(df['LoadHourlyAvg'], edgecolor='k', bins = histBins)

for i, (cnt, value, bar) in enumerate(zip(cnts, values, bars)):
    if ((value <= minLoad) & (minPercent != 0)) | (value >= maxLoad) :
        bar.set_facecolor('#7997a1')
    else:
        bar.set_facecolor('#add8e6')

maxStr = (str(maxPercent) + 'th Percentile: ' + str(int(round(maxLoad))) + ' Btu/h')
hourStr = ('Cooling load greater in ' + str(int(overHour)) + ' hours out of ' + str(len(df)))

plt.xlabel('Cooling Load (Btu/h)', fontsize = 18)
plt.ylabel('Count of Hours', fontsize = 18)
plt.title('Histogram of San Leandro Patient Room Btu/h', fontsize = 24)

plt.annotate(maxStr, (0, 0), xytext=(0.45, 0.7), textcoords='axes fraction', fontsize = 14)
plt.annotate(hourStr, (0, 0), xytext=(0.45, 0.6), textcoords='axes fraction', fontsize = 14)

fig.show()

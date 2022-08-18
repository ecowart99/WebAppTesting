from datetime import date
import pandas as pd
import streamlit as st

#read in excel
uploaded_file = st.file_uploader("Please upload a properly formatted .csv file", type = ['csv'])

try:
    schedule = pd.read_csv(uploaded_file)
    st.write(schedule.head())
        
    #drop any unnamed columns
    schedule = schedule.loc[:,~schedule.columns.str.contains('^Unnamed')]

    #rename start and end time
    schedule= schedule.rename(index=str, columns={"StartTime":"StartTime", "EndTime":"EndTime"})

    #create variable time index for start and end times
    ST = pd.DatetimeIndex(schedule['Start Time'])
    ET = pd.DatetimeIndex(schedule['End Time'])

    #create Start Minute and End Minute variables
    schedule['SM']=ST.hour * 60 + ST.minute
    schedule['EM']=ET.hour*60 + ET.minute

    # start time at 0 
    time = 0

    # while time is less than 1440 (or 24 hours_)
    while time <= 1440:
    #empty list for time increment times
        SplitTime = []
        for i,x in schedule.iterrows(): 
    # if time is between start an end time place an 'y'
            if x['SM'] <= time and x['EM'] >= time:
                SplitTime.append('y')
            else:
    # if this is anything else, place a "n"
                SplitTime.append('n')
    # create new DF for schedule and then merge them together
        schedule[str(time)]=SplitTime

    # add 15 minutes to the time, to keep iterating through
        time += 30

    #Create file name
    today = date.today()
    filename = str(today) + '_' + uploaded_file.name + '_py'

    #Convert csv to string
    scheduleStr = schedule.to_csv()

    #export file
    st.download_button("Click here to download the updated .csv file", scheduleStr, file_name = filename)

except:
    st.write("No file uploaded yet")

import streamlit as st
import pandas as pd

maxPercent = st.slider('Maximum Percentile', 0, 100)
minPercent = st.slider('Minimum Percentile', 0, 100)
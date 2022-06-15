import matplotlib.font_manager as fm
import plotly.express as px
import streamlit as st

sgFont = fm.FontProperties(fname = 'kapra-neue-semibold-expanded.otf')

df = px.data.tips()

fig = px.density_heatmap(df, x = 'total_bill', y = 'tip', title = 'This is the special SMITHGROUP font')
fig.update_layout(font_family = 'Kapra Neue', font_size = 20)
st.plotly_chart(fig)
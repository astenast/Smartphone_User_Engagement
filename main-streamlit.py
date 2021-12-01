import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import calendar_d3, classification, patterns, details

import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title="Smartphone Addiction Tracker", page_icon=':chart_with_upwards_trend:', layout="wide")

html_temp ="""
    <div style="background-color:#778AAE;padding:1.5px">
    <font color=\"#FFFFFF\" size=\"32\"><strong><center>Smartphone Addiction Tracker</center></strong></font>
    </div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

PAGES = {
    "Introduction": calendar_d3,
    "Classification": classification,
    "Patterns Detection": patterns,
    "Info": details
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

if page == calendar_d3:
    page.app()
elif page == classification:
    page.app()
elif page == patterns:
    page.app()
elif page == details:
    page.app()


import pandas as pd
import streamlit as st
from streamlit_observable import observable
import plotly.graph_objects as go
from PIL import Image
import calendar_d3, classification, patterns, details

@st.cache(allow_output_mutation=True)
def get_data():
    df = pd.read_csv("data/sample_data.csv", index_col='Unnamed: 0')
    df = df[df['duration_min'] < 30]

    # create quantiles
    quantiles = df['duration_min'].quantile([.33, .66, .98, 1])

    # labeling of groups
    df['group'] = 'extreme'
    df['group'][df['duration_min'] <= quantiles[.98]] = 'high'
    df['group'][df['duration_min'] <= quantiles[.66]] = 'mid'
    df['group'][df['duration_min'] <= quantiles[.33]] = 'low' 

    return df


st.set_page_config(page_title="Smartphone Addiction Tracker", page_icon=':chart_with_upwards_trend:', layout="wide")

html_temp ="""
    <div style="background-color:#9EA2FF;padding:1.5px">
    <font color=\"#FFFFFF\" size=\"32\"><strong><center>Smartphone Addiction Tracker</center></strong></font>
    </div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

df = get_data()

PAGES = {
    "Calendar": calendar_d3,
    "Classification": classification,
    "Patterns Detection": patterns,
    "Technical Details": details
}

st.sidebar.title('User Selection')
option = st.sidebar.selectbox(
    'Pick a user id from the list:',
    ('389', 'user2', 'user3'))

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

if page == calendar_d3:
    page(df)
elif page == classification:
    page.app(df)
elif page == patterns:
    page.app(df)
elif page == details:
    page.app()

#with st.echo():
    #@st.cache
def get_calendar_data():
    return pd.read_csv("https://raw.githubusercontent.com/astenast/Smartphone_User_Engagement/main/data/calendar_user_389_final.csv?token=AMWUYUNDOQME4QGHBVX3MVTBUKLDI")

calendar_data = get_calendar_data()

#st.dataframe(calendar_data) shows the data lol

#with st.echo():

observable("General", 
    notebook="@astenast/digital_media_project",
    targets=["other"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
)

observable("Calendar", 
    notebook="@astenast/digital_media_project",
    targets=["chart"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
)
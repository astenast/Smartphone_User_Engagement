import streamlit as st
import pandas as pd
from streamlit_observable import observable

@st.cache(allow_output_mutation=True)
def get_calendar_data():
    return pd.read_csv("https://raw.githubusercontent.com/astenast/Smartphone_User_Engagement/main/data/calendar_user_389_final.csv?token=AMWUYUNDOQME4QGHBVX3MVTBUKLDI")


def app():
    st.header("Usage Overview")

    calendar_data = get_calendar_data()

    observable("General", 
        notebook="@astenast/digital_media_project",
        targets=["other"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
    )

    st.header("Calendar")

    left, right = st.columns(2)

    with left:
        option1 = st.selectbox(
        'Filter by Sessions or Duration:',
        ('Sessions', 'Duration'))
    with right:
        option2 = st.selectbox(
        'Pick type of visualization:',
        ('Relative Daily change', 'Change across all time'))


    observable("Calendar", 
        notebook="@astenast/digital_media_project",
        targets=["chart"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
    )
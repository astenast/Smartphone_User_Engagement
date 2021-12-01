import streamlit as st
import pandas as pd
from streamlit_observable import observable

@st.cache(allow_output_mutation=True)
def get_calendar_data():
    return pd.read_csv("https://raw.githubusercontent.com/astenast/Smartphone_User_Engagement/main/data/calendar_user_389_final_w_dailyduration.csv?token=AMWUYUOHKPTGOAEFAV75FF3BV6Y3G")


def app():
    st.header("Usage Overview")

    calendar_data = get_calendar_data()

    observable("General", 
        notebook="@astenast/digital_media_project",
        targets=["other"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
    )

    st.header("Calendar")


    observable("Calendar", 
        notebook="@astenast/digital_media_project",
        targets=["chart_w_daily2"], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"
        
    # observable("Calendar", 
    #     notebook="@astenast/digital_media_project",
    #     targets=[], #"chart", "key" "chart2", "chart3", "chart4", "chart5", "other"

    
    )
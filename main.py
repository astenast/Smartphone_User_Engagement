import pandas as pd
import streamlit as st
from streamlit_observable import observable
import plotly.graph_objects as go
from PIL import Image

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
    <font color=\"#000000\" size=\"32\"><strong><center>Smartphone Addiction Tracker</center></strong></font>
    </div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

df = get_data()

df_3633 = df[(df.user_id == 3633) & (df.year == 2017)].sort_values(['date', 'hour_period'])


fig = go.Figure(data=go.Scatter(x=df_3633['date'].astype(dtype=str)+df_3633['hour_period'].astype(dtype=str), 
                                y=df_3633['duration_min'],
                                marker_color='white'))

fig.update_layout({"title": '',
                   "xaxis": {"title":"Time"},
                   "yaxis": {"title":"Duration"},
                   "showlegend": False})

st.plotly_chart(fig, use_container_width = True)

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
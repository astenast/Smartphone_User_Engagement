import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

cats = [
    '00:00-00:30', '00:30-01:00', '01:00-01:30', '01:30-02:00', '02:00-02:30', '02:30-03:00', '03:00-03:30', 
    '03:30-04:00', '04:00-04:30', '04:30-05:00','05:00-05:30', '05:30-06:00', '06:00-06:30', '06:30-07:00', '07:00-07:30', 
    '07:30-08:00','08:00-08:30','08:30-09:00', '09:00-09:30', '09:30-10:00', '10:00-10:30', '10:30-11:00','11:00-11:30',
    '11:30-12:00', '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00','14:00-14:30',
    '14:30-15:00', '15:00-15:30', '15:30-16:00', '16:00-16:30', '16:30-17:00', '17:00-17:30', '17:30-18:00', '18:00-18:30', 
    '18:30-19:00', '19:00-19:30', '19:30-20:00','20:00-20:30', '20:30-21:00', '21:00-21:30', '21:30-22:00', '22:00-22:30', 
    '22:30-23:00','23:00-23:30', '23:30-24:00'
    ]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

colors = {'low': 'rgba(136,204,238,0.7)',
          'mid': 'rgba(102,194,165,0.7)',
          'high': 'rgba(252,141,98,0.7)',
          'extreme': 'rgba(228,26,28,0.7)'}

@st.cache(allow_output_mutation=True)
def get_data(user, option, day=None):

    if (option == 'Day of week') & (day is not None):
        df = pd.read_csv('data/data_session_group.csv').\
                drop(columns=['Unnamed: 0'])

        session_df = df[(df.user_id == int(user)) & (df.day == day)]

        df = pd.read_csv('data/data_duration_group.csv').\
                drop(columns=['Unnamed: 0'])

        duration_df = df[(df.user_id == int(user)) & (df.day == day)]

    elif (option == 'Day of week') & (day is None):
        df = pd.read_csv('data/data_session_group.csv').\
                drop(columns=['Unnamed: 0'])

        session_df = df[(df.user_id == int(user))]

        df = pd.read_csv('data/data_duration_group.csv').\
                drop(columns=['Unnamed: 0'])

        duration_df = df[(df.user_id == int(user))]

    else:
        df = pd.read_csv('data/data_session_group_monthly.csv').\
                drop(columns=['Unnamed: 0'])

        session_df = df[(df.user_id == int(user))]

        df = pd.read_csv('data/data_duration_group_monthly.csv').\
                drop(columns=['Unnamed: 0'])

        duration_df = df[(df.user_id == int(user))]    

    return session_df, duration_df

def app():  

    st.sidebar.title('User Selection')
    user = st.sidebar.selectbox(
        'Pick a user id from the list:',
        ('389', '6323', '2437'))

    st.header("User Classification")

    option = st.radio(
        'Select type of filtering:',
        ('Day of week', 'Month'))

    left, right = st.columns(2)

    with left:
        st.subheader("Based on number of sessions")
    
    with right:

        st.subheader("Based on duration of sessions")
    
    if option == 'Day of week':    

        session_df, duration_df = get_data(user, option)

        session_df = session_df.groupby(['day', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['day', 'Group count'], ascending=False)
        session_df['Type'] = 'Session'

        duration_df = duration_df.groupby(['day', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['day', 'Group count'], ascending=False)
        duration_df['Type'] = 'Duration'

        plot_df = session_df.append(duration_df)    
        
        fig = px.bar(plot_df, 
                        x='day', 
                        y="Group count", 
                        color="session_group", 
                        color_discrete_map=colors,
                        category_orders={'day': days},
                        labels={'session_group': 'Categories'},
                        facet_col='Type',
                        facet_col_spacing=0.1)

        # subplot titles
        for anno in fig['layout']['annotations']:
            anno['text']=''

        # hide subplot y-axis titles and x-axis titles
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''

        fig.update_layout(plot_bgcolor = "white")

        st.plotly_chart(fig, use_container_width=True)

        # Hourly plot

        day_option = st.selectbox(
                                'Select day of week:',
                                ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))

        session_df, duration_df = get_data(user, option, day=day_option)

        session_df = session_df.groupby(['hour_period', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['hour_period', 'Group count'], ascending=False)
        session_df['Type'] = 'Session'

        duration_df = duration_df.groupby(['hour_period', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['hour_period', 'Group count'], ascending=False)
        duration_df['Type'] = 'Duration'

        plot_df = session_df.append(duration_df)    
        
        fig = px.bar(plot_df, 
                        x='hour_period', 
                        y="Group count", 
                        color="session_group", 
                        color_discrete_map=colors,
                        category_orders={'hour_period': cats},
                        labels={'session_group': 'Categories'},
                        facet_col='Type',
                        facet_col_spacing=0.2)

        # subplot titles
        for anno in fig['layout']['annotations']:
            anno['text']=''

        # hide subplot y-axis titles and x-axis titles
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''

        fig.update_layout(plot_bgcolor = "white")

        st.plotly_chart(fig, use_container_width=True)
    
    else:
        session_df, duration_df = get_data(user, option)

        session_df = session_df.groupby(['month', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['month', 'Group count'], ascending=False)
        session_df['Type'] = 'Session'

        duration_df = duration_df.groupby(['month', 'session_group'])\
                        ['30min sessions'].\
                        count().\
                        reset_index(name='Group count').\
                        sort_values(by=['month', 'Group count'], ascending=False)
        duration_df['Type'] = 'Duration'

        plot_df = session_df.append(duration_df)    
        
        fig = px.bar(plot_df, 
                        x='month', 
                        y="Group count", 
                        color="session_group", 
                        color_discrete_map=colors,
                        category_orders={'month': days},
                        labels={'session_group': 'Categories'},
                        facet_col='Type',
                        facet_col_spacing=0.2)

        # subplot titles
        for anno in fig['layout']['annotations']:
            anno['text']=''

        # hide subplot y-axis titles and x-axis titles
        for axis in fig.layout:
            if type(fig.layout[axis]) == go.layout.XAxis:
                fig.layout[axis].title.text = ''

        fig.update_layout(plot_bgcolor = "white")

        st.plotly_chart(fig, use_container_width=True)

    

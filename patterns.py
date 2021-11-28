import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

cats = [
    '00:00-01:00', '01:00-02:00', '02:00-03:00', '03:00-04:00', '04:00-05:00','05:00-06:00', '06:00-07:00', '07:00-08:00',
    '08:00-09:00', '09:00-10:00', '10:00-11:00','11:00-12:00', '12:00-13:00', '13:00-14:00','14:00-15:00', '15:00-16:00', 
    '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00','20:00-21:00', '21:00-22:00', '22:00-23:00','23:00-24:00'
    ]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

@st.cache(allow_output_mutation=True)
def get_data(user):
    df = pd.read_csv('data/sample_data_hour.csv').\
            drop(columns=['Unnamed: 0'])
    high = pd.read_csv('data/high_group.csv').\
            drop(columns=['Unnamed: 0'])

    user = df[(df.user_id == int(user))].\
                sort_values(['date', 'hour_period']).\
                reset_index(drop=True)\
                [['day', 'hour_period','duration_min']]

    all_hours = pd.DataFrame(cats, columns=['hour_period'])

    all_hours_daily_df = \
            pd.merge(user[['day']].drop_duplicates(),
            all_hours[['hour_period']].drop_duplicates(),
            how = 'cross')

    user = \
        user.\
        merge(all_hours_daily_df,
        how='right').\
        fillna({'duration_min': 0}).\
        reset_index(drop = True)

    user = user.\
            groupby(['day', 'hour_period'])\
            ['duration_min'].\
            mean().\
            reset_index(name='Avg duration')
    user['day'] = pd.Categorical(user['day'], categories=days, ordered=True)
    user.sort_values(['day', 'hour_period'], inplace=True)

    return user, high

def app(user):    

    user_df, high_df = get_data(user)

    st.header("Patterns Detection")

    left, right = st.columns([1,3])

    with left:

        st.markdown('Explain plot and highlighted areas.')

    with right:

        fig = make_subplots(rows=7, cols=1, shared_xaxes=True, subplot_titles=days, vertical_spacing=0.05)
        xpoints = {}

        for i, day in enumerate(user_df.day.unique()):
            periods = []
            df_tmp = user_df[(user_df.day == day)]
            fig.add_trace(go.Scatter(x=df_tmp['hour_period'].astype(dtype=str), 
                                     y=df_tmp['Avg duration'], fill='tonexty',  name=day, fillcolor='rgba(145, 211, 199, 0.6)',
                                     mode='lines', line_color='rgb(145, 211, 199)'),
                    row=i+1, col=1)

            for period in df_tmp.hour_period.unique():

                extreme_dur = high_df[(high_df.day == days[i]) & (high_df.hour_period == period)]['Avg duration'].values[0]
                
                duration = df_tmp[df_tmp.hour_period ==  period]['Avg duration'].values[0]

                if (extreme_dur > 0) & (duration > 0):

                    if (duration >= extreme_dur):
                        periods.append(period)

            xpoints[i] = periods


        shapes_lst = []

        for i, vals in xpoints.items():
            if len(vals) > 0:
                for val in vals:
                    if i == 0:
                        shapes_lst.append(dict(type='rect', xref='x', yref='y',
                                x0=val, x1=val, y0=0, y1=8, line=dict(
                                            color="rgb(228,26,28)",
                                            width=20,
                                        ), opacity=0.4, line_width=1, layer='below'))    
                    else:
                        shapes_lst.append(dict(type='rect', xref=f'x{i+1}', yref=f'y{i+1}',
                                    x0=val, x1=val, y0=0, y1=8, line=dict(
                                            color="rgb(228,26,28)",
                                            width=10,
                                        ), opacity=0.4, line_width=20, layer='below'))

        fig.update_layout(
                shapes=shapes_lst, height=1500, showlegend=False)

        fig.for_each_yaxis(lambda x: x.update(showgrid=False))
        fig.update_yaxes(range=[0,8])
        st.plotly_chart(fig, use_container_width=True)
    
    st.header('Activity Overview')




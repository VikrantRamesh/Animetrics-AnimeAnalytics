import streamlit as st
import plotly.graph_objects as go
import numpy as np
import warnings
from streamlit_plotly_events import plotly_events
warnings.filterwarnings('ignore')
import pandas as pd

with open('css/master.css', 'r') as file:
        css = file.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


    
start_year,end_year = st.sidebar.slider("Year Range", 1970, 2025, (1970, 2025))

#Reading the Anime data
df = pd.read_csv('assets/processed_anime_data.csv')


df = df[(df['Start Year'] >= start_year) & (df['Start Year'] <= end_year)]

    
if 'xaxis' not in st.session_state:
    st.session_state.xaxis = "Members"

trans_df = df.copy()
trans_df['popularity'] = max(trans_df['popularity']) - trans_df['popularity'] +1 

main_container = st.container()
left,right = main_container.columns([3,1])
with main_container:
    with left:
        graph_size = 800
        slide_left, slide_mid, slide_right = st.columns([1,12,1]) 
        graph_size = slide_mid.slider("Adjust graph size", 500, 1000, 800, 25)

        fig = go.Figure()
        
        hover ='''
        <b>Name:</b> %{customdata[0]} <br>
        <b>Score:</b> %{x} <br>
        <b>Rank:</b> %{customdata[1]} <br>
        <b>Members:</b> %{customdata[2]} <br>
        <b>Episodes:</b> %{customdata[3]} <br>'''

        colors_dict = {'TV': '#FF5733', 'Movie': '#0099FF', 'OVA': ' #99FF33', 'Special': '#B533FF', 'ONA': '#FFA319'}  
        sym_dict = {'TV': 'cross', 'Movie': 'square', 'OVA': 'diamond', 'Special': 'circle', 'ONA': 'x'}  


        for typ in trans_df['Type'].unique():
            filt = trans_df[trans_df['Type'] == typ]
            custom_data = np.stack((filt['Title'], filt['Rank'], filt['Members'], filt['Episodes'],filt['Image']), axis=-1)
            
            fig.add_trace(go.Scatter(x = filt['Score'],
                                            y=filt[st.session_state.xaxis],
                                            customdata = custom_data, 
                                            mode='markers',
                                            name=typ,
                                            marker = dict(color=colors_dict[typ], symbol = sym_dict[typ])))
            fig.update_traces(hovertemplate=hover)

            
        
        fig.update_layout(
            title = {
                'text':f'Rating vs {st.session_state.xaxis}',
                'x':0.5
            },
            xaxis=dict(title='Rating',showgrid=False, linecolor='white', showline=True),
            yaxis=dict(title=st.session_state.xaxis,showgrid=False, linecolor='white', showline=True),
            showlegend = True,
            height=600,
            width=graph_size,
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',
            font=dict(color='white'),
            hovermode="closest"
        )



        #chart = st.plotly_chart(fig,use_container_width=True)
        fig.update_layout({"uirevision": "foo"}, overwrite=True)
        selected_points = plotly_events(fig, hover_event=True)
        
        result = []
        if selected_points:
            result = df[(trans_df['Score'] == selected_points[0]['x']) & (trans_df[st.session_state.xaxis] == selected_points[0]['y'])]
            
        

    with right:
        with st.sidebar:
            st.selectbox("Select Y-axis:", ["Members", "popularity"], key="xaxis")
            

        if len(result)>0:

            st.image(str(result['Image'].values[0]))
            
            st.markdown(f'''#### <center> {str(result['Title'].values[0])}\n</center>
            Rank: {str(result['Rank'].values[0])}<br>Score: {str(result['Score'].values[0])}<br>Popularity: #{str(result['popularity'].values[0])}<br>Episodes: {str(result['Episodes'].values[0])}<br>Score: {str(result['Score'].values[0])}<br>Genre: {str(result['Genre'].values[0])[1:-1]}<br>Start Date: {str(result['Start Date'].values[0])}<br>End Date: {str(result['End Date'].values[0])}           
            ''', unsafe_allow_html=True)

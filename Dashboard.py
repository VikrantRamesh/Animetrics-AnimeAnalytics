import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import warnings
from ast import literal_eval
from sklearn.preprocessing import MinMaxScaler
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Anime Analytics', page_icon=":peacock:",layout='wide')


with open('css/master.css', 'r') as file:
        css = file.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


selected = "Home"

if selected == 'Home':
    st.title("Animetrics")
    st.markdown("###### Find Your Next Anime Recommendation!")
st.markdown('<style>div.block-container{padding-top:3rem;padding-bottom:0rem;} </style>', unsafe_allow_html=True)
st.markdown('<style>h1#anime-analytics{padding-top:0rem;} </style>', unsafe_allow_html=True)

    
start_year,end_year = st.sidebar.slider("Year Range", 1970, 2025, (1970, 2025))

#Reading the Anime data
df = pd.read_csv('assets/processed_anime_data.csv')


df = df[(df['Start Year'] >= start_year) & (df['Start Year'] <= end_year)]


if selected == 'Home':
    left,middle = st.columns([2,3])
    ## Genres
    def string_to_list(s):
        if pd.isnull(s):
            return None
        return literal_eval(s)
    df['Genre'] = df['Genre'].apply(string_to_list)
    genre_dict = {}

    for genre_list in df['Genre']:
        if genre_list is not None and not isinstance(genre_list, float):
            
            for genre in genre_list:
                if genre in genre_dict.keys():
                    genre_dict[genre]+=1
                else:
                    genre_dict[genre] = 0

    ##### Histogram 1 #####
    genre_dict =  {k: v for k, v in sorted(genre_dict.items(), key=lambda item: item[1], reverse=True)}

    fig = go.Figure(go.Pie(labels = list(genre_dict.keys()), values=list(genre_dict.values()),  textinfo='none',hoverinfo='label+percent', hovertemplate="<b>Genre:</b> %{label} <br><b>Count:</b> %{value} <br><b>Precentage:</b> %{percent} <br>"))

    fig.update_layout(
        title = {
            'text':'Genre Distribution',
            'x':0.4
        },
        xaxis=dict(title='Genres'),
        yaxis=dict(title=''),
        legend=dict(orientation='v', y=0.5, yanchor='middle', x=-0.2, xanchor='left'),
        width=400,
        height=400
    )


    left.plotly_chart(fig,use_container_width=True)


    # ##### Histogram 2 #####

    year_data = []
    for typ in df['Type'].unique():
        year_data.append(go.Histogram(name=typ,x=df[df['Type'] == typ]['Start Year']))

    fig = go.Figure(data=year_data)

    # px.histogram(df, x='Type', category_orders={'Categories': df['Type'].unique()})

    fig.update_traces(hovertemplate="<b>Year:</b> %{x} <br><b>Count:</b> %{y} <br>")

    fig.update_layout(
        title={
                'text':'Histogram of Anime Type',
                'x': 0.4,
            },
        xaxis=dict(title='Types'),
        yaxis=dict(title='Count'),
        barmode='group',
    )

    middle.plotly_chart(fig,use_container_width=True)

    ### Trend Line

    fig = go.Figure()

    grouped_df = df.groupby('Start Year').agg({'Members': 'sum', 'Episodes': 'sum'}).reset_index()

    scaler = MinMaxScaler()
    grouped_df['Episodes'] = scaler.fit_transform(np.array(grouped_df['Episodes']).reshape(-1, 1))*10**7

    fig.add_trace(go.Scatter(x=grouped_df['Start Year'],
                            y=grouped_df['Episodes'],
                            name='Episodes Produced (Scaled)',
                            customdata=np.array(df.groupby('Start Year').agg({'Episodes': 'sum'})),
                            hovertemplate='Year: %{x}<br>Episodes: %{customdata[0]}<extra></extra>'))



    fig.add_trace(go.Scatter(x=grouped_df['Start Year'],
                            y=grouped_df['Members'],
                            name='Members',
                            hovertemplate='Year: %{x}<br>Members: %{y}<extra></extra>'))

    fig.update_layout(
        title={
            'text':'Trendline',
            'x':0.4
        },
        height=350,
    )

    st.plotly_chart(fig,use_container_width=True)


    ## Bubble Chart
    ind = df.index[df['Title'] == "Doraemon (1979)"].tolist()
    trans_df =  df.drop(ind)
    print(trans_df.shape)
    trans_df['popularity'] = max(trans_df['popularity']) - trans_df['popularity'] +1 
    ind = trans_df.index[trans_df['popularity'] <1000].tolist()
    trans_df =  trans_df.drop(ind)
    # print(trans_df.shape)

    hover ='''
    <b>Name:</b> %{customdata[0]} <br>
    <b>Score:</b> %{customdata[1]} <br>
    <b>Rank:</b> %{x} <br>
    <b>Members:</b> %{customdata[2]} <br>
    <b>Episodes:</b> %{customdata[3]} <br>
            '''

    fig = go.Figure()


    colors_dict = {'TV': ' #FF5733', 'Movie': '#0099FF', 'OVA': ' #99FF33', 'Special': '#B533FF', 'ONA': '#FFA319'}  


    for typ in trans_df['Type'].unique():

        filtered_data = trans_df[trans_df['Type'] == typ]
        custom = np.stack((filtered_data['Title'], filtered_data['Score'], filtered_data['Members'], filtered_data['Episodes']), axis=-1)
        
        # Add trace for each type
        fig.add_trace(
            go.Scatter(
                x=filtered_data['Rank'], 
                y=filtered_data['popularity'],  
                customdata=custom,
                mode="markers",
                name=typ,  
                marker=dict(color=colors_dict[typ],
                            size=filtered_data["Members"],
                            sizemode='area',
                            sizeref=2.0 * max(filtered_data["Members"]) / (20 ** 2), 
                            sizemin=4 )  
            )
        )
        fig.update_traces(
            
            hovertemplate=hover
        )


    fig.update_layout(
        title = "Rank vs Popularity vs Members",
        xaxis = dict(title='Rank',autorange='reversed'),
        yaxis = dict(title='Popularity'),
        showlegend=True,
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)




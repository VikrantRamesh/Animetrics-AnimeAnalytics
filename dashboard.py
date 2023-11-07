import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import warnings
from ast import literal_eval
from sklearn.preprocessing import MinMaxScaler
from streamlit_plotly_events import plotly_events
import smtplib
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Anime Analytics', page_icon=":peacock:",layout='wide')


title_alignment="""
<style>
#the-title {
  text-align: center
}
</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)

selected = "Home"



##Navigation Bar
selected = option_menu(
            menu_title=None,
            options=['Home','Master Plot', 'Contact'],
            icons=['house', 'bar-chart-line', 'envelope'],
            orientation='horizontal'
        )

if selected == 'Home':
    st.title("Anime Analytics")
    st.markdown("###### Find Your Next Anime Recommendation!")
st.markdown('<style>div.block-container{padding-top:3rem;padding-bottom:0rem;} </style>', unsafe_allow_html=True)
st.markdown('<style>h1#anime-analytics{padding-top:0rem;} </style>', unsafe_allow_html=True)

    


#Reading the Anime data
df = pd.read_csv('assets/processed_anime_data.csv')
left,middle = st.columns([2,3])

if selected == 'Home':
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
        width=450,
        height=450
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







##### PAGE 2

elif selected=='Master Plot':
    left,right = st.columns([3,1])
    
    if 'xaxis' not in st.session_state:
        st.session_state.xaxis = "Members"
    trans_df = df.copy()
    trans_df['popularity'] = max(trans_df['popularity']) - trans_df['popularity'] +1 

    with left:
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
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',
            font=dict(color='white'),
            hovermode="closest"
        )



        #chart = st.plotly_chart(fig,use_container_width=True)
        selected_points = plotly_events(fig, click_event=True,  hover_event=True)
        result = []
        if selected_points:
            result = df[(trans_df['Score'] == selected_points[0]['x']) & (trans_df[st.session_state.xaxis] == selected_points[0]['y'])]
            
        

    with right:
        st.selectbox("Select Y-axis:", ["Members", "popularity"], key="xaxis")
        #Boder
        st.markdown(
            """
            <style>
            .st-df:last-child {
                border-radius: 15px;
                border: 2px solid white;
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if len(result)>0:
            left_co, cent_co,last_co = st.columns(3)
            with cent_co:
                st.image(str(result['Image'].values[0]))
            
            st.markdown(f'''### <div style="padding-left:3rem;"><center> {str(result['Title'].values[0])}\n</center>
            Rank: {str(result['Rank'].values[0])}<br>Score: {str(result['Score'].values[0])}<br>Popularity: #{str(result['popularity'].values[0])}<br>Episodes: {str(result['Episodes'].values[0])}<br>Score: {str(result['Score'].values[0])}<br>Genre: {str(result['Genre'].values[0])[1:-1]}<br>Start Date: {str(result['Start Date'].values[0])}<br>End Date: {str(result['End Date'].values[0])}           
            </div>''', unsafe_allow_html=True)



## Page 3 

elif selected=='Contact':

    st.markdown("## <center>CONTACT ME</center>", unsafe_allow_html=True)


    left, right = st.columns([3,4])
    # Contact details

    with left:

        st.markdown(
            """
            <style>
            
            .st-emotion-cache-1v0mbdj.e115fcil1 img{
                border-radius: 50%;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                height:280px;
                width:280px!important;
            }
            </style>
            """
            , unsafe_allow_html=True
        )   
        # Image display in circular boundary
        col_left, cent, col_right = st.columns(3)
        cent.image("assets/images/Vikrant.jpg",  use_column_width=True)



    with right:
        st.markdown("##### <b> Name: </b>&emsp;&emsp;&nbsp; Vikrant Ramesh", unsafe_allow_html=True)
        st.markdown("##### <b> Mail: </b>&emsp;&emsp;&emsp; rvikrant2004@gmail.com", unsafe_allow_html=True)
        st.markdown("##### <b> Github: </b>&emsp;&emsp; https://github.com/VikrantRamesh", unsafe_allow_html=True)
        st.markdown("##### <b> Linkedin: </b>&emsp;&nbsp;&nbsp;https://www.linkedin.com/in/vikrant-ramesh-046061190/", unsafe_allow_html=True)
        st.markdown("##### <b> Github: </b>&emsp;&emsp; https://github.com/VikrantRamesh", unsafe_allow_html=True)
        
        with st.form(key = 'comment_form', clear_on_submit=True):
            comment=st.text_area('##### Reach out to Me!', )
            button = st.form_submit_button("Send")

        if button:
            st.success("Thank you for Reaching out!")
            with open("assets/comments.txt", 'a') as file:
                print(file.read())
                file.write(f"{comment}\n____________________________________________\n")

    

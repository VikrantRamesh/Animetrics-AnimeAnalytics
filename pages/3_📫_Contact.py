import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from streamlit_gsheets import GSheetsConnection
import requests
from datetime import datetime
import pandas as pd

# url = "https://docs.google.com/spreadsheets/d/1wGHqNlmQnwgM19QlVedBDg6ED-zrWu_qzXrCexp34h4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
#reading comments data
sql = '''
SELECT "Name", "Date", "Comment" FROM Comments WHERE "Name" IS NOT NULL;
'''
comment_data = conn.query(spreadsheet='https://docs.google.com/spreadsheets/d/1RswQ-cHUhqmYI0POJChEJhSb7OOV9g4dHy1NK-HYLeo/edit#gid=0',worksheet='Comments',sql =sql, ttl=5)


st.markdown("## <center>CONTACT ME</center>", unsafe_allow_html=True)

#importing CSS
with open('css/master.css', 'r') as file:
        css = file.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
with open('css/contact.css', 'r') as file:
        css = file.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


left, right = st.columns([2,4])

with left:
    col_left, cent = st.columns([1,8])
    cent.image("assets/images/Vikrant.jpg",  use_column_width=True)



with right:
    st.markdown("###### <b> Name: </b>&emsp;&emsp;&nbsp; Vikrant Ramesh", unsafe_allow_html=True)
    st.markdown("###### <b> Mail: </b>&emsp;&emsp;&emsp; rvikrant2004@gmail.com", unsafe_allow_html=True)
    st.markdown("###### <b> Github: </b>&emsp;&emsp; https://github.com/VikrantRamesh", unsafe_allow_html=True)
    st.markdown("###### <b> Linkedin: </b>&emsp;&nbsp;&nbsp;https://www.linkedin.com/in/vikrant-ramesh-046061190/", unsafe_allow_html=True)
    st.markdown("###### <b> Github: </b>&emsp;&emsp; https://github.com/VikrantRamesh", unsafe_allow_html=True)

    st.markdown('#####  Comment')
    # st.markdown('''
    #     <form action="https://formspree.io/f/mwkdzjpj" method="post">
    #         <input name="name" placeholder ='Name' class='form_input'/>
    #         <textarea name="comment" placeholder ='Comment'></textarea>
    #         <button type="submit" class="btn btn-lg btn-dark btn-block">Submit</button>
    #     </form>
    # ''', unsafe_allow_html=True)\
    with st.form("Comments", clear_on_submit=True):
        name = st.text_input("Name")
        comment = st.text_area("Comment")

        form_data = {
            "name": name,
            "comment": comment,
        }
        submit = st.form_submit_button("Comment")

    # Submit button
    if submit:
        
        response = requests.post("https://formspree.io/f/mwkdzjpj", data=form_data)
        
        if response.status_code == 200:
            st.success("Thanks for Commenting!...Proessing, Please wait")
        else:
            st.warning(f"Form submission failed with status code: {response.status_code}")   
        
        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d") 

        new_comment = pd.DataFrame([[name,current_date, comment]], columns=comment_data.columns)

        sql = '''
        SELECT "Name", "Date", "Comment" FROM Comments WHERE "Name" IS NOT NULL;
        '''
        
        comment_data = conn.query(sql=sql)
        comment_data = pd.concat([comment_data, new_comment], ignore_index=True, axis=0)
        conn.update(
            worksheet="Comments",
            data = comment_data
        )


container_style = (
    " border-radius: 10px; box-shadow: 2px 2px 5px #888; margin:10px auto;"
)

st.markdown("### Latest Comments")

for index,row in comment_data[::-1].head().iterrows():
    st.markdown(
        f"""
        <div style = "{container_style}">
            <div style='background-color:#E5E4E2;padding: 10px; border-radius:10px 10px 0 0;'>
                <div style="display:flex;color: black;">
                    <div style="flex: 1; margin-right: 20px;font-size: 20px;">
                        <strong style="font-weight: bold;">Name:&nbsp;&nbsp;&nbsp;</strong> {row['Name']}
                    </div>
                    <div style="flex: 1;text-align: right;font-size: 16px;font-weight: black;">
                        {row['Date']}
                    </div>
                </div>
            </div>
            <div style = "padding-right:10px;padding: 10px;">
                <p><em style="font-style: italic;"> {row['Comment']}</em></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

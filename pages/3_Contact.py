import streamlit as st
import warnings
warnings.filterwarnings('ignore')

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
    st.markdown("##### <b> Name: </b>&emsp;&emsp;&nbsp; Vikrant Ramesh", unsafe_allow_html=True)
    st.markdown("##### <b> Mail: </b>&emsp;&emsp;&emsp; rvikrant2004@gmail.com", unsafe_allow_html=True)
    st.markdown("##### <b> Github: </b>&emsp;&emsp; https://github.com/VikrantRamesh", unsafe_allow_html=True)
    st.markdown("##### <b> Linkedin: </b>&emsp;&nbsp;&nbsp;https://www.linkedin.com/in/vikrant-ramesh-046061190/", unsafe_allow_html=True)

    st.markdown('#####  Reach Out to Me!')
    st.markdown('''
        <form action="https://formspree.io/f/mwkdzjpj" method="post">
            <input name="name" placeholder ='Name' class='form_input'/>
            <textarea name="comment" placeholder ='Comment'></textarea>
            <button type="submit" class="btn btn-lg btn-dark btn-block">Submit</button>
        </form>
    ''', unsafe_allow_html=True)


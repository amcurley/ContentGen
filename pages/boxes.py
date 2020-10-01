import streamlit as st
import awesome_streamlit as ast
from streamlit import caching


def boxes():
    option = st.selectbox('Select one example topic below!',
    ('Choose a Topic', 'Argentina', 'Yellow', 'Red', 'Blue'))

    if option == 'Choose a Topic':
        st.text('')
    elif option == 'Argentina':
        f = open('./pages/argentina.txt', "r" ) # I will need a few .txt files
        message = f.read()
        st.text(message)
    else:
        st.text('You did not choose green')

    return option

# def select():
#     color = boxes()
#
#     if color != 'Green':
#         st.markdown("You choose green")
#     else:
#         st.markdown("You did not pick green")


def write():
    """Method used to bring page into the app.py file"""
    with st.spinner("Loading ..."):
        box = boxes()

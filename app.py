import streamlit as st
from PIL import Image
import os, random
import base64
import pages.home
import pages.gan
import awesome_streamlit as ast
def main():
    """Main Function of the App"""
    PAGES = {
        'Home': pages.home,
        'GAN': pages.gan
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Select Your Page", list(PAGES.keys()))
    page = PAGES[selection]
    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Aidan Curley. You can learn more about me on
        [LinkedIn](https://www.linkedin.com/in/aidancurley/).
        """
    )
if __name__ == "__main__":
    main()

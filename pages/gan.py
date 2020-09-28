import streamlit as st
from PIL import Image
import os, random
import base64
import awesome_streamlit as ast


def gen():
    folder = r'/Users/aidancurley/Documents/dsir/personal/MeetAbby/faces'

    a = random.choice(os.listdir(folder))

    file = folder + "/" + a #File to selected image

    image = Image.open(file)

    st.title('Generate Faces')
    st.markdown("Click Generate to Get Your Face!")
    if st.button('Generate'):
        st.image(image, use_column_width=True)
        st.title('Download Generated Face')
        st.markdown('Click to Download')

        # Give the user a link to download their image
        def get_image_download_link(img, file_label='File'):
            with open(img, 'rb') as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(img)}">Download {file_label}</a>'
            return href
        # CLickable link for the downloadable image.
        st.markdown(get_image_download_link(file, 'Generated Face'), unsafe_allow_html=True)
    else:
        pass

def write():
    """Method used to bring page into the app.py file"""
    with st.spinner("Loading ..."):
        stylegan = gen()

 # main page for app

import streamlit as st
import pandas as pd
import numpy as np
import time

def importCss(file_name):
    with open(file_name) as f:
        st.markdown("<style>{f.read}</style>", unsafe_allow_html=True)

importCss("./assets/styles/app.css")

bookOptions = [
    "https://via.placeholder.com/300.png?text=Image+1",
    "https://via.placeholder.com/300.png?text=Image+2",
    "https://via.placeholder.com/300.png?text=Image+3",
    "https://via.placeholder.com/300.png?text=Image+4",
]

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

def update_index(direction):
    if direction == 'right':
        st.session_state.current_index += 1
    elif direction == 'left':
        st.session_state.current_index -= 1
    st.session_state.current_index %= len(bookOptions)


current_option = bookOptions[st.session_state.current_index]

st.image(current_option, caption=f"Book {st.session_state.current_index + 1}")

if st.button(f"Select Book {st.session_state.current_index + 1}"):
    st.success(f"You selected Book {st.session_state.current_index + 1}!") #completes action after book has been selected

col1, col2 = st.columns(2)

with col1:
    if st.button('Previous'):
        update_index('left')
with col2:
    if st.button('Next'):
        update_index('right')


st.write("\n\n\n\n\n\n\n\n\n\n\n\n\n")

videoDisplay = st.Page("videoDisplay.py", title="Create entry", icon=":material/add_circle:")

pg = st.navigation([create_page, delete_page])

with st.form("my_form"):
    st.write("Create your own video!")
    script = st.text_input("Book script")
    submit = st.form_submit_button(label = "Submit")

st.write(script, "\n\n")


if st.button("video display"):
    st.switch_page("videoDisplay")

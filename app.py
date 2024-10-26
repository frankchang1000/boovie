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



col1, col2 = st.columns(2)

with col1:
    if st.button('Previous'):
        update_index('left')
with col2:
    if st.button('Next'):
        update_index('right')

st.image(current_option, caption=f"Book {st.session_state.current_index + 1}")

if st.button(f"Select Book {st.session_state.current_index + 1}"):
    st.success(f"You selected Book {st.session_state.current_index + 1}!") #completes action after book has been selected


st.write(f"Current Book Index: {st.session_state.current_index + 1}/{len(bookOptions)}")

st.write("\n\n\n\n\n\n\n\n\n\n\n\n\n")


with st.form("my_form"):
    st.write("Create your own video!")
    script = st.text_input("Book script")
    st.form_submit_button()

st.write(script)

def progressBar():
    st.write('Starting')
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'{i + 1}%')
        bar.progress(i + 1)
        time.sleep(0.05)

    st.write('Done downloading')

if(st.button("Start download")):
    progressBar()

import streamlit as st
import requests 
import os
import sys
from PIL import Image
from pathlib import Path
from io import BytesIO

st.title('Find A Park')

answer = st.text_input('Enter a park name:', value ='Acadia National Park')
if st.button('Search Park'):
    st.image(
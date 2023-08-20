import streamlit as st
st.set_page_config(
    page_title="Find A Park", #<------- Change this to the page you're currently on when copying/pasting after your imports
    page_icon="⛰️",
    menu_items={
        'About': """This is an app developed by 5 Peers at Coding Temple. Here are our
        Github accounts: \n\rHarrison : https://github.com/Acronine, \n\rJoshua : https://github.com/TechNTalk,
        \n\rLogan : https://github.com/Sir-Roe, \n\rVaidic: https://github.com/tvaidic"""})

import requests 
import os
import sys
from PIL import Image
from pathlib import Path
import pandas as pd
from io import BytesIO
import numpy as np
filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)
import myfuncs as mf
from tomongo import ToMongo
from collections import OrderedDict
c=ToMongo()
cursor=c.park_info.find()
df =  pd.DataFrame(list(cursor))

pk_list = df.full_name.tolist()
select= st.selectbox('Search a park', options=pk_list)
if select:
    st.subheader(select)
    
    for i in range(len(df['full_name'])):
        if select == df['full_name'][i]:
            link = (df['images'][i])
            index = i
    ran_num = np.random.randint(0, len(df['images'][index]))
    st.image(link[ran_num]['url'], caption=link[ran_num]['caption'])
    st.subheader('About The Park:')
    st.write(df['description'][index])
    st.subheader('Things to do:')
    act_string=''
    for act in df['activities'][index]:
        act_string +=act+', '
    st.markdown(act_string)
    st.subheader('Entrance fees and hours:')
    st.dataframe(mf.hour_sort(df['standard_hours'][index]))
    if type(df['entrance'][index]) == list:
        st.dataframe(pd.DataFrame({"Fee":df['entrance'][index],"Costs":df['cost'][index]}),hide_index=True)
    else:
        st.dataframe({"Fee":df['entrance'][index],"Costs":df['cost'][index]})
    st.subheader('Press the link for more info')
    st.write(df['url'][index])
    
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 21:18:34 2021

@author: THANGAMARIAPPAN.P
"""
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import pandas_bokeh


primaryColor="#2214c7"
backgroundColor="#ffffff"
secondaryBackgroundColor="#e8eef9"
textColor="#000000"
font="sans serif"

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="Map Marker",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="Logo.png",  # String, anything supported by st.image, or None.
)

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {5}rem;
        padding-left: {5}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: left; color: white;'>Map Marker</h2>", unsafe_allow_html=True)

# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
# Side Bar

st.markdown( f'''<style>
            section[data-testid="stSidebar"] .css-ng1t4o {{
                padding-top: 1rem;
                
            }}</style>''',unsafe_allow_html=True)

display = Image.open('Logo.png')
display = np.array(display)

st.sidebar.image(display, width = 300)
st.sidebar.title("Select your key_file")

key = st.sidebar.file_uploader('',type=['csv','xlsx'])

## Table
if key is not None:
    
    try:
        df = pd.read_csv(key)
    except:
        df = pd.read_excel(key)
    
    try:
    	lat = [i for i, elem in enumerate(list(df.columns)) if 'Lat' in elem]
    	lat = int(lat[0])
    except:
    	lat = 0
    try:
    	long = [i for i, elem in enumerate(list(df.columns)) if 'Long' in elem]
    	long = int(long[0])
    except:
    	long = 0
    try:
    	time = [i for i, elem in enumerate(list(df.columns)) if 'Event' in elem]
    	time = int(time[0])
    except:
    	time = 0
        
    st.sidebar.subheader("Select the variable")
    
    time_ = st.sidebar.selectbox('TimeStamp', df.columns,time)
    lat_ = st.sidebar.selectbox('Latitude', df.columns, lat)
    long_ = st.sidebar.selectbox('Longitude', df.columns, long)
    
    if st.sidebar.button("Load Data"):
        map_df = df.copy()
        map_df = map_df.rename({lat_: 'lat', long_: 'lon'}, axis='columns')
        st.map(map_df, use_container_width=True)
        # st.sidebar(visibility=False)
    
    if st.button("Export html"):
        pandas_bokeh.output_file(str(key.name)+".html")
        # pandas_bokeh.show
        df.plot_bokeh.map(x=str(long_), y=str(lat_),
                              tile_provider="OSM",
                              hovertool_string="""<h2> @{} </h2> 
                                                  <h3> Lat Long: @{} , @{}  </h3>                                     
                                                  <h3>  @{} </h3>""".format(None,lat_,long_,time_),
                            # size="size", 
                            figsize=(1300, 650),
                            # dropdown=["j", "i"],
                            title="Map Marker_"+ str(key.name) )
        map_df = df.copy()
        map_df = map_df.rename({lat_: 'lat', long_: 'lon'}, axis='columns')
        st.map(map_df)
        st.success('Export completed')
            

        
	



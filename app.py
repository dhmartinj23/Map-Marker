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
import os

if 'init' not in st.session_state: st.session_state['init']=False
if 'store' not in st.session_state: st.session_state['store']={}
if 'store_d' not in st.session_state: st.session_state['store_d']={}
if 'edit' not in st.session_state: st.session_state['edit']=True

if st.session_state.init == False:
    st.session_state.store_d = pd.DataFrame(columns =['lat','lon']) #{'A':[1,2,3,4], 'B':[7,6,5,4]}
    st.session_state.init = True
 
@st.cache(allow_output_mutation=True)
def fetch_data():
    return pd.DataFrame(st.session_state.store_d)

def saveDefault():
    st.session_state.store_d = st.session_state.store
    return

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

# display = Image.open('Logo.png')
# display = np.array(display)

# st.sidebar.image(display, width = 300)
# Update(map_df,30,30)

st.sidebar.subheader("Enter Your lat lon")

lat_input = st.sidebar.number_input("Latitude")
lon_input = st.sidebar.number_input("Longitude")


def Update(data_df,lat,lon):
    data_df.loc[len(data_df),['lat','lon']] = [lat,lon]

global map_df
map_df = fetch_data()        
map_display = st.sidebar.button("Update")

if map_display:
    map_df = fetch_data() 
    Update(map_df,lat_input,lon_input)
    st.session_state.store=map_df.to_dict()
    
# st.session_state.store=map_df.to_dict()

st.sidebar.subheader("Select your key_file")
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
        
        df = df.rename({lat_: 'lat', long_: 'lon'}, axis='columns')
        
        map_df = fetch_data() 
        map_df = map_df.append(df, sort=False)
        st.session_state.store = map_df.to_dict()
        # st.write(map_df)       
        # _DEFAULT_MAP = dict(deck_gl_json_chart.EMPTY_MAP)  
        # _DEFAULT_MAP["mapStyle"] = "mapbox://styles/mapbox/light-v11"
        # st.map(map_df)
    
    if st.button("Export html"):
        pandas_bokeh.output_file(os.path.dirname(os.path.abspath(str(key.name)+".html")))
        #p = pandas_bokeh.output_notebook
        map_df.plot_bokeh.map(x="lat", y="lon",
                              tile_provider="OSM",
                              hovertool_string="""<h2> @{} </h2> 
                                                  <h3> Lat Long: @{} , @{}  </h3>                                     
                                                  <h3>  @{} </h3>""".format(None,lat,lon,time_),
                            # size="size", 
                            figsize=(1300, 650),
                            # dropdown=["j", "i"],
                            title="Map Marker_"+ str(key.name) )
        data = open( os.path.dirname(os.path.abspath(str(key.name)+".html"))) #folder + str(key.name)+".html")
        st.download_button("Download as html",data=data, file_name = str(key.name)+".html")
        
        
st.map(map_df)
# st.sidebar.write(map_df)        
# os.path.dirname(os.path.abspath(str(key.name)+".html"))

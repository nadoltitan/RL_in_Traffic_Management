
import base64
import os
import json
import pickle
import uuid
import re

import streamlit as st
import pandas as pd


def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link


def file_selector(folder_path='https://github.com/nadoltitan/RL_in_Traffic_Management'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


st.markdown("""
                ## Reinforcement Learning in Traffic Management""")
image = Image.open('Traffic_congestion.jpg')
st.image(image)

if __name__ == '__main__':
    st.markdown("""
                
                [SUMO simulation](https://sumo.dlr.de/)
                for running the model and then you need to download the file named
                "ingolstadt7" and unzipit. Dowload other file called "Test_RL.zip"
                BUT YOU MUSTN'T UNZIP IT.
                When every file is ready you can run the code bellow from the python in your device.
                You will see the SUMO RL sitmulation that have been trained 
                You can read more about it in [This medium](https://medium.com/@nadoltitan1/%E0%B8%A5%E0%B8%94%E0%B8%9B%E0%B8%B1%E0%B8%8D%E0%B8%AB%E0%B8%B2%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%88%E0%B8%A3%E0%B8%B2%E0%B8%88%E0%B8%A3%E0%B8%95%E0%B8%B4%E0%B8%94%E0%B8%82%E0%B8%B1%E0%B8%94%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-reinforcement-learning-d3b9c6014863) 
                and [This Github](https://github.com/nadoltitan/RL_in_Traffic_Management)
                However, if you want to see the untrained model version which switch
                between red light and green light every 15 second, 
                you can run the file named "SUMO Configuration File (.sumocfg)". 
                It located the 'ingolstadt7' that have been unziped. 
                You can compare which one is better The AI version or The routine version.
                 """)

    st.markdown('-'*17)

    st.code('''
import sumo_rl
import supersuit as ss
from stable_baselines3.common.vec_env import VecMonitor
import supersuit
from pettingzoo.utils.env import ParallelEnv
import gym

from stable_baselines3 import A2C   
    
model = A2C.load("Test_RL") 
env = sumo_rl.env(net_file='sumo-rl-master/nets/RESCO/ingolstadt7/ingolstadt7.net.xml',
                  route_file='sumo-rl-master/nets/RESCO/ingolstadt7/osm.rou.xml',
                  use_gui=True,
                  delta_time = 10 ,
                  begin_time = 1000 ,
                  num_seconds= 10000)  
env = supersuit.pad_observations_v0(env)
env = supersuit.pad_action_space_v0(env)

env.reset()
for agent in env.agent_iter():

    observation, reward, done, info = env.last()
    action , _ = model.predict(observation)
    env.step(action)
    #print(observation,reward) ''' , language='python')

    # --------------------------
    # Select a file to download
    # --------------------------
    if st.checkbox('Select a file to download'):
        st.write('~> Use if you want to test uploading / downloading a certain file.')

        # Upload file for testing
        folder_path = st.text_input('Enter directory: deafult .', '.')
        filename = file_selector(folder_path=folder_path)

        # Load selected file
        with open(filename, 'rb') as f:
            s = f.read()

        download_button_str = download_button(s, filename, f'Click here to download {filename}')
        st.markdown(download_button_str, unsafe_allow_html=True)

        if st.checkbox('Show code example'):
            code_text = f"""
                        with open('{filename}', 'rb') as f:
                            s = f.read()
                        download_button_str = download_button(s, '{filename}', 'Click here to download {filename}')
                        st.markdown(download_button_str, unsafe_allow_html=True)"""

            st.code(code_text, language='python')

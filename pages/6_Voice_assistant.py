import base64
import streamlit as st
from pages.api.xi_audio import generate_xi_audio
import numpy as np
from pages.api.aichat import get_answer

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
        
st.write("# Voice assistant Page")

assistant = {'Rachel': '21m00Tcm4TlvDq8ikWAM', 'Domi': 'AZnzlk1XvdvUeBnXmlld', 'Bella': 'EXAVITQu4vr4xnSDxMaL', 'Antoni': 'ErXwobaYiN019PkySvjV', 'Elli': 'MF3mGyEYCl7XYWbV9V6O', 'Josh': 'TxGEqnHWrfWFTfGW9XjX', 'Arnold': 'VR6AewLTigWG4xSOukaG', 'Adam': 'pNInz6obpgDQGcFmaJgB', 'Sam': 'yoZ06aMxZJJ28mfd3POQ'}
option = st.selectbox(
    'Please select your assistant',
    ('Rachel', 'Domi', 'Bella', 'Antoni', 'Elli', 'Josh', 'Arnold', 'Adam', 'Sam'))


question = st.text_area('Text to convert (How to achieve and maintain safety?, Can you explain me how Training and checking is organized?)', '')


if st.button('Ask ', type = "primary"):
    voice_id = assistant[option]
    txt = get_answer(question)
    generate_xi_audio(voice_id, txt)
    

    autoplay_audio("output.mp3")

    # audio_file = open('output.mp3', 'rb')
    # audio_bytes = audio_file.read()
    # st.audio(audio_bytes, format='audio/mp3')



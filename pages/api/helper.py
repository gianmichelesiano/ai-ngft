import requests

from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()


def generate_xi_audio(voice_id, texts):
    print("generate_xi_audio")
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/"+voice_id

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": st.secrets['XI_API_KEY']
    }

    data = {
    "text": texts,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
            



import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

def create_supabase_client():
    load_dotenv()
    supabase_url =  st.secrets['SUPABASE_URL']
    supabase_key =  st.secrets['SUPABASE_KEY']
    client: Client = create_client(supabase_url, supabase_key)
    return client
import streamlit as st
from dotenv import load_dotenv
import os
from streamlit_supabase_auth import login_form


def get_sessio_auth():
    load_dotenv()
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    session_auth = login_form(
        url=supabase_url,
        apiKey=supabase_key,
    )
    return session_auth
import streamlit as st

import os
from streamlit_supabase_auth import login_form


def get_sessio_auth():

    supabase_url = st.secrets['SUPABASE_URL']
    supabase_key = st.secrets['SUPABASE_KEY']

    session_auth = login_form(
        url=supabase_url,
        apiKey=supabase_key,
    )
    return session_auth
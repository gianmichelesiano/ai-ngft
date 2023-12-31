import streamlit as st
from streamlit_supabase_auth import logout_button
from Auth import get_sessio_auth 

st.set_page_config(
    page_title="Ngft AI",
    page_icon="🗒️",
)

sessionAuth = get_sessio_auth()


if not sessionAuth:
    st.warning("Please login to continue")
    #st.stop()

with st.sidebar:
    st.write(f"Welcome")
    logout_button()
    
st.write("# Welcome to Ngft AI! 🗒️ to ")

st.markdown(
    """
    This is the main page of the Ngft AI app. Use the navigation bar on the left to browse the different pages.
"""
)
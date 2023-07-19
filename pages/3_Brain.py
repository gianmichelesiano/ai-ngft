import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
import random
from Auth import get_sessio_auth 
from pages.api.client import create_supabase_client


def initialize_session_state():
    if "list" not in st.session_state:
        st.session_state.list = True
    if "add" not in st.session_state:
        st.session_state.add = False


def change_status():
    st.session_state.list = False
    st.session_state.add = True


def save_brain():
    st.warning("Not implemented yet")
    st.session_state.list = True
    st.session_state.add = False

sessionAuth = get_sessio_auth()
if not sessionAuth:
    st.warning("Please login to continue")
    st.stop()
    
st.write("# Brain Page")

initialize_session_state()
supabase = create_supabase_client()
if st.session_state.add:
    st.write("Add new Brain")
    st.text_input("Brain Name", key="brain_name")
    docs = supabase.table('docs').select('id','name').execute()
    data = [i['name'] for i in docs.data]
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)
    st.button("Save bRAIN", on_click=save_brain)
    

if st.session_state.list:
    st.button("Add Brain", on_click=change_status)
    st.write("List Brain")
    
    response = supabase.table('brain').select('*, brain_2_docs(*)').execute()

    
    list_brain = []
    list_docs = []

    for item in response.data:
        list_brain.append(item['name'])
        list_doc = []
        for doc in item['brain_2_docs']:
            doc_name = supabase.table('docs').select('id','name').eq('id', doc['docs_id']).execute()
            list_doc.append(doc_name.data[0]['name'])
        list_docs.append(", ".join(list_doc))

    df = pd.DataFrame(
        {
            "brain": list_brain,
            "docs": list_docs,
        }
    )
    st.dataframe(
        df,
        column_config={
            "brain": "Brain",
            "docs": "docs"
        },
        hide_index=True,
    )
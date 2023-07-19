import streamlit as st
from pages.api.services import get_documents_list
from Auth import get_sessio_auth 
from pages.api.client import create_supabase_client

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def on_click_load():
    st.session_state.content = ''

    if len(selected_docs) != 1:
        st.warning("Please select a document to load")
    else:
        doc = selected_docs[0]
        response = supabase.table('documents').select('content').eq('metadata->>source', doc).execute()

        cont = ''
        for res in response.data:
            cont = cont + res['content']
        st.session_state.content = cont


def on_click_delete():
    st.session_state.content = ''

    
    if len(selected_docs) == 0:
        st.warning("Please select a document to delete")
    else:
        for doc in selected_docs:

            supabase.table('documents').delete().eq('metadata->>source', doc).execute()
            supabase.table('docs').delete().eq('name', doc).execute()


st.write("# Explore uploaded data")
st.subheader("# View or delete stored data")

supabase = create_supabase_client()
sessionAuth = get_sessio_auth()
if not sessionAuth:
    st.warning("Please login to continue")
    st.stop()

docs = get_documents_list(sessionAuth['user']['id'])    
for i in docs:
    st.checkbox(i, key='dynamic_checkbox_' + i)

selected_docs = get_selected_checkboxes()
if len(selected_docs) > 0:
    st.button("Delete selected docs", type="secondary", on_click=on_click_delete)

contents = ''
if len(selected_docs) == 1:
    st.button("Load selected docs", type="primary", on_click=on_click_load)
    
if "content" not in st.session_state:
    st.session_state.content = ''
if len(selected_docs) == 0:
    st.session_state.content = ''
    
st.write(st.session_state.content)


# for item in lista:
#     files_placeholder = st.container()
#     with files_placeholder:
#         cols = st.columns((6,1,1))
#         cols[0].write("File name")
#         cols[1].button("View", type="primary", key=f"view_{item}", )
#         cols[2].button("Delete", type="secondary", key=f"delete_{item}")
    
    



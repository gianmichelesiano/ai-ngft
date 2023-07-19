import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
import random
from Auth import get_sessio_auth 
from pages.api.client import create_supabase_client


sessionAuth = get_sessio_auth()
if not sessionAuth:
    st.warning("Please login to continue")
    st.stop()
    
st.write("# Users Page")

supabase = create_supabase_client()
users = supabase.auth.admin.list_users()

  
list_uuid = []
list_mail = []

for user in users:
    list_uuid.append(user.id)
    list_mail.append(user.email) 

df = pd.DataFrame(
    {
        "uuid": list_uuid,
        "email": list_mail,
    }
)
st.dataframe(
    df,
    column_config={
        "uuid": "UUID",
        "email": "email"
    },
    hide_index=True,
)
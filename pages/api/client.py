

import os
from supabase import create_client, Client
from dotenv import load_dotenv

def create_supabase_client():
    load_dotenv()
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    client: Client = create_client(supabase_url, supabase_key)
    return client
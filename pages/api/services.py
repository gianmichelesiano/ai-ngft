import json
from pages.api.client import create_supabase_client


def get_documents_list(uuid):
    client = create_supabase_client()
    response = client.table('docs').select("*").eq('owner', uuid).execute()
    data_json = json.loads(response.json())
    data_entries = data_json['data']
    documents = []
    for i in range(len(data_entries)):
        document = data_entries[i]['name']
        documents.append(document)
    return documents

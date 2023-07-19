import os
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from pages.api.client import create_supabase_client


def get_answer(query):
    print(query)
    supabase = create_supabase_client()
    embeddings = OpenAIEmbeddings()
    
    vector_store = SupabaseVectorStore( supabase, embeddings, table_name='documents')
    
    
    matched_docs = vector_store.similarity_search_with_relevance_scores(query)
    print(matched_docs)
    document_list = [document for document, _ in matched_docs]
    new_vector_store = SupabaseVectorStore.from_documents(document_list, embeddings, client=supabase)


    # completion llm
    llm = ChatOpenAI(
        openai_api_key="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",
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=new_vector_store.as_retriever(),
    )

    return qa.run(query)

import streamlit as st
from pages.api.services import get_documents_list
from pages.api.client import create_supabase_client
from PyPDF2 import PdfReader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import SupabaseVectorStore
from Auth import get_sessio_auth 
import os

def get_pdf_text(pdf_docs):
    text = ""
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_superbase_vectorstore(text, pdf_filename, supabase):
    documents = []
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    for text in chunks:
        metadata = {"source": pdf_filename}
        doc  =  [Document(page_content=text, metadata=metadata)]
        documents = documents + doc
    SupabaseVectorStore.from_documents(documents, embeddings, client=supabase)
    return chunks


sessionAuth = get_sessio_auth()
if not sessionAuth:
    st.warning("Please login to continue")
    st.stop()
    
docs = get_documents_list(sessionAuth['user']['id'])
supabase = create_supabase_client()


st.write("# Upload Page")
st.subheader("Upload file:") 
pdf_docs = st.file_uploader(
    "Upload your files here and click on 'Process'")

if st.button("Process", type = "primary"):
    with st.spinner("Processing"):
        if pdf_docs:
            file_extension = pdf_docs.name.split('.')[1]  
            if pdf_docs.name not in docs:
                
                docs.append(pdf_docs.name)
                if file_extension == "pdf":
                    raw_text = get_pdf_text(pdf_docs)
                    vectorstore = get_superbase_vectorstore(raw_text, pdf_docs.name, supabase)
                    data, count = supabase.table('docs').insert({"name": pdf_docs.name, "owner": sessionAuth['user']['id']}).execute()
                    st.success("Uploaded")
                else:
                    st.warning("Format invalid you can upload only pdf files")
            else:
                st.warning("This document is already uploaded")
        else:
            st.warning("Please upload a file first")
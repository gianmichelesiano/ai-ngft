import streamlit as st
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI
import faiss
from contextlib import redirect_stdout
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
SERPAPI_API_KEY = st.secrets['SERPAPI_API_KEY']


st.sidebar.title("AutoGPT Parameters")
ai_name = st.sidebar.text_input(
    "AI Name",
    value="Q",
    help="Enter the name of your AI agent.",
)
ai_role = st.sidebar.text_input(
    "AI Role",
    value="Research Assistant",
    help="Enter the role of your AI agent.",
)
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    help="Set the randomness of the AI's responses. Higher values produce more random outputs.",
)

search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    WriteFileTool(),
    ReadFileTool(),
]

embeddings_model = OpenAIEmbeddings()
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

agent = AutoGPT.from_llm_and_tools(
    ai_name=ai_name,
    ai_role=ai_role,
    memory=vectorstore.as_retriever(),
    tools=tools,
    llm=ChatOpenAI(temperature=temperature),
)

class StreamlitOutput:
    def __init__(self):
        self.buffer = ""

    def write(self, data):
        self.buffer += data
        if 'File written successfully to ' in data:
            match = re.search(r'File written successfully to ([\w\.-]+)\.', data)
            if match:
                file_path = match.group(1)
                if 'file_paths' not in st.session_state:
                    st.session_state.file_paths = []
                if file_path not in st.session_state.file_paths:
                    st.session_state.file_paths.append(file_path)

output = StreamlitOutput()


def load_files():
    # If 'file_paths' exists in the session state, iterate through each file path
    if 'file_paths' in st.session_state:
        for file_path in st.session_state.file_paths:
            # Check if the file still exists
            if os.path.exists(file_path):
                # If the file exists, create a download button for it
                with open(file_path, "rb") as file:
                    file_data = file.read()
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=file_data,
                    file_name=os.path.basename(file_path),
                    mime="text/plain",
                    key=file_path  # Use the file path as the key
                )
            else:
                # If the file doesn't exist, remove it from 'file_paths'
                st.session_state.file_paths.remove(file_path)
    else:
        # If 'file_paths' doesn't exist in the session state, create it
        st.session_state.file_paths = []
        
        
st.title('Autonomous Assistant')

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
st.session_state.user_input = st.text_input("Please enter your command (write a weather report for Zurich today)", st.session_state.user_input)

if st.button('Run'):
    if st.session_state.user_input:
        with redirect_stdout(output):
            result = agent.run([st.session_state.user_input])
        st.session_state.model_output = output.buffer
        st.session_state.result = result
        load_files()
        st.session_state.files_loaded = True

# If any of the download buttons was clicked, re-render them
if 'file_paths' in st.session_state:
    for index, file_path in enumerate(st.session_state.file_paths):
        widget_key = f"{file_path}_{index}"  # Use the unique widget key
        if st.session_state.get(widget_key, False):  # Check if the button was clicked
            load_files()

# Display the model output if it's in the session state
if 'model_output' in st.session_state:
    st.write(f"Result: {st.session_state.result}")
    expander = st.expander("Model Output")
    expander.text(st.session_state.model_output)
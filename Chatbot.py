import os
from openai import OpenAI
import streamlit as st

from loaders.indexer import run_indexer
from main import get_prompt, ask

# Constants
VS_BASE_DIRECTORY = 'vector_stores'  # Change this to your desired directory

# Utility Functions
def list_folders(directory):
    """List all folders in a given directory."""
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def create_new_folder(directory, folder_name):
    """Create a new folder in the specified directory."""
    new_folder_path = os.path.join(directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        st.success(f"Folder '{folder_name}' created successfully!")
    else:
        st.warning(f"Folder '{folder_name}' already exists!")

def save_uploaded_file(uploaded_file, save_dir):
    """Save an uploaded file to the specified directory."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Create the directory if it doesn't exist
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())  # Write the uploaded file to the filesystem
    st.success(f"Saved file: {uploaded_file.name} in {save_dir}")

# Session state initialization
if "vector_store_name" not in st.session_state:
    st.session_state["vector_store_name"] = None
if "internal" not in st.session_state:
    st.session_state["internal"] = [{"role": "assistant", "content": "How can I help you?"}]
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Sidebar: API key and Vector Store Selection
with st.sidebar:
    st.subheader("Step 1: Add your OpenAI API Key")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    # Vector Store Creation
    st.subheader("Step 2: Create or Select a Knowledge Base")
    
    # Create a new vector store
    st.subheader("Create a New Vector Store")
    new_folder_name = st.text_input("Enter the name of the new vector store")
    if st.button("Create Vector Store"):
        if new_folder_name:
            create_new_folder(VS_BASE_DIRECTORY, new_folder_name)
        else:
            st.error("Please enter a valid folder name.")

    st.subheader("OR")

    # List existing vector stores
    st.subheader("Vector Stores (Knowledge Base)")
    folders = list_folders(VS_BASE_DIRECTORY)
    if folders:
        st.write("Available knowledge bases:")
        selected_folder = st.selectbox("Vector Stores", folders, index=folders.index(st.session_state.vector_store_name) if st.session_state.vector_store_name else None)
        if st.session_state["vector_store_name"] != selected_folder:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
            st.session_state["vector_store_name"] = selected_folder

    # File Upload Section
    st.subheader("Step 3: Upload a PDF file to the knowledge base")
    st.title("File Upload")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    if uploaded_file:
        save_directory = f"data/{st.session_state.vector_store_name}"
        save_uploaded_file(uploaded_file, save_directory)
        st.write(f"File {uploaded_file.name} has been uploaded and saved to the '{save_directory}' directory.")
        run_indexer(f"vector_stores/{st.session_state.vector_store_name}")

# Chatbot Section
st.title("💬 Knowledge Base Assistant")
st.caption(f"🚀 A simplified RAG solution - Selected knowledge base: {st.session_state.vector_store_name}")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
if prompt := st.chat_input():
    # Use environment variable API key if available
    if os.getenv('OPENAI_API_KEY'):
        openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    new_prompt, sources = get_prompt(prompt, f"vector_stores/{st.session_state.vector_store_name}")
    
    # Update session messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.internal.append({"role": "user", "content": new_prompt})
    
    # Display user prompt
    st.chat_message("user").write(prompt)
    
    # Get response from the assistant
    response = ask(st.session_state.internal)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.internal.append({"role": "assistant", "content": response})
    
    # Display assistant response
    st.chat_message("assistant").write(response)

from uuid import uuid4
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import glob

def return_vector_store(index_name: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index = faiss.IndexFlatL2(len(embeddings.embed_query(index_name)))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    ) 

    return vector_store   

def load_pdf(vector_store_name):
    documents = []
    files = glob.glob(f"./{os.environ.get('DATA_PATH', 'data')}/{vector_store_name}/*.pdf")
    for pdfFile in files:
        print(f"Loading {pdfFile}")
        loader = PyPDFLoader(
            pdfFile,
        )
        documents.extend(loader.load())
    return documents    

def load_documents():
    loader = DirectoryLoader(os.environ.get('DATA_PATH', 'data'), glob="*.pdf")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks

def run_indexer(vector_store_name):
    documents = load_pdf(vector_store_name.split("/")[-1])
    if documents is None:
        raise Exception("No Documents Found to be loaded check env variables")
    chunks = split_text(documents)
    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store = return_vector_store("default")
    vector_store.add_documents(documents=chunks, ids=uuids)
    vector_store.save_local(vector_store_name)

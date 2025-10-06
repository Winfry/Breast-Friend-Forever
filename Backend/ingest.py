# backend/ingest.py
import os, glob
from langchain.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = "chroma_store"

def load_and_chunk(file_path):
    loader = UnstructuredPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    return splitter.split_documents(docs)

def ingest_files(folder="docs"):
    emb = OpenAIEmbeddings()
    client = chromadb.Client(chromadb.config.Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name="breast_docs", embedding_function=embedding_functions.StripFn(emb.embed_query))
    for f in glob.glob(os.path.join(folder, "*")):
        chunks = load_and_chunk(f)
        for i, c in enumerate(chunks):
            metadata = {"source": os.path.basename(f)}
            collection.add(
                documents=[c.page_content],
                metadatas=[metadata],
                ids=[f"{os.path.basename(f)}_{i}"]
            )
    client.persist()
    print("Docs ingested successfully.")

if __name__ == "__main__":
    ingest_files()
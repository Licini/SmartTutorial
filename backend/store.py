import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader("data", recursive=True).load_data(show_progress=True)
print("making index")
index = VectorStoreIndex.from_documents(documents, show_progress=True)
index.storage_context.persist(persist_dir="store")

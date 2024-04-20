import os
from llama_index.core import StorageContext, load_index_from_storage

print("loading storage")
storage_context = StorageContext.from_defaults(persist_dir="store")
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

while True:
    query = input("Enter a query: ")
    if query == "exit":
        break
    response = query_engine.query(query)
    print(response)

from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage


Settings.llm = OpenAI(model="gpt-4")

documents = SimpleDirectoryReader("data/compas/src/compas", recursive=True).load_data(show_progress=True)
index = VectorStoreIndex.from_documents(
    documents, show_process=True
)
index.storage_context.persist(persist_dir="store2")

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="store2")

# load index
index = load_index_from_storage(storage_context)


chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)
while True:
    query = input("Enter a query: ")
    streaming_response = chat_engine.stream_chat(query)
    for token in streaming_response.response_gen:
        print(token, end="")

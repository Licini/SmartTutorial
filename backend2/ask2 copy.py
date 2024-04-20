

from openai import OpenAI
from annoy import AnnoyIndex
import json

embeddings = json.load(open("embeddings.json"))

client = OpenAI()
u = AnnoyIndex(3072, 'angular')
u.load('embeddings.ann') # super fast, will just mmap the file
# print(u.get_nns_by_item(0, 1000)) # will find the 1000 nearest neighbors

def ask(message, context_length=8):
    response = client.embeddings.create(
        input=message,
        model="text-embedding-3-large"
    )
        
    embedding = response.data[0].embedding

    results = u.get_nns_by_vector(embedding, context_length, include_distances=False)
    for result in results:
        print(embeddings[result]["path"], embeddings[result]["chunk"])
    all_files = [embeddings[result]["path"] for result in results]
    all_files = list(set(all_files))
    
    context = "Following are the relevant context: \n\n"
    for result in results:
        context += open(embeddings[result]["path"], 'r').read()
    

    # Create an assistant using the file ID
    assistant = client.beta.assistants.create(
        instructions="You are a tutorial generator that generates compas example codes based on the files provided.",
        model="gpt-4-turbo",
        tools=[{"type": "file_search"}],
    )

    # Create a vector store caled "Financial Statements"
    vector_store = client.beta.vector_stores.create(name="COMPAS source code")
    
    # Ready the files for upload to OpenAI 
    file_streams = [open(path, "rb") for path in all_files]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    
    # You can print the status and the file counts of the batch to see the result of this operation. 
    print(file_batch.status)
    print(file_batch.file_counts)

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": message,
        }
    ]
    )
    
    # The thread now has a vector store with that file in its tool resources.
    print(thread.tool_resources.file_search)


    from typing_extensions import override
    from openai import AssistantEventHandler
    
    # First, we create a EventHandler class to define
    # how we want to handle the events in the response stream.

    class EventHandler(AssistantEventHandler):    
        @override
        def on_text_created(self, text) -> None:
            print(f"\nassistant > ", end="", flush=True)
            
        @override
        def on_text_delta(self, delta, snapshot):
            print(delta.value, end="", flush=True)
            
        def on_tool_call_created(self, tool_call):
            print(f"\nassistant > {tool_call.type}\n", flush=True)
    
        def on_tool_call_delta(self, delta, snapshot):
            if delta.type == 'code_interpreter':
                if delta.code_interpreter.input:
                    print(delta.code_interpreter.input, end="", flush=True)
                if delta.code_interpreter.outputs:
                    print(f"\n\noutput >", flush=True)
                    for output in delta.code_interpreter.outputs:
                        if output.type == "logs":
                            print(f"\n{output.logs}", flush=True)
    
    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        # instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()


if __name__ == "__main__":
    while True:
        response = ask(input("Enter a query: "))
        # print(response["response"])
    
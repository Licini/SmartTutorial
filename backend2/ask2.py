

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
    

    # Upload a file with an "assistants" purpose
    files = []
    for result in results:
        file = client.files.create(
            file=open(embeddings[result]["path"], 'rb'),
            purpose='assistants'
        )
        files.append(file)

    # Create an assistant using the file ID
    assistant = client.beta.assistants.create(
        instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
        model="gpt-4-turbo",
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
            "file_ids": [file.id for file in files]
            }
        }
    )

    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?",
            "attachments": [
                {
                "file_id": file.id,
                "tools": [{"type": "code_interpreter"}]
                }
            ]
            }
        ]
    )



    return {
        "response": response.choices[0].message.content,
        "files": all_files
    }


if __name__ == "__main__":
    while True:
        response = ask(input("Enter a query: "))
        print(response["response"])
    
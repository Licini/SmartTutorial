from openai import OpenAI
from annoy import AnnoyIndex
import json

software = "compas"

embeddings = json.load(open(f"embeddings_{software}.json"))

client = OpenAI()
u = AnnoyIndex(3072, 'angular')
u.load(f'embeddings_{software}.ann')

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
    
    context = "Following are the relevant source code: \n\n"
    for result in results:
        context += open(embeddings[result]["path"], 'r').read()
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"You are a tutorial generator that generates {software} example codes based on given source code, reply in markdown format."},
            {"role": "user", "content": context},
            {"role": "user", "content": message},
        ])
    # print(response.choices[0].message.content)

    return {
        "response": response.choices[0].message.content,
        "files": all_files
    }


if __name__ == "__main__":
    while True:
        response = ask(input("Enter a query: "))
        print(response["response"])
    
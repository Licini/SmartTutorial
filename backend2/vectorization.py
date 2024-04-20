import os
from openai import OpenAI
client = OpenAI()

def get_files(path):
    # Get all .py files and .rst files.
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".rst") or filename.endswith(".js"):
                files.append(os.path.join(root, filename))
    return files


def vectorisation(path):

    def chunk_text(text, max_tokens=8192):
    # Splitting the text into chunks of approximately max_tokens tokens each
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks


    text = open(path, 'r').read()

    chuncks = chunk_text(text)
    results = []

    print(f"Processing {len(chuncks)} chunks")

    for i, chunk in enumerate(chuncks):
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-3-large"
        )
        
        result = {
            "path": path,
            "chunk": i,
            "embedding": response.data[0].embedding
        }

        results.append(result)

    return results

if __name__ == "__main__":
    import json

    software = "threejs"
    files = get_files(f"data/{software}")
    all_embeddings = []
    print(len(files))
    for i, file in enumerate(files):
        print(f"Processing file {i+1}/{len(files)}: {file}")
        embeddings = vectorisation(file)
        all_embeddings.extend(embeddings)

    json.dump(all_embeddings, open(f"embeddings_{software}.json", "w"))
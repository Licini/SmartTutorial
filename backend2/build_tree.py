from annoy import AnnoyIndex
import json

embeddings = json.load(open("embeddings.json"))

f = 3072  # Length of item vector that will be indexed

t = AnnoyIndex(f, 'angular')

for i, e in enumerate(embeddings):
    t.add_item(i, e["embedding"]) 


t.build(10) # 10 trees
t.save('embeddings.ann')
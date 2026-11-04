from pronto import Ontology
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np
import faiss
import json
import pickle

import sys

ONTOLOGY_FILE = sys.argv[1]

print("Loading ontology...")
ont = Ontology(ONTOLOGY_FILE)

records = []

for term in ont.terms():

    label = term.name or ""

    synonyms = []
    if hasattr(term, "synonyms"):
        synonyms = [s.description for s in term.synonyms]

    definition = ""
    try:
        if term.definition:
            definition = term.definition
    except:
        pass

    text = f"""
    Label: {label}
    Synonyms: {"; ".join(synonyms)}
    Definition: {definition}
    """

    records.append(
        {
            "id": term.id,
            "label": label,
            "text": text
        }
    )

print(f"Terms loaded: {len(records)}")

model = SentenceTransformer(
    "intfloat/multilingual-e5-large"
)
texts = [
    f"passage: {r['text']}"
    for r in records
]

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)

embeddings = np.array(
    embeddings,
    dtype=np.float32
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(
    index,
    "ontology.faiss"
)

with open("ontology_metadata.pkl", "wb") as f:
    pickle.dump(records, f)

print("Done.")
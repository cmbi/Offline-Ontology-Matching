import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

index = faiss.read_index(
    "ontology.faiss"
)

with open("ontology_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

model = SentenceTransformer(
    "intfloat/multilingual-e5-large"
)

while True:

    query = input("> ")

    q_emb = model.encode(
        [query],
        normalize_embeddings=True
    )

    q_emb = np.array(
        q_emb,
        dtype=np.float32
    )

    scores, ids = index.search(
        q_emb,
        10
    )

    for score, idx in zip(
        scores[0],
        ids[0]
    ):
        item = metadata[idx]

        print(
            f"{score:.3f} | "
            f"{item['id']} | "
            f"{item['label']}"
        )

    print()
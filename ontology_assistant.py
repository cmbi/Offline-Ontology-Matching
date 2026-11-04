import faiss
import pickle
import numpy as np
import ollama

from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Configuration
# --------------------------------------------------

FAISS_INDEX = "ontology.faiss"
METADATA_FILE = "ontology_metadata.pkl"

EMBEDDING_MODEL = "intfloat/multilingual-e5-large"

# Small local model
LLM_NAME = "qwen2.5:1.5b"

TOP_K = 5

# --------------------------------------------------
# Load resources
# --------------------------------------------------

print("Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX)

print("Loading metadata...")
with open(METADATA_FILE, "rb") as f:
    metadata = pickle.load(f)

print("Loading embedding model...")
embed_model = SentenceTransformer(EMBEDDING_MODEL)

print("Ready!\n")


def retrieve_concepts(query, top_k=TOP_K):
    """
    Retrieve the most similar ontology concepts.
    """

    query_embedding = embed_model.encode(
        [f"query: {query}"],
        normalize_embeddings=True
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    scores, ids = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], ids[0]):

        if idx < 0:
            continue

        item = metadata[idx]

        results.append(
            {
                "score": float(score),
                "id": item["id"],
                "label": item["label"],
                "text": item["text"]
            }
        )

    return results


def build_prompt(question, concepts):

    context = []

    for c in concepts:

        context.append(
            f"""
Similarity: {c['score']:.3f}

Concept ID: {c['id']}
Label: {c['label']}

Description:
{c['text']}
"""
        )

    joined_context = "\n".join(context)

    prompt = f"""
You are a biomedical ontology assistant.

A user has provided the following clinical description:

{question}

The ontology search system retrieved these candidate concepts:

{joined_context}

Tasks:

1. Select the best matching ontology concept.
2. Explain why it matches.
3. Provide a confidence score (0-100).
4. List alternative concepts if relevant.
5. Be concise and scientific.

Return the answer in Markdown.
"""

    return prompt


def ask_llm(prompt):

    response = ollama.chat(
        model=LLM_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# Main loop
# --------------------------------------------------

while True:

    question = input("Question (or 'exit'): ")

    if question.lower() in ["exit", "quit"]:
        break

    concepts = retrieve_concepts(question)

    print("\nTop Retrieved Concepts")
    print("=" * 60)

    for c in concepts:
        print(
            f"{c['score']:.3f} | {c['id']} | {c['label']}"
        )

    print("\nGenerating answer...\n")

    prompt = build_prompt(
        question,
        concepts
    )

    answer = ask_llm(prompt)

    print("=" * 60)
    print(answer)
    print("=" * 60)
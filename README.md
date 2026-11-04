# Offline Ontology Matching

A lightweight tool for finding ontology concepts using semantic search, entirely on your own machine. The project supports multilingual queries and can optionally provide human-readable explanations of the matches using a local LLM.

## Features

- ✅ Runs entirely offline after initial setup
- ✅ Keeps sensitive data on your local machine
- ✅ Supports multilingual queries (e.g. English, Spanish, French, Dutch)
- ✅ Works with OWL ontologies
- ✅ Fast semantic matching using vector search
- ✅ Optional AI-generated explanations

## How It Works

```text
Ontology (OWL)
    ↓
Embeddings (multilingual-e5-large)
    ↓
FAISS Vector Index
    ↓
Semantic Search
    ↓
Best Matching Concepts
```

The matching itself is performed using embeddings and vector similarity search.

## Installation

It is recommended to install the project in a dedicated Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build the Index

Place your ontology file (for example [`nmdo.owl`](https://github.com/NeuromuscularDisease/neuromuscular-disease-ontology/blob/main/nmdo-full.owl)) in the project folder and generate the vector index:

```bash
python build_embeddings.py ontology_file.owl
```

This is a one-time step and may take several minutes depending on the size of the ontology.

## Search

Retrieve the most relevant ontology concepts:

```bash
python search.py
```

## Optional: Semantic Search with Explanations

If you would like the tool to explain why a concept was selected, you can enable a local LLM.

Install an Ollama-compatible model:

```bash
ollama pull qwen2.5:1.5b
```

This repository uses **Qwen 2.5 1.5B** in the examples because it offers a good balance between quality, speed, and CPU usage, making it suitable for typical laptops and desktop computers. If your hardware allows it, you can use any Ollama-compatible model by changing the model name in the code.

### Run the Assistant

Start the local Ollama server:

```bash
ollama serve
```

Then, in a second terminal:

```bash
python ontology_assistant.py
```

The assistant will retrieve the most relevant ontology concepts and provide a short explanation of why they were selected.

> **Note:** The LLM is only used to explain the retrieved matches. Ontology matching itself is always performed using embeddings and vector search.
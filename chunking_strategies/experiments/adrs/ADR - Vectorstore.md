# Which Vector Store should be used to Store Embeddings

## Context and Problem Statement

To store out chunks for retrieval, we require a vector database capability

## Considered Options

- ChromaDB
- Azure AI Search

## Decision Outcome

- ChromaDB - selected for simplicity. The repo is intended to highlight the decision process specifically around chunking strategies. More complex topics like index design, hybrid search and re-ranking where AI search add value will be covered in separate experiments.
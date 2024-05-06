# Which Similariy Metric to use for Retrieval

## Context and Problem Statement

When retrieving documents from a vector database, we need to select those that are "similar" to our query. This is done via comparing embeddings vectors. 

## Considered Options
- HNSW: Cosine Similarity

## Decision Outcome

HNSW: Cosine Similarity: Cosine similarity is a mathematical operation that is most popular and easy to understand. We apply this is the HNSW due to the performance over more exhaustive clustering methods.



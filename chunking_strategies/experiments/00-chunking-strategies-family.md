---
template-version: 2023-12-07.1
status: "{proposed}"
date: 2024-04-15
creators: Guy Bourne, Anastasia Gromova
reviewers: {list everyone who reviewed the experiment}
keywords: {list of keywords to help with search relevancy}
---
# Experiment Family: Chunking Strategies

## Summary

Overall experiment description from the Garden:

This experiment family is intended to highlight the decision process for selecting a chunking strategy and is part of a broader educational asset, which includes notebooks and azure implementations of considered approaches to generative ai solutions. 

One of the challenges of vector-store-grounded LLM scenarios (RAG) is the quality of search results. This is partially due to embedding issues, and partially due to what we embed. We need to better understand the performance characteristics of our choice for what we embed - our default solution is to chunk the documents and embed overlapping chunks, but there are other options - embedding summarizations, using an LLM to generate question/answer pairs that it believes the document can answer, and embedding those, etc. In a domain-specific scenario, where embeddings tend to cluster and it can be hard to tease out relevant results for a particular query against large document chunks, how do these other options impact search relevance?

This describes several possible experiments - in this document we will be focused on the impact of chunking strategies on overall search relevance.

## Outline

"Chunking Strategies" consists (currently) of 4 main experiments:

- [baseline](./00-chunking-strategies-family.md)
- [Recursive Chunking](./02-chunking-strategies-recursive.md)
- [Topic Based Chunking](./03-chunking-strategies-topics.md)
- [Semantic Chunking](./04-chunking-strategies-semantic.md)

These experiments depend on the following:
- [ADR - Data](adrs/ADR%20-%20Data.md)
- [ADR - Embedding Model](adrs/ADR%20-%20Embedding%20Model.md)
- [ADR - Generation Step Model](adrs/ADR%20-%20Generation%20Step%20Model.md)
- [ADR - QA Gen Model](adrs/ADR%20-%20QA%20Gen%20Model.md)
- [ADR - Similarity Metrics](adrs/ADR%20-%20Similarity%20Metrics.md)
- [ADR - Topic Modelling Approach](adrs/ADR%20-%20Topic%20Modelling%20Approach.md)
- [ADR - Vectorstore](adrs/ADR%20-%20Vectorstore.md)

## Plan

To start the experiment, we must select appropriate constants for the experiment family - this will be done in the ADRs.

We will begin with an exploration of the data, and in particular focus on understanding how to look at documents, and understand the relationship of document attributes (e.g. length) to selecting a chunking strategy. We will explore the definition of a chunk and what makes a "good" chunk, which we will aim to tie to our measurement criteria.

We will then define a chunking and evaluation harnesses to be used across the experiments, starting with the baseline. After each experiment, we will review and publish the results that have been captured in AI Studio. 

Given that all experiments depend on the baseline, the experiment dependency graph looks like:

```mermaid
graph TD;
  p0["ADR: Data"]
  p1["ADR: Embedding Model"]
  p2["ADR: Generation Step Model"]
  p3["ADR: QA Gen Model"]
  p4["ADR: Vectorstore"]
  p5["ADR - Topic Modelling Approach"]
  p6["ADR - Similarity Metrics"]
  e0["Baseline experiment"]
  e1["Recursive Chunking"]
  e2["Topic Based Chunking"]
  e3["Semantic Chunking"]
  p0 --> e0
  p1 --> e0
  p2 --> e0
  p3 --> e0
  p4 --> e0
  p5 --> e2
  p6 --> e0
  p6 --> e3
  e0 --> e1
  e0 --> e2
  e0 --> e3
```

## Dependencies

### Data
<!-- Optional if experiment family does not require data -->
For this experiment we will be using the [Scientific Papers](https://huggingface.co/datasets/scientific_papers) dataset from Hugging Face. Given the size of the dataset, and the educational nature of the experiment family we will apply to following constraints:
- We will exclude documents that are excessively large
- We will exlcude documents that appear corrupted or erroneous
- We will subset the data down to a random sample of <X> documents 


### Measure of Success
<!-- Creator should fill this in -->

We will be using he OOTB evaluation metrics from Azure AI Studio. These are:
- Coherence
- Fluency
- Groundedness
- Relevance
- Similarity
- Retrieval Score
- F1 Score

For more information on these metrics see the [AI Studio documentation](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-metrics-built-in?tabs=warning)

## More Information
<!-- Optional -->

{ Any additional links or details that may help crews come up to speed quickly and be more effective.}
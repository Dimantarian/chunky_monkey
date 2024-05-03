---
status: "proposed"
date: 2024-04-15
creator: guybourne
experimenters: 
---

# Chunking Strategies: Topic Based Chunking

## Experiment Summary

Overall experiment description from the Garden:

This experiment family is intended to highlight the decision process for selecting a chunking strategy and is part of a broader educational asset, which includes notebooks and azure implementations of considered approaches to generative ai solutions. 

One of the challenges of vector-store-grounded LLM scenarios (RAG) is the quality of search results. This is partially due to embedding issues, and partially due to what we embed. We need to better understand the performance characteristics of our choice for what we embed - our default solution is to chunk the documents and embed overlapping chunks, but there are other options - embedding summarizations, using an LLM to generate question/answer pairs that it believes the document can answer, and embedding those, etc. In a domain-specific scenario, where embeddings tend to cluster and it can be hard to tease out relevant results for a particular query against large document chunks, how do these other options impact search relevance?

This describes several possible experiments - in this document we will be focused on the impact of chunking strategies on overall search relevance.

### Hypothesis
<!-- Creator should fill this in -->

Chunking documents based on different strategies will result in significant differences in search relevance. We assume that by understanding and extracting the various topics of the corpus (pun intended), we can dynamically select chunks based on the "maximum topic density". This approach is highly experimental and subject to the quality of topic modelling performed as a precursor.

We expect this approach may deliver an uplift in relevance, retrieval, groundedness and F1 Score relative to the baseline.

### Impact
<!-- Creator should fill this in -->

When choosing a chunking strategy for chunking whole documents, we need insight into how our choices impact search relevance and how those choices should vary based on document length.

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

For more information on these metrics see the [documentation](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-metrics-built-in?tabs=warning)

## Methodology

### Initial Plan
<!-- Creator should fill this in -->

Experimenter should:
- [ ] Execute the chunking strategy on the [agreed dataset](adrs/ADR%20-%20Data.md).
- [ ] Embed the chunks using the [agreed embedding model](adrs/ADR%20-%20Embedding%20Model.md).
- [ ] Create an appropriately named index in the [vector store](adrs/ADR%20-%20Vectorstore.md) and load all chunks and associated metadata 
- [ ] Run the questions dataset against the newly created index 
- [ ] Evaluate the search results for a set of queries against the vector store using the metrics noted in the [Measures of Success](#measure-of-success) section.
- [ ] Analyze the results to determine if there are statistically significant differences in the results based on the chunking strategy used, and if so, what those differences are.

### Assumptions and Limitations

### Data Specification
- See [experiment family definition](./00-chunking-strategies-family.md).

## Execution 

### Execution Details
<!-- Experimenter should fill this in -->

{In conducting this experiment, how did you deviate from the initial plan, and why? Is there anything we can learn from those deviations that may influence future experiments?}

## Results
<!-- Experimenter should fill this in -->

{What were the concrete results of the experiment? How do those results compare to your expectations? Was this a success or a failure?}

### Results Summary

### Results References
<!-- Experimenter should fill this in -->

{If the experiment was executed in a Jupyter Notebook, link to the notebook here.}

## Review
<details><summary>Review Summary (click to expand)</summary>
What were the key takeaways from the review process? Were there any significant issues raised during review that need to be addressed?
</details>

### [Optional] Additional references
<!-- Experimenter should fill this in -->

{If there are any other related notebooks/experiments or external references that are relevant for this experiment.}
# Chunking Strategies

This repo is a guide to on how to structure genAI experiments, with a particular focus on the thought process nd decisions to be made when selecting a chunking strategy.

## Who is this for

This repo is for software engineers who are starting out building generative AI applications, in particular Retrieval Augmented Generation systems. If you've built the "hello, world!" RAG apps already, and are wondering how to improve the system performance to win over your users. 

Like wth most data probles, there's no single optimal configuration that will work for all datasets. This guide aims to outline how to experiment with your chunking strategies, and identify the levers you can pull, and how to measure performance.

We restrict the scope to chunking methodologies, but can expand to other aspects of RAG if there is enough demand for it.

## Prereqs
- Azure Open AI resource
- Deployments of:
    - an embedding model
    - an LLM (suggest using gpt-4 for Q&A generation, and 35-turbo-16k elsewhere)
- Python 3.10 onwards (tested on 3.11)

## Setup

- Create a .env file using the [sample file](../.env.sample)
- Run and follow along with [00-Chunking Strategies.ipynb](./chunking_strategies/00-Chunking%20Strategies.ipynb)
- Run and follow along with [01-Baseline Strategy.ipynb](./chunking_strategies/01-Baseline%20Strategy.ipynb)
- Run and follow along with [02-Recursive Chunking.ipynb](./chunking_strategies/02-Recursive%20Chunking.ipynb)
- View the results in MLFlow (launched from within the notebooks)

> NOTE: Given the nature of RAG, running these from scratch can take some time and can be resource intensive. Some example outputs have been provided throughout in the chunking_Strategies/data folder to allow for quick exploration. Feel free to update the parameters at the top of the experiment notebooks and / or use different models in your .env file to try running your own experiment and compare the results
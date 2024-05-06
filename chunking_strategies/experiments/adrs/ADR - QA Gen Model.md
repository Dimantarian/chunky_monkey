# Which LLM to use to Generate Question/Answer pairs 

## Context and Problem Statement

Due to lack of subject matter expertise on the pubmed dataset, this repo takes the (flawed) approach of generating Q&A data via an LLM. It submits documents one by one to the model instructing it to generate 5 question answer pairs.

## Considered Options

- GPT4
- GPT35-turbo

## Decision Outcome

- GPT4

Given this only needs to be ran once, the benefits of higher quality question answer pairs outweighed the cost / time investment of having to use a larger model.
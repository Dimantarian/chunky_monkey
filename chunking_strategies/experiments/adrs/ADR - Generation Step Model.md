# Which LLM to use for the Generation Step

## Context and Problem Statement

An LLM is required to generate an answer to a provided user question, taking into account the retrieved context.

## Considered Options

- GPT4
- GPT35-turbo-16k

## Decision Outcome

- GPT35-turbo-16k

Whilst GPT4 would have been preferable for quality of answer, we tend to recommend smaller models to customers, and focus on the quality of the retrieval. This makes for a more cost efficient and performant system.
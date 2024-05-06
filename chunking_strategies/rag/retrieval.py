import os
from dotenv import load_dotenv, find_dotenv
import chromadb.utils.embedding_functions as embedding_functions
from helper.logging import logger

load_dotenv(find_dotenv())

logger = logger()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_type="azure",
    api_version=os.getenv("OPENAI_API_VERSION"),
    model_name="text-embedding-ada-002",
)


def create_index(
    client, index_name, embedding_function, metadata={"hnsw:space": "cosine"}
):
    index = client.create_collection(
        name=index_name, embedding_function=embedding_function, metadata=metadata
    )
    logger.info(f"Created index: {index_name}")
    return index


def add_documents(index, chunks, chunk_ids, doc_ids, embeddings=None):

    if embeddings is None:
        logger.info("Generating embeddings on load. Please be patient")
        index.add(
            documents=chunks,
            metadatas=[{"doc_id": doc_id} for doc_id in doc_ids],
            ids=chunk_ids,
        )

    else:
        logger.info("Adding pre-generated embeddings")
        index.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{"doc_id": doc_id} for doc_id in doc_ids],
            ids=chunk_ids,
        )

    return None

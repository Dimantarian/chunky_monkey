from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd
from datasets import Dataset
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from ragas import evaluate

load_dotenv(find_dotenv())

from ragas.metrics import (
    context_precision,
    answer_relevancy,
    faithfulness,
    context_recall,
)


def ragas_evaluate(
    df: pd.DataFrame,
    metrics=None,
    azure_model=None,
    azure_embeddings=None,
):

    dataset = Dataset.from_pandas(df)

    # Check if the dataset has the necessary features
    # (question :str, ground_truth: str, answer: str, contexts: list)

    if "question" not in dataset.column_names:
        raise ValueError("The dataset must have a 'question' column")
    if "ground_truth" not in dataset.column_names:
        raise ValueError("The dataset must have a 'ground_truth' column")
    if "answer" not in dataset.column_names:
        raise ValueError("The dataset must have an 'answer' column")
    if "contexts" not in dataset.column_names:
        raise ValueError("The dataset must have a 'contexts' column")

    # list of metrics we're going to use
    if metrics is None:
        metrics = [
            faithfulness,
            answer_relevancy,
            context_recall,
            context_precision,
        ]

    azure_configs = {
        "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "model_deployment": os.getenv("GEN_STEP_MODEL"),
        "model_name": os.getenv("GEN_STEP_MODEL"),
        "embedding_deployment": os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
        "embedding_name": os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
    }

    azure_model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_endpoint=azure_configs["base_url"],
        azure_deployment=azure_configs["model_deployment"],
        model=azure_configs["model_name"],
        validate_base_url=False,
    )

    # init the embeddings for answer_relevancy, answer_correctness and answer_similarity
    azure_embeddings = AzureOpenAIEmbeddings(
        openai_api_version="2023-05-15",
        azure_endpoint=azure_configs["base_url"],
        azure_deployment=azure_configs["embedding_deployment"],
        model=azure_configs["embedding_name"],
    )

    return evaluate(
        dataset,
        metrics=metrics,
        llm=azure_model,
        embeddings=azure_embeddings,
        raise_exceptions=False,
    )

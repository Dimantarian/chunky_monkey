import pandas as pd
import nltk
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from topic_utils.logging import get_logger

logging = get_logger(__name__)

nltk.download("punkt")


def split_and_reconstitute(strings, minimum, maximum, increment):
    """Split the given strings into sentences, then reconstitute them into chunks.

    Parameters:
    - strings: list of strings to process.
    - minimum: int, the minimum number of sentences per chunk.
    - maximum: int, the maximum number of sentences per chunk.
    - increment: int, the number of sentences to increment by.

    Returns:
    - pandas.DataFrame containing the chunks.
    """

    def split_sentences(text):
        """Split the given text into sentences using NLTK."""
        return nltk.sent_tokenize(text)

    def reconstitute(sentences, min_sentences, max_sentences, increment):
        result = []
        start_index = 0
        doc_id = str(uuid4())

        while start_index < len(sentences):
            end_index = start_index + min_sentences
            chunk_id = str(uuid4())

            while (
                end_index <= len(sentences)
                and (end_index - start_index) <= max_sentences
            ):
                result.append(" ".join(sentences[start_index:end_index]))
                yield doc_id, chunk_id, start_index, end_index, result[-1]
                end_index += increment

            next_start = start_index + increment
            if next_start <= start_index:
                break

            start_index = next_start

            if (
                end_index >= len(sentences)
                and (end_index - start_index) <= min_sentences
            ):
                break

        return result

    data = []
    for string in strings:
        sentences = split_sentences(string)
        for item in reconstitute(sentences, minimum, maximum, increment):
            data.append(item)

    df = pd.DataFrame(data, columns=["doc_id", "chunk_id", "start", "end", "string"])
    return df


def create_chunk_embeddings(
    df: pd.DataFrame, column_to_embed: str, model="all-MiniLM-L6-v2", batch_size=250
) -> pd.DataFrame:
    """Create embeddings for each chunk in the DataFrame using the specified model.

    Parameters:
    - df: pandas.DataFrame containing the chunks to embed.
    - column_to_embed: str, the name of the column containing the strings to embed.
    - model: str, the name of the SentenceTransformer model to use.
    - batch_size: int, the batch size to use when encoding the chunks.

    Returns:
    - pandas.DataFrame with the embeddings added as a new column.
    """
    model = SentenceTransformer(model)
    df["embeddings"] = model.encode(
        df[column_to_embed].tolist(), batch_size=batch_size, show_progress_bar=True
    ).tolist()
    return df


def calculate_similarity(
    df: pd.DataFrame, embedding_column: str, topics: dict
) -> pd.DataFrame:
    """Calculate the cosine similarity between the embeddings and the topic vectors.

    Parameters:
    - df: pandas.DataFrame containing the chunks and their embeddings.
    - embedding_column: str, the name of the column containing the embeddings.
    - topics: dict, a dictionary containing the topic vectors.

    Returns:
    - pandas.DataFrame with the cosine similarity metrics added as new columns.
    """

    metric_columns = [f"{topic}_metric" for topic in topics.keys()]
    logging.info(f"Calculating similarity for {len(metric_columns)} topics")

    topic_vectors = [entry["topic_vector"] for entry in topics.values()]
    logging.info(f"Using {len(topic_vectors)} topic vectors")

    # Convert embedding_column to a NumPy array

    embeddings = np.stack(df[embedding_column].values)
    logging.info(f"Using {len(embeddings)} embeddings")

    # Vectorized cosine similarity
    cosine_similarities = cosine_similarity(embeddings, topic_vectors)

    # Step 2: Convert the dictionary to a DataFrame
    new_columns_df = pd.DataFrame(cosine_similarities, columns=metric_columns)

    # Step 3: Concatenate the new DataFrame with the original DataFrame
    df = pd.concat([df, new_columns_df], axis=1)

    logging.info(f"Cosine similarity calculated for {len(df)} chunks")

    return df


def identify_max_topic(df: pd.DataFrame, topics: dict) -> pd.DataFrame:
    """
    Identifies the topic with the maximum metric value for each chunk and adds the
    corresponding topic and metric columns to the DataFrame.

    Parameters:
    - df: pandas.DataFrame containing the chunks and their metric values.
    - topics: dict, a dictionary containing the topic vectors.

    Returns:
    - pandas.DataFrame with the max_metric and max_topic columns added.
    """
    metric_columns = [f"{topic}_metric" for topic in topics.keys()]
    max_metric_column = "max_metric"
    max_topic_column = "max_topic"

    df[max_metric_column] = df[metric_columns].max(axis=1)
    df[max_topic_column] = df[metric_columns].idxmax(axis=1).str.replace("_metric", "")

    df_reduced = df.drop(columns=metric_columns)

    return df_reduced


def select_max_metric_chunks(df):
    """
    For each doc_id, selects the maximum max_metric within the first chunk (start=0),
    then continues selecting chunks based on the end value of the previously selected chunk,
    until reaching the max end value for each doc_id.

    Parameters:
    - df: pandas.DataFrame with columns ['doc_id', 'chunk_id', 'start', 'end', 'max_metric', 'max_topic']

    Returns:
    - pandas.DataFrame containing the selected rows based on the specified logic.
    """
    # Sort by 'doc_id', 'start', then by 'max_metric' descending to get the max_metric row first within each start group
    df_sorted = df.sort_values(
        by=["doc_id", "start", "max_metric"], ascending=[True, True, False]
    )

    # Initialize the result DataFrame
    result_df = pd.DataFrame()

    # Iterate over each document
    for doc_id, group in df_sorted.groupby("doc_id"):
        current_start = 0
        max_end = group["end"].max()
        while current_start < max_end:
            # Select the row with the current start (the first row for each start due to sorting)
            chunk = group[group["start"] == current_start].head(1)
            if not chunk.empty:
                result_df = pd.concat([result_df, chunk])
                # Update current_start to the 'end' value of the selected chunk - 1
                current_start = chunk.iloc[0]["end"] - 1
            else:
                break

    # Reset index if needed
    result_df.reset_index(drop=True, inplace=True)

    return result_df

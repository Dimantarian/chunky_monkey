import nltk

# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np  # For L2 norm calculation
import uuid
from topic_utils.logging import get_logger
from tqdm.notebook import tqdm

logger = get_logger(__name__)


# Ensure NLTK resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")


def _calculate_topic_densities(
    text: str,
    topics: dict,
    min_substring=20,
    max_substring=50,
    overlap=10,
    increment=5,
    doc_id=None,
) -> list[pd.Series]:
    # Preprocess text: remove stopwords and stem
    # stop_words = set(stopwords.words("english"))
    # stemmer = PorterStemmer()

    best_substrings = []

    if doc_id is None:
        doc_id = uuid.uuid4()

    logger.info(f"Calculating topic densities for document {doc_id}")

    # Tokenize and preprocess words
    words = word_tokenize(text)
    processed_words = words
    # [stemmer.stem(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]

    # Initialize DataFrame
    columns = ["doc_id", "chunk_id", "substring_start", "substring_end", "l2_norm"] + [
        f"{topic}_topic_density" for topic in topics.keys()
    ]

    current_start = 0

    # Loop until the end of the string is reached
    while current_start + min_substring < len(processed_words):
        best_substring = []
        best_density = -1

        # Adjust end point based on min and max substring lengths
        for end in range(
            current_start + min_substring, current_start + max_substring + 1, increment
        ):
            substring = processed_words[current_start:end]

            # Calculate densities for each topic
            densities = []
            for topic in topics.values():
                topic_count = sum(word in topic for word in substring)
                density = topic_count / len(substring)
                densities.append(density)

            # Calculate L2 norm of the densities
            l2_norm = np.sqrt(sum([d**2 for d in densities]))

            # Check if this L2 norm is the best so far
            if l2_norm > best_density:
                chunk_id = uuid.uuid4()
                best_substring = [
                    doc_id,
                    chunk_id,
                    current_start,
                    end,
                    l2_norm,
                ] + densities
                best_density = l2_norm

        # Add the best substring information to DataFrame
        best_substring_series = pd.Series(best_substring, index=columns)

        # Set the new start point for the next iteration
        if best_substring:
            best_substrings.append(best_substring_series)
            current_start = best_substring[3] - overlap
        else:
            break  # Exit if no best substring is found

    return best_substrings


def combined_densities(docs: list[str], topics: dict) -> pd.DataFrame:
    """
    Calculates the topic densities for a list of documents and combines them into
    a single DataFrame.

    Args:
        docs: A list of documents.
        topics: A dictionary of topic terms where each item maps to a topic list.

    Returns:
        combined_densities: A DataFrame of topic densities for all documents.

    """
    logger.info(f"Calculating topic densities for {len(docs)} documents")

    # Map based approach
    # density_map = map(lambda x: _calculate_topic_densities(x, topics), docs)

    # logger.info("Combining topic densities into a list")
    # combined_densities = list(itertools.chain.from_iterable(density_map))

    # List comprehension based approach
    # TODO find a better/more readable way to flatten the list
    combined_densities = [
        density
        for doc in tqdm(docs, desc="Processing docs...")
        for density in _calculate_topic_densities(doc, topics)
    ]

    # element for item in items for element in your_function(item)

    logger.info("Converting topic densities into a DataFrame")
    combined_densities_df = pd.DataFrame(combined_densities)

    return combined_densities_df
